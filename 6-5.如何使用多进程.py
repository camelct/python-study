'''
    问题：如何使用多进程?

    实际案例
        由于python中全局解释器锁(GIL)的存在,在任意时刻只允许一个线程在解释器中运行.
        因此python的多线程不适合处理cpu密集型的任务

        GIL 锁的是 线程

        想要处理cpu密集型的任务，可以使用多进程模型.


    解决方案:
        使用标准库中multiprocessing.Process,它可以启动子进程执行任务.
        操作接口，进程间通信，进程间同步等都与Threading.Thread类似.

'''

# 多进程
'''
from multiprocessing import Process

x = 1

def f(s): 
    global x
    x = 5
    print('hello', x)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',)) # 新建一个子进程p，目标函数是f，args是函数f的参数列表
    p.start() # 开始执行进程
    p.join() # 等待子进程结束
    print(x)
'''

# Process Queue Pipe
'''
from multiprocessing import Process, Queue, Pipe
q = Queue()
q.put(1)
q.get()


def f(q):
    print('start')
    print(q.get())
    print('end')


def f2(c):
    c.send(c.recv() * 2)


if __name__ == '__main__':
    Process(target=f, args=(q,)).start()
    q.put(100)

    c1, c2 = Pipe()
    Process(target=f2, args=(c2,)).start()
    c1.send('abc')
    print(c1.recv())

'''




import time
from threading import Thread
from multiprocessing import Process
def isArmstrong(n):
    a, t = [], n
    while t > 0:
        a.append(t % 10)
        t /= 10
    k = len(a)
    return sum(x ** k for x in a) == n


def findArmstrong(a, b):
    print(a, b)
    res = [k for k in range(a, b) if isArmstrong(k)]
    print("%f - %f: %f" % (a, b, res))


def findByThread(*argslist):
    workers = []
    for args in argslist:
        worker = Thread(target=findArmstrong, args=args)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()


def findByProcess(*argslist):
    workers = []
    for args in argslist:
        worker = Process(target=findArmstrong, args=args)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()


if __name__ == '__main__':
    start = time.time()
    findByProcess((20000, 25000), (25000, 30000))
    # findByThread((20000, 25000), (25000, 30000))

    print(time.time() - start)