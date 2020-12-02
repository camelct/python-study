'''
    问题：如何使用函数装饰器?

    实际案例
        某些时候我们想为多个函数统一添加某种 功能，
        比如计时统计，记录日志，缓存运算结果等等.
        我们不想在每个函数内一一添加完全相同的代码


    解决方案:

'''
# 源函数
def fibonacci(n):
    if n <= 1:
        return 1
    return fibonacci(n - 1) + fibonacci( n - 2)

# 缓存处理
def fibonacci2(n, cache=None):
    # cache[n]
    if cache is None:
        cache = {}

    if n in cache:
        return cache[n]

    if n <= 1:
        return 1
    cache[n] = fibonacci2(n - 1, cache) + fibonacci2( n - 2, cache)
    return cache[n]

# print(fibonacci2(50))

# 方式二： 包裹的方式 （装饰器）
# 闭包 保存了 cache
def memo(func):
    cache = {}
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

# 装饰器
fibonacci = memo(fibonacci)
print(fibonacci(50))


@memo
def climb(n, steps):
    count = 0
    if n == 0:
        count = 1
    elif n > 0:
        for step in steps:
            count += climb(n - step, steps)
    return count

print(climb(10, (1,2,3)))