'''
    问题：如何使用线程池?

    实际案例
        我们之前实现了一个多线程web视频监控服务器，我们需要对请求连接数做限制.
        以防止恶意用户发起大量连接而导致服务器创建大量线程，最终因资源耗尽而瘫痪.

        可以使用线程池，替代原来的每次请求创建线程.

    解决方案:
        python3中有线程池实现
        使用标准库中concurrent.futures下的ThreadPoolExecutor,
        对象的submit和map方法可以用来启动线程池中线程执行任务.
'''

# 线程池
'''
from concurrent.futures import ThreadPoolExecutor
import time

executor = ThreadPoolExecutor(3)

def f(a, b):
    print('f', a, b)
    time.sleep(10)
    return a ** b

future = executor.submit(f, 2, 3)
print(future)

# 会阻塞在这，直到运行完
print(future.result())

futures = executor.map(f, [2, 3, 5], [4, 5, 6])
print(futures)
'''


from concurrent.futures import ThreadPoolExecutor
from time import sleep
from select import select
from threading import Thread, RLock
from SocketServer import TCPServer, ThreadingTCPServer
# ignore this file
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import os
import cv2, time, struct, threading

class JpegStreamer(Thread):
    def __init__(self, camera):
        Thread.__init__(self)
        # self.cap = cv2.VideoCapture(camera) # 打开摄像头文件 openCV是图像处理,视觉工具,可以打开图像或视频
        self.lock = RLock()
        self.pipes = {}

    # 数据输出，使用注册的方式
    def register(self):
        pr, pw = os.pipe()  # 创建管道
        self.lock.acquire()  # 对列表进行互斥锁操作
        self.pipes[pr] = pw  # 维护管道的写端  把写端入在了pipes字典  {pr:pw}
        self.lock.release()
        return pr  # 把读端返回给用户接口

    def unregister(self, pr):
        self.lock.acquire()
        pw = self.pipes.pop(pr)  # 将读的键删除值删除
        self.lock.release()
        pr.close()  # 关闭读写管道
        pw.close()

    # 数据采集  返回一个生成器对象
    @property
    def capture(self):
        '''
        cap = self.cap
        while cap.isOpened():
            ret, frame = cap.read() # 从摄像头获取一帧数据
            if ret:
                """
                    返回一个生成器对象，
                """
                # ret, data = cv2.imencode('.jpg', frame)

                ret, data = cv2.imencode(
                    '.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 40))  # 将获取的数据帧编码成jpg图片
                yield data.tostring()
        '''

        while True:
            # opencv库函数 从地址文件获取照片数据，解码器以像素BGR顺序存储到矩阵中。通过照片的内容决定照片的格式，而不是通过后缀名实现的
            frame = cv2.imread(r"test.jpg")

            # 将获取的数据帧编码成jpg图片。 将解码后的数据矩阵编码成相应的格式  返回是一个buffer
            ret, data = cv2.imencode(
                '.jpg', frame, (cv2.IMWRITE_JPEG_QUALITY, 40))

            # 返回一个生成器，变成generator的函数，在每次调用next()或for循环迭代的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
            # tostring具体用法不太知道，这是openCV的依赖库numpy模块里的函数。应该是转换将16进制转为相应的字符串  0x16改为”16“，python写文件是写的字符串或者是反过来的？？？？？
            yield data.tostring()

            sleep(0.2)  # 延时200ms

    """
    将其中的一帧发送到所有已注册的管道中
    """

    def send(self, frame):
        # struct模块用于python的值和c结构转换。官方文档https://docs.python.org/3/library/struct.html#format-characters
        # 这里的意思是把frame的长度按long型转换 如3转换为b‘\x03x00\x00\x00’即0x00000003
        n = struct.pack('l', len(frame))
        """
            >>> from struct import *
            >>> pack('hhl', 1, 2, 3)     #h  对应C_TYPE 为 short
            b'\x00\x01\x00\x02\x00\x00\x00\x03'
            >>> unpack('hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03')
            (1, 2, 3)
        """
        self.lock.acquire()

        # self.pipes字典里有值时，注册后自然就会有值 了
        if len(self.pipes):
            # linux里可以用select监测socket和文件的数据，但windows只能监测socket里的，不能监测文件的
            #_, pipes, _ = select([], self.pipes.itervalues(), [], 1)
            sleep(0.2)
            """
            |  iteritems(...)
            |      D.iteritems() -> an iterator over the (key, value) items of D
            |  
            |  iterkeys(...)
            |      D.iterkeys() -> an iterator over the keys of D
            |  
            |  itervalues(...)
            |      D.itervalues() -> an iterator over the values of D
            """
            for pipe in self.pipes.items():  # 返回字典值的生成器，pipes的键是读pipe 值 是写pipe
                os.write(pipe, n)  # 把长度写入pipe
                os.write(pipe, frame)  # 把图像帧写入pipe
        self.lock.release()

    """
    从capture()获取一帧数据，再发送到管道中去
    """

    def run(self):
        # 循环迭代获取的图片，并把图片数据发送到管道中
        for frame in self.capture:
            self.send(frame)


