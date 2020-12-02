'''
    问题：如何去掉字符串中不需要的字符

    案例：1.过滤掉用户输入中前后多余的空白字符: '   nick2008@gmail.com'
      2.过滤某windows下编辑文本中的 '\r':'hello world\r\n'
      3.去掉文本中的unicode组合符号(音调):
      u'ni hao, chi fan'


    解决：方法一:字符串strip(), lstrip(), rstrip()方法去掉字符串两端字符.
        方法二:删除单个固定位置的字符，可以使用切片+拼接的方式
        方法三:字符串的replace()方法或正则表达式re.sub()删除任意位置字符.
        方法四:字符串translate()方法，可以同时删除多种不同字符.

'''

# 方法一： strip

import unicodedata
import sys
import re
s = '   abc     123    '
print(s.strip())
print(s.rstrip())
print(s.lstrip())

s2 = '---abc+++aaa'
print(s2.strip('-+'))

# 方法二： 切片
s3 = 'abc:123'
print(s3[:3] + s3[4:])

# 方法三：  原生 replace  或  re.sub
s4 = '\tabc\t123\tzyzqw\r234wer'
print(s4.replace('\t', ''))

print(re.sub('[\t\r]', '', s4))

# 方法四：   translate 就是翻译，替换
s5 = 'abc1233013xyz'
# 建立映射表
ss = s5.translate(str.maketrans('abcxyz', 'xyzabc'))
print(ss)

u = '（nǐ）（hǎo）（mā）'
print(u)
'''
通过使用dict.fromkeys()方法构造一个字典，每个unicode和音符作为键，对应的值全部为None，
然后使用unicodedata.normalize()将原始输入标准化为分解形式字符
sys.maxunicode:给出最大Unicode代码的值的整数，即1114111（十六进制的0x10FFFF).
unocodedata.combining:将分配给字符chr的规范组合类作为整数返回，如果未定义组合类，则返回0.
'''
cmb_chrs = dict.fromkeys(c for c in range(
    sys.maxunicode) if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', u)
print(b.translate(cmb_chrs))
