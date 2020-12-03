
# coding:utf8
import os
import requests
import logging
from queue import Queue
from random import randint
from time import time, sleep
from bs4 import BeautifulSoup
from threading import Thread
from callingLog import CallingLog, warn

logImg = CallingLog('4kdongman_img')

PATH = os.path.dirname(__file__)
HOST = 'http://pic.netbian.com'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/76.0.3809.132 Safari/537.36 "
}


def downloadList(url):
    """ 下载列表页 """

    response = requests.get(url, headers=HEADERS)
    if response.ok:
        return response.text


@logImg.info
def downloadImg(url):
    """ 下载图片 """

    response = requests.get(url, headers=HEADERS)
    if response.ok:
        filename = url.split('/')[-1]

        with open(os.path.join(PATH, 'imgs', filename), 'wb') as f:
            f.write(response.content)
            logging.info('filename: ' + filename + ' has down')


class InfoThread(Thread):
    """ 详情页 """

    def __init__(self, m_queue):
        Thread.__init__(self)
        self.m_queue = m_queue

    def getUrlInfo(self, content):
        soup = BeautifulSoup(content, 'lxml')
        la = soup.select('div.photo-pic img')

        aList = ''
        for tagA in la:
            imgSrc = tagA.get('src')
            aList = HOST + imgSrc
        return aList

    def run(self):
        count = 0
        while True:
            _, data = self.m_queue.get()
            if (count == 5):
                logging.info('Done')
                break

            if data:
                count = 0
                for url in data:
                    sleep(randint(0, 1))
                    dload = downloadList(url)
                    cont = self.getUrlInfo(dload)
                    sleep(randint(0, 2))
                    downloadImg(cont)
            else:
                break

class ListThread(Thread):
    """ 列表页 """

    def __init__(self, sid, m_queue):
        Thread.__init__(self)

        self.isSkip = True if sid == 0 else False
        self.dirName = '4kmeinv'
        self.sid = sid
        self.m_queue = m_queue

    def setDirName(self, dirName):
        self.dirName = dirName

    def getUrlList(self, content):
        soup = BeautifulSoup(content, 'lxml')
        la = soup.select('div.slist a')

        aList = []
        for tagA in la:
            href = tagA.get('href')
            aList.append(HOST + href)
        return aList

    def run(self):
        if not self.isSkip:
            pageStr = '' if self.sid == 1 else '_%s' % self.sid
            url = HOST + '/%s/index%s.html' % (self.dirName, pageStr)
            dload = downloadList(url)
            cont = self.getUrlList(dload)
            self.m_queue.put((self.sid, cont))


if __name__ == '__main__':
    m_queue = Queue()

    listThreads = [ListThread(i, m_queue) for i in range(2, 10)]

    contentThread = InfoThread(m_queue)
    for t in listThreads:
        # t.setDirName('4kdongman')
        t.start()

    contentThread.start()

    for t in listThreads:
        t.join()

    m_queue.put((-1, None))
