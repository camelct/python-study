# -*- coding:utf-8 -*-

from random import randint
from collections import Counter
import re

data = [randint(0, 20) for _ in range(30)]

# 解决方案1：
c = dict.fromkeys(data, 0)  # 得到初始的字典，目前每个元素的键值是0
for x in data:
    c[x] += 1


# 解决方案2：
# 将序列传入Counter的构造器，得到Counter对象是元素频度的字典
# Counter.most_common(n)方法得到频度最高的n个元素的列表

c2 = Counter(data)  # 统计出来的c2就是上面c字典的样子
c2.most_common(3)
# 结果：
# [(5, 5), (11, 4), (2, 3)]

# 复杂例子(很多字符串)：
txt = open('CodingStyle').read()
c3 = Counter(re.split(r'\W+', txt))  # 以非字母的字符为分割符
print(c3)
