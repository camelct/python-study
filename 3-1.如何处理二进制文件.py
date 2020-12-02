# link: wav 二进制文件图

'''
    问题：如何处理二进制文件?
        
    实际案例：wav是-种音频文件的格式,音频文件为二进制文件.
    wav文件由头部信息和音频采样数据构成前44个字节
    为头部信息，包括声道数，采样频率, PCM位宽等等,后面是音频采样数据.

    使用python,分析-个wav文件头部信息，处理音频数据.
    WAV格式

    解决方案：
    open函数想以二进制模式打开文件，指定mode参数为"b'.
    二进制数据可以用readinto，读入到提前分配好的buffer中，便于数据处理。
    解析二进制数据可以使用标准库中的struct模块的unpack方法.
'''

import struct
f = open('xueluoxiade.mp3', 'rb')
info = f.read(44)
print(info)

print(struct.unpack('h', b'\x01\x02'))  # 小端 2*256+1
print(struct.unpack('>h', b'\x01\x02'))  # 大端 256 + 2

# 0000_0001 0000 0010  -> 0000_0010 0000_0001
#       256 + 2        ->   256*2  + 1

print(struct.unpack('i', info[0:4]))
print(struct.unpack('b', info[4:5]))
print(struct.unpack('b', info[5:6]))
print(struct.unpack('b', info[6:7]))
print(struct.unpack('b', info[7:8]))


import array
# array.array('h', f.seek(0,2))

f.seek(0, 2)  # 将文件的指针，挪到文件的尾部
a = f.tell()  # 文件大小
print(a)

n = (f.tell() - 44) / 2
buf = array.array('h', (0 for _ in range(n)))
f.seek(44) # 将文件指针 指到 44 处
f.readinto(buf)

print(buf[0])

# 处理数据： 将采样缩小
for i in range(n):
    buf[i] /= 8

f2 = open('demo2.png', 'wb')
f2.write(info)
buf.tofile(f2)
f2.close()

