'''
    如何在一个 for 语句中迭代多个可迭代对象
    
    1.某班学生期末考试成绩，语文，数学，英语分别存储在3个列表中，
    同时迭代三个列表，计算每个学生的总分(并行)

        使用内置函数zip,它能将多个可迭代对象合并，每次迭代返回一个元组.
    
    2.某年级有4个班，某次考试每班英语成绩分别存储在4个列表中，
    依次迭代每个列表，统计全学年成绩高于90分人数. (串行)

        使用标准库中的itertools.chain,它能将多个可迭代对象连接.

'''

# 并行

from random import randint

chinese = [randint(60, 100) for _ in range(40)]
math = [randint(60, 100) for _ in range(40)]
english = [randint(60, 100) for _ in range(40)]

# for i in range(len(math)):
#     chinese[i] + math[i] + english[i]
#  该方法是有局限性的 如果是 迭代器就不能用这种方式

# 而使用 zip  只需要传入的是 可迭代对象即可

total = []
for c, m, e in zip(chinese, math, english):
    total.append(c + m + e)

print(total)


# 串行

from itertools import chain

e1 = [randint(60, 100) for _ in range(40)]
e2 = [randint(60, 100) for _ in range(42)]
e3 = [randint(60, 100) for _ in range(43)]
e4 = [randint(60, 100) for _ in range(39)]

count = 0

for s in chain(e1, e2, e3, e4):
    if s > 90:
        count += 1

print(count)