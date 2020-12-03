# coding:utf8
import logging
import os
from time import localtime, time, strftime

PATH = os.path.dirname(__file__)


class CallingLog(object):
    def __init__(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        fh = logging.FileHandler(os.path.join(
            PATH, 'logs', name+'.log'))
        log.addHandler(fh)
        log.info('Start'.center(50, '-'))
        self.log = log
        self.formatter = '%(func)s ->[%(time)s - %(used)s -%(ncalls)s]'

    def info(self, func):
        def wrapper(*args, **kw):
            wrapper.ncalls += 1
            lt = localtime()
            start = time()
            res = func(*args, **kw)
            used = time() - start

            info = {}
            info['func'] = func.__name__
            info['time'] = strftime('%x %X', lt)
            info['used'] = used
            info['ncalls'] = wrapper.ncalls

            msg = self.formatter % info
            self.log.info(msg)
            return res
        wrapper.ncalls = 0
        return wrapper

    def setFromatter(self, formatter):
        self.formatter = formatter

    def turnOn(self):
        """降低级别"""
        self.log.setLevel(logging.INFO)

    def turnOff(self):
        """抬高级别"""
        self.log.setLevel(logging.WARN)


def warn(timeout):
    def decorator(func):
        def wrapper(*args, **kargs):
            start = time()
            res = func(*args, **kargs)
            used = time() - start
            if used > timeout:
                msg = '"%s": %s > %s' % (func.__name__, used, timeout)
                logging.warn(msg)
            return res

        def setTimeout(k):
            nonlocal timeout

        wrapper.setTimeout = setTimeout
        return wrapper
    return decorator
