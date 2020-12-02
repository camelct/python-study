'''
    问题： (如何读写文本文件? )

    案例：某文本文件编码格式已知(如UTF-8, GBK, BIG5), 
        在python 2.x和python 3.x中分别如何读取该文件?

    字符串的语义发生了变化:
    python2             python3
    ---------------------------
    str         ->      bytes
    unicode     ->      str

    python2.x   写入文件 前对unicode编码,读入文件后对二进制字符串解码.
    python3.x   open函数指定't'的文本模式,endcoding指定编码格式



    unicode 是真正含义上的 字符串

    unicode 到 str 的转换
'''

s = '你好'
print(s.encode('utf8'))
print(s.encode('gbk'))

# 编解码 格式统一 否则乱码
print(s.encode('utf8').decode('gbk'))
print(s.encode('utf8').decode('utf8'))

print('='*20)

# py3中 自动编解码
f = open('py3.txt', 'wt', encoding='gbk')
s = '你好'
f.write(s)
f.close()
f = open('py3.txt', 'rt', encoding='gbk')
t = f.read()
print(t)
