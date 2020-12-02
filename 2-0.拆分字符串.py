'''
    问题： 如何拆分含多种分隔符的字符串

    案例： 我们要把某个字符串依据分隔符号拆分不同的字段，
    该字符串包含多种不同的分隔符，例如:
    s = 'ab;cd|efglhi,jklmn\topq;rst,uvw\txyz'
    其中<,>, <>, <|>, <\t>都是分隔符号，如何处理?

    方法一:连续使用是str.split()方法，每次处理一种分隔符号. 
    方法二:使用正则表达式的re.split()方法，-次性拆分字符串.

'''

# 方法一：
# t = []
# s = 'ab;cd|efglhi,jklmn\topq;rst,uvw\txyz'
# res = s.split(';')
# a = map(lambda x: t.extend(x.split('|')), res)

# print(list(a))
# print(res)
# print(t)

# 优化
def mySplit(s, ds):
    res = [s]

    for d in ds:
        t = []
        for z in map(lambda x: x.split(d), res):
            t.extend(z)
        res = t

    return [x for x in res if x]


s = 'ab;cd|efglhi,jklmn\topq;rst,uvw\txyz'
print(mySplit(s, ',;.|\t'))


# 方法二：
import re
aa = re.split('[,;.|\t]+', s)
print(aa)