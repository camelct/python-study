'''
  如何筛选数据

    列表
        filter函数   filter(lambda: x: x >= 0, data)
        列表解析      [x for in data if x >= 0]

    字典
        字典解析      {k: v for k, v in d.items() if v > 90}

    集合
        集合解析      {x for in s if x % 3 == 0}

'''

'''
  如何统计序列中元素出现的频率

    1.某随机序列 [12,2,3,4,5...]中，找到出现次数最高的3个元素，它们出现的次数是多少？

        from random import randint
        data = [randint(0, 20) for _ in range(30)]
        c = dict.fromkeys(data, 0)
        for x in data:
            c[x] += 1


    2.对某英文文章的单词，进行词频统计，找到出现次数最高的10个单词，它们出现的次数是多少？

        from random import randint
        from collections import Counter
        data = [randint(0, 20) for _ in range(30)]
        c2 = Counter(data)
        a = c2.most_common(3)
        print(a)
'''

# counter


'''
  如何根据字典中值的大小，对字典中的项排序

    from random import randint
    d = {x: randint(60, 100) for x in 'xyzabc'}
    # 方法一： 将字典 转为 元组
    sorted(zip(d.values(), d.keys()))

    # 方法二： 高阶函数
    sorted(d.items(), key=lambda x: x[1])
'''

# sorted
# zip

'''
  如何快速找到多个字典中的公共键（key）?

    利用集合 (set) 的交集操作

    1. 使用字典的 keys() 方法，得到一个字典的集合
        [] & [] 交集
    2. 使用map函数，得到所有字典的 keys 的集合
        arr = map(lambda d: d.keys(), [s1, s2, s3])   转数组
    3. 使用reduce函数，取所有字典的keys的集合的交集
        reduce(lambda cur, pre: cur & pre, arr)  数组迭代


    # sample('abcdefg', randint(3, 6)) # 随机取样
    from random import randint, sample
    from functools import reduce
    s1 = {x: randint(1, 4) for x in sample('abcdefg', randint(3, 6))}
    s2 = {x: randint(1, 4) for x in sample('abcdefg', randint(3, 6))}
    s3 = {x: randint(1, 4) for x in sample('abcdefg', randint(3, 6))}

    arr = map(lambda d: d.keys(), [s1, s2, s3])
    a = reduce(lambda cur, pre: cur & pre, arr)

'''

# [] & []

'''
  如何让字典保持有序
'''
import pickle
from collections import deque
from random import randint
from time import time
from collections import OrderedDict
d = OrderedDict()
players = list('ABCDEFGH')
start = time()

for i in range(8):
    input()
    p = players.pop(randint(0, 7 - i))
    end = time()
    print(i + 1, p, end - start)
    d[p] = (i+1, end - start)

print()
print('-' * 20)
for k in d:
    print(k, d[k])


# sort

'''
  历史记录

    队列，入队出队
'''

N = randint(0, 100)
history = deque([], 5)


def guess(k):
    if k == N:
        print('right')
        return True
    if k < N:
        print('%s is less-than N' % k)
    else:
        print('%s is greater-than N' % k)
    return False


print(N)
while True:
    line = input('please input a number \n')
    if line.isdigit():
        k = int(line)
        history.append(k)
        if guess(k):
            break
    elif line == 'h':
        print(list(history))

pickle.dump(history, open('history', 'wb'))

q2 = pickle.load(open('history', 'rb'))
print(q2)

# pickle
# deque
