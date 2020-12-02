'''
    问题：如何为被装饰的函数保存元数据?

    实际案例
        在函数对象中保存着-些函数的元数据，例如:
        f.__name__: 函数的名字
        f.__doc__: 函数文档字符串
        f.__moudle__: 函数所属模块名;
        f.__dict__: 属性字典
        f.__defaults__: 默认参数元组
        ....
        我们在使用装饰器后，再使用上面这些属性访问时，
        看到的是内部包裹函数的元数据，原来函数的元数据
        便丢失掉了,应该如何解决?


    解决方案:
        使用标准库functools中的装饰器wraps装饰内部包裹函数，
        可以制定将原函数的某些属性，更新到包裹函数上面

'''


from functools import update_wrapper, wraps, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES


def f(a, b=1, c=[]):
    '''f function'''
    print(a, b, c)
    return a * 2


# f.__name__  函数名
# f.__doc__  函数文档
# f.__module__ 函数属于哪个模块， 如果不是导入的，就是 main
# f.__defaults__  定义函数的时候 的默认参数
print(f.__defaults__)

f.__defaults__[1].append('abc')  # 会改变 引用的值， 所以参数最好不要有 引用类型的
f(100)


def f2():
    a = 23
    return lambda k: a ** k


g = f2()
print(g.__closure__)  # 函数的 闭包数据
c = g.__closure__[0]
print(c.cell_contents)
print('='*20)


def mydecorator(func):
    # 直接拿这个来包裹,就可以了
    @wraps(func)
    def wrapper(*args, **kargs):
        '''wrapper function'''
        print('In wrapper')
        func(*args, **kargs)

    '''
    # 这样太不优雅了
    # wrapper.__name__ = func.__name__
    '''

    '''
    # update_wrapper
    update_wrapper(wrapper, func,
                   # 直接替换
                   #('__name__', '__doc__'),
                #    WRAPPER_ASSIGNMENTS, # 可以不传，就是使用默认参数
                   # wrapper 里面也可以有自己的 __xx__  所以可以合并
                   #('__dict__',)
                #    WRAPPER_UPDATES # 可以不传，就是使用默认参数
                   )
    '''
    return wrapper


@mydecorator
def example():
    '''example function'''
    print('In example')


print(example.__name__)  # wrapper
print(example.__doc__)  # wrapper function
print(WRAPPER_ASSIGNMENTS)
print(WRAPPER_UPDATES)
