'''
    问题：如何在环状数据结构中管理内存?

    实际案例
        
        在python中,垃圾回收器通过引用计数来回收垃圾对象，但某些环状数据结构(树，图...)存在对象间的循环引用，
        比如树的父节点引用子节点子节点也同时引用父节点.此时同时del掉引用父子节点两个对象不能被立即回收.
        
        如何解决此类的内存管理问题?


    解决方案
        使用标准库weakref,它可以创建一种能访问对象但不增加引用计数的对象，

'''

# import weakref
# class A(object):
#     # 析构函数  在回收的时候,会被调用
#     def __del__(self):
#         print('in A.__del__')

# a = A()

# import sys
# print(sys.getrefcount(a) - 1)
# a2 = a
# print(sys.getrefcount(a) - 1)
# del a2
# print(sys.getrefcount(a) - 1)
# # a = '79'
# # print(sys.getrefcount(a) - 1)
# a_wref = weakref.ref(a)
# a2 = a_wref()
# print(a is a2)

import weakref

class Data(object):
    def __init__(self, value, owner):
        self.owner = weakref.ref(owner)
        self.value = value

    def __str__(self):
        return '%s"s data, value is %s' % (self.owner(), self.value)
    
    def __del__(self):
        print('in Data.__del__')

class Node(object):
    def __init__(self, value):
        self.data = Data(value, self)

    def __del__(self):
        print('in Node.__del__')

node = Node(100)
del node
input('wait...')

# 强制回收 也不能进行回收
# import gc
# gc.collect()
