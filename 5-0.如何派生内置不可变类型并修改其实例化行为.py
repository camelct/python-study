'''
    问题：如何派生内置不可变类型并修其改实例化行为?

    实际案例
        我们想自定义-种新类型的元组，对于传入的可迭代对象，我们只保留作其中int类型且值大字0的元素，例如:
        IntTuple([1,-1, 'abc',6, ['x', 'y'], 3])=>(1,6,3)

        要求IntTuple是内置tuple的子类，如何实现?

    解决方案
        定义类IntTuple继承内置tuple,并实现__new__  修改实例化行为.

'''

class IntTuple(tuple):
    # cls 当前 class
    def __new__(cls, iterable):
        g = (x for x in iterable if isinstance(x, int) and x > 0)
        return super(IntTuple, cls).__new__(cls, g)

    def __init__(self, iterable):
        # before
        print(self)
        super(IntTuple, self).__init__()
        # after
    
t = IntTuple([1,-1, 'abc',6, ['x', 'y'], 3])
print(t)