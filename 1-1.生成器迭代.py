'''

    问题：如何使用生成器函数实现可迭代对象

    实例：实现一个可迭代对象的类，能迭代出给定返回内的

    解决方案： 将该类的 __iter__ 方法实现成生成器函数，每次yield返回一个内容
'''


class PrimeNumbers:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def isPrimeNum(self, k):
        if k < 2:
            return False

        for i in range(2, k):
            if k % i == 0:
                return False

        return True

    def __iter__(self):
        for k in range(self.start, self.end + 1):
            if self.isPrimeNum(k):
                yield k

for x in PrimeNumbers(1, 100): print(x)