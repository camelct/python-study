'''
    问题：如何定义带参数的装饰器?

    实际案例
        实现一个装饰器，它用来检查被装饰函数的参数类型.
        装饰器可以通过参数指明函数参数的类型,调用时如果
        检测出类型不匹配则抛出异常.
        @typeassert(str, int, int)
        def f(a, b, c):
            ...

        @typeassert(y=list)
        def g(x, y):
            ...

    解决方案:
        提取函数签名inspect.signature()

        带参数的装饰器，也就是根据参数定制化一个装饰器.可以看成生产装饰器的工厂.
        每次调用typeassert返回一个特定的装饰器，然后用它去修饰其他函数。
'''

# 基础框架
'''
def typeassert(*ty_args, **ty_kargs):
    def decorator(func):
        def wrapper(*args, **kargs):
            return func(*args, **kargs)
        return wrapper
    return decorator
'''

'''

from inspect import signature

def f(a, b, c = 1):
    pass

sig = signature(f)
print(sig)
a = sig.parameters['a']
print(a)
print(a.name)
print(a.kind)
print(a.default)

c = sig.parameters['c']
print(c.default)

bargs = sig.bind(str, int, int)
print(bargs.arguments['a'])
print(bargs.arguments['b'])

d = sig.bind_partial(str)
print(d.arguments['a'])

'''

from inspect import signature

def typeassert(*ty_args, **ty_kargs):
    def decorator(func):
        # 函数的映射关系
        # func ->  a,b
        # d = {'a': int, 'b': str}
        sig = signature(func)
        btypes = sig.bind_partial(*ty_args, **ty_kargs).arguments
        print(btypes)
        def wrapper(*args, **kargs):
            # arg in d,  instance(arg, d[arg])
            for name, obj in sig.bind(*args, **kargs).arguments.items():
                if name in btypes:
                    if not isinstance(obj, btypes[name]):
                        raise TypeError('"%s" must be "%s"' % (name, btypes[name]))
            return func(*args, **kargs)
        return wrapper
    return decorator

@typeassert(int, str, list)
def f (a, b, c):
    print(a, b, c)

f(1, 'abv', [1, 2, 3])
f(1, '2', 3)