'''
    问题：如何判断字符串a是否以字符串b开头或结尾?

    案例：某文件系统目录下有-系列文件:
        quicksort.c
        graph.py
        heap.java
        install.sh
        stack.cpp
        编写程序给其中所有.sh文件和.py文件加上用户可执行权限.


    解决：使用字符串的str.startswith()和str.endswith()方法.
    注意:多个匹配时参数使用元组。

'''

import os
import stat

[print(name) for name in os.listdir('.') if name.endswith(('.sh', '.py'))]

# print(os.stat('stat.py').st_mode)
# os.chmod('stat.py', os.stat('stat.py').st_mode | stat.S_IXUSR)


'''
    问题：如何调整字符串中 文本格式?

    案例：某软件的log文件，其中的日期格式为'yyy-mm-dd':
        2016-05-23 10:59:26 status unpacked python3-pip:all
        2016-05-23 10:59:26 status half-configured python3-pip:all
        2016-05-23 10:59:26 status installed python3-pip:all
        2016-05-23 10:59:26 configure python3-wheel:all 0.24.0-1
        ......
        我们想把其中日期改为美国期的格式'mm/dd/yyyy'.
        '2016-05-23' => 05/23/2016',应如何处理?



    解决：使用正则表达式re.sub()方法做字符串替换，利用正则表达式的捕获组，
        捕获每个部分内容，在替换字符串中调整各个捕获组的顺序.

'''

log = open('log.log').read()

import re
print(re.sub(r'(?P<year>\d{4})-(\d{2})-(\d{2})', r'\2/\3/\g<year>', log))

# ?P<year> 取别名
# \g<year> 使用别名