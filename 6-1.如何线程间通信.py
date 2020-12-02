'''
    问题：如何线程间通信?

    实际案例
        htt://table.finance.yahoo.com/table.csv?s-000001.sz
        我们通过雅虎网站获取了中国股市某支股票csv数据文件，
        现在要下载多只股票的csv数据，井将其转换为xm|文件.
        由于全局解释器锁的存在，多线程进行CPU密集型操作并
        不能提高执行效率，我们修改程序构架:
        1.使用多个DownloadThread线程进行下载(/O操作)，
        2.使用-个ConvertThread线程进行转换(CPU密集型操作).
        3.下载线程把下载数据安全地传递给转换线程.

    解决方案

'''

from threading import Thread
import csv
from xml.etree.ElementTree import Element, ElementTree
import requests
from io import StringIO

# from collections import deque
# # 线程间通讯
# q = deque()

from Queue import Queue


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
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

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
        # 因为只有一个 消费者 所以可以 循环
        while True:
            sid, data = self.queue.get()
            print('Convert', sid)
            if sid == -1:
                break
            # 1. sid data
            if data:
                # 2.
                fname = str(sid).rjust(6, '0') + '.xml'
                with open(fname, 'wt') as wf:
                    self.csvToXml(data, wf)


if __name__ == '__main__':
    q = Queue()
    dThreads = [DownloadThread(i, q) for i in range(1, 11)]
    cThread = ConvertThread(q)
    for t in dThreads:
        t.start()

    cThread.start()

    for t in dThreads:
        t.join()

    q.put((-1, None))
    print('done')