class JpegRetriever(object):
    def __init__(self, streamer):
        self.streamer = streamer  # 持有一个streamer对象（数据源对象）
        # 需要将每个线程使用的管道，实现线程本地数据，以后每注册一个管道都应该成为这个 self.local的一个属性
        self.local = threading.local()
        # self.pipe = streamer.register()    #多线程就是多线程Retriever来处理,这里用相同的本地数据在不同线程不同值的特点.
        # 调用注册register()接口拿道管道

    # 生成器对象，从管道读取，并返回
    def retrieve(self):
        while True:
            ns = os.read(self.local.pipe, 8)  # 写入的时候明明是4个字节long的长度，读出时为什么读8个长度
            # unpack返回的是一个元组，即使只有一个元素如unpack('l','\x03\x00\x00\x00') 返回 （3,）返回这里加了[0]表示返回元组的第0项
            n = struct.unpack('l', ns)[0]
            data = os.read(self.local.pipe, n)  # 从管道中读出图片数据
            yield data  # 返回生成器，图片数据的生成器，向Handler返回

    """
    retriever是单线程时没有—__enter__()。
    有注册也有注销，最好实现成上下文管理器。__enter__()
    """
    """
    使用管道时，每次使用都需要注册，使用完后都需要注销，这样最好使用上下文管理
    实现上下文管理器 __enter__进入函数
    """
    # 上下文管理 进行注册

    def __enter__(self):
        # self.pipe = streamer.register()

        # 为了避免重复进入enter，判断local下是否有pipe属性，没有时，才注册。hasattr()查看某一对象是否包含某一属性。
        if hasattr(self.local, 'pipe'):
            raise RuntimeError()

        # 注册
        self.local.pipe = streamer.register()  # 注册成为一个本地的管道
        return self.retrieve()  # 得到每一帧的生成器

    """
    def cleanup(self):
        self.streamer.unregister(self.pipe)
    """

    """
    上下文管理器的退出函数，这里先不关心异常，用*args收集异常，压制所有异常
    """

    def __exit__(self, *args):
        self.streamer.unregister(self.local.pipe)
        del self.local.pipe  # 使用完毕后删除本地属性
        return True

# 用于实现HTTP服务器，但自身不能实现，需要通过继承子类，实现do_METHOD(METHOD为具体的方法如GET、POST等)


class Handler(BaseHTTPRequestHandler):
    # 只有一个对象
    retriever = None

    @staticmethod  # 装饰器 使setJpegRetriever成为静态的方法。参见C++的类里静态方法，只能类调用 ，不能实例调用
    def setJpegRetriever(retriever):
        Handler.retriever = retriever  # 将传入的retriever对象赋值给类的retriever的对象

    def do_GET(self):
        if self.retriever is None:
            raise RuntimeError('no retriver')

        """
        http响应头部的构造
        """
        if self.path != '/':
            return

        # 响应头的构造
        self.send_response(200)
        self.send_header(
            'Content-type', 'multipart/x-mixed-replace, boundary=abcde')
        self.end_headers()

        """
        #调用retrieve（）每次拿到一帧数据并通过send_frame()变成hettp的响应发送出去
        for frame in self.retriever.retrieve():
            self.send_frame(frame)
        """
        """
        使用上下文管理，得到数据帧生成器
        """
        with self.retriever as frames:  # 增加上下文管理  打开retriever，循环迭代  得到图到每一帧的数据
            for frame in frames:
                self.send_frame(frame)  # 调用send_frame 将图片的的数据发送到http中去

    # 变成 http 的响应 发送出去
    def send_frame(self, frame):
        self.wfile.write('--abcde\r\n')
        self.wfile.write('Content-Type: image/jpeg\r\n')
        self.wfile.write('Content-Length: %d\r\n\r\n' % len(frame))
        self.wfile.write(frame)

class ThreadingPoolTCPServer(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, max_thread_num=100):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.executor = ThreadPoolExecutor(max_thread_num)

    def process_request(self, request, client_address):
        '''
        Start a new thread to process the request.
        '''
        self.executor.submit(self.process_request_thread, request, client_address)

if __name__ == '__main__':
    streamer = JpegStreamer(0)  # 定义JpegStreamer线程类的对象
    streamer.start()  # 线程启动调用 run（）方法

    retriever = JpegRetriever(streamer)  # 定义JpegRetriever类的实例，
    Handler.setJpegRetriever(retriever)

    print('Start server...')
    # httpd = TCPServer(('', 9000), Handler)     #TCPServer和ThreadingTCPServer的差别是。在处理每一次的http请求的时候，ThreadingTCPServer会创建一个独立的线程来执行Handler中的do_GET
    httpd = ThreadingPoolTCPServer(('', 9000), Handler, max_thread_num = 3)
    httpd.serve_forever()  # 启动服务
