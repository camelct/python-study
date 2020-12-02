'''
    问题：如何使用多线程?

    实际案例
        http://tabl.finance.yahoo.com/table.csv?s-000001.sz
        我们通过雅虎网站获取了中国股市某支股票csv数据文件，
        现在要下载多只股票的csv数据，并将其转换为xml文件.
        如何使用线程来提高下载并处理的效率?

    解决方案
        使用标准库threading.Thread创建线程，在每-个线程中下载并转换一只股票数据。

'''

from threading import Thread
import csv
from xml.etree.ElementTree import Element, ElementTree
import requests
from io import StringIO


def pretty(e, level=0):
    if len(e) > 0:
        e.text = '\n' + '\t' * (level + 1)
        for child in e:
            pretty(child, level + 1)
        child.tail = child.tail[:-1]
    e.tail = '\n' + '\t' * level


# IO操作 访问网络,或者磁盘
def download(url):
    response = requests.get(url, timeout=3)
    if response.ok:
        return StringIO(response.content)

# CPU 密集型操作
# 然鹅 在python 不适合处理 CPU密集型操作 
# 因为 pyhton 有 GIL, 全局解释器锁, 导致当前只能有一个 线程能够被执行
# 所以就不是真正意义上的 多线程
def csvToXml(scsv, fxml):
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

# 普通 for
# if __name__ == '__main__':
#     '''
#     url = 'http://table.finance.yahoo.com/table.csv?s=00001.sz'
#     rf = download(url)
#     print(rf)
#     if rf:
#         with open('00001.xml', 'wt') as wf:
#             csvToXml(rf, wf)
#     '''

#     for sid in range(1, 11):
#         print('Download...(%d)' % sid)
#         url = 'http://table.finance.yahoo.com/table.csv?s=%s.sz'
#         url %= str(sid).rjust(6, '0')
#         rf = download(url)
#         if rf is None:
#             continue
#         print('Convert to XML... (%d)' % sid)
#         fname = str(sid).rjust(6, '0') + '.xml'
#         with open(fname, 'wt') as wf:
#             csvToXml(rf, wf)


def handle(sid):
    print('Download...(%d)' % sid)
    url = 'http://table.finance.yahoo.com/table.csv?s=%s.sz'
    url %= str(sid).rjust(6, '0')
    rf = download(url)
    if rf is None:
        return
    print('Convert to XML... (%d)' % sid)
    fname = str(sid).rjust(6, '0') + '.xml'
    with open(fname, 'wt') as wf:
        csvToXml(rf, wf)


# 线程方法一:
'''
t = Thread(target=handle, args=(1,))
t.start()
print('main thread')
'''

# 线程方法二:
class MyThread(Thread):
    def __init__(self, sid):
        Thread.__init__(self)
        self.sid = sid

    def run(self):
        handle(self.sid)

threads = []
for i in range(1, 11):
    t = MyThread(i)
    threads.append(t)
    t.start()

for t in threads:
    # 主占函数, 当前面执行完之后再执行
    t.join()

print('main thread')