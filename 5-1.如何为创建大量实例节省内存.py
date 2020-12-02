'''
    问题：如何为创建大量实例节省内存?

    实际案例
        某网络游戏中，定义了玩家类Player (id, name, status, ...)
        每有一个在线玩家，在服务器程序内则有一个Player的实例，
        当在线人数很多时，将产生大量实例.(如百万级)

        如何降低这些大量实例的内存开销?

    解决方案
        定义类的 __slots__ 属性，它是用来声明实例属性名字的列表.

'''


class Player(object):
    def __init__(self, uid, name, status=0, level=1):
        self.uid = uid
        self.name = name
        self.stat = status
        self.level = level


class Player2(object):
    __slots__ = ['uid', 'name', 'stat', 'level']

    def __init__(self, uid, name, status=0, level=1):
        self.uid = uid
        self.name = name
        self.stat = status
        self.level = level

p1 = Player('0001', 'JIM')
p2 = Player2('0001', 'JIM')

print(dir(p1))
print(dir(p2))

# 集合做差值  p1 比 p2 多了什么
print(set(dir(p1)) - set(dir(p2)))
print(p1.__dict__)

p1.x = 123
print(p1.__dict__)
p1.__dict__['y'] = 99
print(p1.__dict__)
del p1.__dict__['x']
print(p1.__dict__)

import sys
print(sys.getsizeof(p1.__dict__))

# p2.x = 123 # 报错

# __slots__ 这个方法 经常被用来作为封装， 变成了 c 语言中的 结构体， 使得不可动态改变属性