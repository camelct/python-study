'''
    问题：如何线程间通信?

    实际案例
        http://table.finance.yahoo.com/table.csvs-000001.sz
        我们通过雅虎网站获取了中国股市某支股票csv数据文件，
        现在要下载多只股票的csv数据，并将其转换为xml文件.

        实现一个线程，将转换出的xml文件压缩打包.比如转换线
        程每生产出100个xml文件，就通知打包线程将它们打包成
        一个xxx.tgz文件,并删除xml文件.打包完成后，打包线程反
        过来通知转换线程，转换线程继续转换.

    解决方案:
        线程间的事件通知，可以使用标准库中Threading.Event:
        1.等待事件端调用wait, 等待事件.
        2.通知事件端调用set, 通知事件.

'''

# 打包
'''
def tarXML(tfname):
    tf = tarfile.open(tfname, 'w:gz')
    for fname in os.listdir('.'):
        if fname.endswith('.xml'):
            tf.add(fname)
            os.remove(fname)
    tf.close()

    if not tf.members:
        os.remove(fname)


tarXML('test.tgz')
'''

# eventBus 通知
'''
from threading import Event, Thread
def f(e):
    print('f 0')
    e.wait() # 开始阻塞 等待事件一端调用 wait; 等待事件
    print('f 1')

e = Event()
t = Thread(target=f, args=(e,))
t.start() 

e.set() # 通知事件 一段调用 set, 通知事件

e.clear() # 清除一下
'''


# from collections import deque
# # 线程间通讯
# q = deque()


from Queue import Queue
from io import StringIO
import requests
from xml.etree.ElementTree import Element, ElementTree
import csv
from threading import Thread, Event
import tarfile
import os

def pretty(e, level=0):
    if len(e) > 0:
        e.text = '\n' + '\t' * (level + 1)
        for child in e:
            pretty(child, level + 1)
        child.tail = child.tail[:-1]
    e.tail = '\n' + '\t' * level


# 生产者
class DownloadThread(Thread):
    def __init__(self, sid, queue):
        Thread.__init__(self)
        self.sid = sid
        self.url = 'http://table.finance.yahoo.com/table.csv?s=%s.sz'
        self.url %= str(sid).rjust(6, '0')
        # 使用全局不安全, 用这种方式 成员变量安全
        self.queue = queue

    # IO操作 访问网络,或者磁盘
    def download(self, url):
        response = requests.get(url, timeout=3)
        if response.ok:
            return StringIO(response.content)

    def run(self):
        print('Download', self.sid)
        # 1. 线程下载
        data = self.download(self.url)
        # 2. 转换 (sid, data)
        # 多个来访问的时候,就不安全, 需要 加锁
        # q.append((self.sid, data))
        self.queue.put((self.sid, data))

# 消费者
class ConvertThread(Thread):
    def __init__(self, queue, cEvent, tEvent):
        Thread.__init__(self)
        self.queue = queue
        self.cEvent = cEvent
        self.tEvent = tEvent

    # CPU 密集型操作
    # 然鹅 在python 不适合处理 CPU密集型操作
    # 因为 pyhton 有 GIL, 全局解释器锁, 导致当前只能有一个 线程能够被执行
    # 所以就不是真正意义上的 多线程
    def csvToXml(self, scsv, fxml):
        reader = csv.reader(scsv)
        headers = next(reader)
        headers = map(lambda h: h.replace(' ', ''), headers)

        root = Element('Data')
        for row in reader:
            eRow = Element('Row')
            root.append(eRow)
            for tag, text in zip(headers, row):
                e = Element(tag)
                e.text = text
                eRow.append(e)

        pretty(root)
        et = ElementTree(root)
        et.write(fxml)

    def run(self):
        count = 0
        # 因为只有一个 消费者 所以可以 循环
        while True:
            sid, data = self.queue.get()
            print('Convert', sid)
            if sid == -1:
                # 当不足5个的时候,也可以打包
                self.cEvent.set()
                self.tEvent.wait()
                break
            # 1. sid data
            if data:
                # 2.
                fname = str(sid).rjust(6, '0') + '.xml'
                with open(fname, 'wt') as wf:
                    self.csvToXml(data, wf)
                count += 1
                if count == 5: # 如果有5个则打包
                    self.cEvent.set() # 通知对端 可以打包
                    self.tEvent.wait() # 对端在打包, 所以等待
                    self.tEvent.clear() # 清空,重复使用
                    count = 0

# 通知, 与被通知
# 作为一个守护线程, 其它线程退出后,自动推出 (是为其它进程服务的)
class TarThread(Thread):
    def __init__(self, cEvent, tEvent):
        Thread.__init__(self)
        self.count = 0
        self.cEvent = cEvent
        self.tEvent = tEvent
        self.setDaemon(True)

    def tarXML(self):
        self.count += 1
        tfname = '%d.tgz' % self.count
        tf = tarfile.open(tfname, 'w:gz')
        for fname in os.listdir('.'):
            if fname.endswith('.xml'):
                tf.add(fname)
                os.remove(fname)
        tf.close()

        if not tf.members:
            os.remove(fname)

    def run(self):
        while True:
            self.cEvent.wait() # 等待 对方通知 
            self.tarXML() # 开始打包
            self.cEvent.clear() # 清除一下,重复使用

            self.tEvent.set() # 告诉对端打包完成了

if __name__ == '__main__':
    q = Queue()
    dThreads = [DownloadThread(i, q) for i in range(1, 11)]

    cEvent = Event() # 转化完成 事件
    tEvent = Event() # 打包完成 事件

    cThread = ConvertThread(q, cEvent, tEvent)
    tThread = TarThread(cEvent, tEvent)
    tThread.start()

    for t in dThreads:
        t.start()

    cThread.start()

    for t in dThreads:
        t.join()

    q.put((-1, None))
    print('done')


