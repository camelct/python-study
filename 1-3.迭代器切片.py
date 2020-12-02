'''
  问题： 如何对迭代器做切片操作

  实例：有某个文本文件，我们想读取其中某范围的内容
    如100 ~ 300行之间的内容, python中文本文件是
    可迭代对象，我们是否可以使用类似列表切片的
    方式得到一个100~300行文件内容的生成器?
    f= open(/var/log/dmesg')
    f[100:300] #可以么?

  解决方案： 使用标准库 itertools.islice 它能返回一个迭代对象切片的生成器
'''

from itertools import islice

l = range(0, 20)
t = iter(l)
for x in islice(t, 5, 10):
    print(x)

print()
print('-'*20)

# islice 返回的是 迭代器，会保存当前的位置
for x in t:
    print(x)
