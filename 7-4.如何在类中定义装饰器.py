'''
    问题：如何在类中定义装饰器,在包裹函数中就可以持有实例对象，便于修改属性和功能

    实际案例
        实现一个能将函数调用信息记录到日志的装饰器:
        1.把每次函数的调用时间,执行时间.调用次数写入日志.
        2.可以对被装饰函数分组,调用信息记录到不同日志.
        3.动态修改参数,比如日志格式.
        4.动态打开关闭日志输出功能

        为了让装饰器在使用上更加灵活，可以把类的实例方法作为装饰器 
        此时在包裹函数中就可以持有实例对象，便于修改属性和功能

        @call_info(arg1, arg2, arg3,...)
        def func(a, b):
            ...

    解决方案:
        为了让装饰器在使用上更加灵活,可以把类的实例方法作为装饰器,
        此时在包裹函数中就可以持有实例对象,便于修改属性和拓展功能
'''

def ff():
    x = 1
    y = [1, 2,3]
    z = 'abc'
    print(locals())

ff()


# coding:utf8
from random import choice
import logging
from time import localtime, time, strftime, sleep


class CallingInfo(object):
    def __init__(self, name):
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)  # 设置等级
        fh = logging.FileHandler(name+'.log')  # 设置文件处理方法
        log.addHandler(fh)  # 绑定方法到log上
        log.info('Start'.center(50, '-'))   # - 占位:-----------Start-----------
        self.log = log  # 绑定到类的属性上
        # 定义了输出模板
        self.formatter = '%(func)s ->[%(time)s - %(used)s -%(ncalls)s]'

    def info(self, func):  # 这个就是平常的装饰器
        def wrapper(*args, **kw):
            wrapper.ncalls += 1
            lt = localtime()  # 返回当地时间
            start = time()
            res = func(*args, **kw)
            used = time() - start

            info = {}  # 建立info的字典
            info['func'] = func.__name__
            info['time'] = strftime('%x %X', lt)
            info['used'] = used
            info['ncalls'] = wrapper.ncalls

            msg = self.formatter % info  # 将字典映射到输入模板上
            self.log.info(msg)  # 输出字符串
            return res
        wrapper.ncalls = 0   # 将调用次数作为函数的属性,比较方便调用
        return wrapper

    def setFromatter(self, formatter):
        self.formatter = formatter

    def turnOn(self):
        """降低级别"""
        self.log.setLevel(logging.INFO)

    def turnOff(self):
        """抬高级别"""
        self.log.setLevel(logging.WARN)  # 级别提高就不在那里输出了


cinfo1 = CallingInfo('mylog1')
cinfo2 = CallingInfo('mylog2')

cinfo1.setFromatter('%(func)s ->[%(time)s  -%(ncalls)s]')
cinfo2.turnOff()  # 这里可以看到是很方便地修改装饰器


@cinfo1.info
def f():
    print('in f')


@cinfo1.info
def h():
    print('in h')


@cinfo2.info
def g():
    print('in g')


for _ in range(10):
    choice([f, g, h])()  # choice 的使用
    sleep(choice([0.5, 1, 1.5]))
