'''
    问题：如何使用描述符对实例属性做类型检查?

    实际案例
        
        在某项目中,我们实现了一些类，并希望能像静态类型语言
        那样(C, C++, Java)对它们的实例属性做类型检查.
            p= Person()
            p.name= 'Bob' #必须是str
            p.age= 18 #必须是int
            p.height= 1.83 #必须是float

        要求:
            1.可以对实例变量名指定类型
            2.赋予不正确类型时抛出异常

    解决方案
        使用描述符来实现需要类型检查的属性:
        分别实现 __get__, __set__, __delete__ 方法，
        在 __set__ 内使用isinstance函数做类型检查.

'''


class Attr(object):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __get__(self, instance, cls):
        print('in __get__', instance, cls)
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print('in __set__', instance, value)
        if not isinstance(value, self.type_):
            raise TypeError('expected an %s' % self.type_)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        print('in __delete__', instance)
        del instance.__dict__[self.name]


class Person(object):
    name = Attr('name', str)
    age = Attr('age', int)
    height = Attr('height', float)


p = Person()
p.name = 'Bob'
print(p.name)
p.age = '17'
