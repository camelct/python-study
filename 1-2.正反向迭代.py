'''
  问题：如何进行反向迭代 以及 如何实现反向迭代

  实例：实现一个连续浮点数发生器 FloatRange(和 range 类似)，
        根据 给定范围 (start, end) 和 步进值 (step) 产生一些列 连续浮点数，
        如 迭代 FloatRange(3.0, 4.0, 0.2) 可产生序列：

  正向： 3.0 -> 3.2 -> 3.4 -> 3.6 -> 3.8 -> 4.0     iter()   可以得到正向的迭代器
  反向： 4.0 -> 3.8 -> 3.6 -> 3.4 -> 3.2 -> 3.0     reversed()   可以得到反向的迭代器
'''


class FloatRange:
    def __init__(self, start, end, step=0.1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        t = self.start
        while t <= self.end:
            yield t
            t += self.step

    def __reversed__(self):
        t = self.end
        while t >= self.start:
            yield t
            t -= self.step


l = FloatRange(1.0, 4.0, 0.5)
for x in reversed(l):
    print(x)
