'''
    问题：如何解析简单的xml文档?

    实际案例
        xml是一种十分常用的标记性语言，可提供统一的方法来描述应用程序的结构化数据:
        <?xml version="1.0" ?>
        <data>
            <country name="Liechtenstein">
                <rank updated="yes">2</rank>
                <year>2008</year>
                <gdppc>141100</gdppc>
                <neighbor name="Austria" direction="E" />
                <neighbor name="Switzer Land" direction="M" />
            </country>
            <country name="Singapore">
                <rank updated="yes">3</rank>
                <year>2011</year>
                <gdppc>141100</gdppc>
                <neighbor name="Austria" direction="E" />
                <neighbor name="Switzer Land" direction="M" />
            </country>
        </data>


    解决方案：
        使用标准库中的xml.etree. ElementTree,其中的parse函数可以解析xml文档。

'''

from xml.etree.ElementTree import parse

f = open('demo.xml')
et = parse(f)
root = et.getroot() # tag  attrib  text
for child in root:
    print(child.get('name'))

print(root.find('country'))
print(root.findall('country'))

for e in root.iterfind('country'):
    print(e.get('name'))

print(list(root.iter('rank')))

# 查找的高级用法
root.findall('country/*') #\                            *               匹配任意
root.findall('.//rank') #\                              //              所有子集
root.findall('.//rank/..') #\                           ..              父级
root.findall('country[@name]') #\                       @attrib         属性
root.findall('country[@name="Liechtenstein"]') #\       @attrib="value" 属性 值
root.findall('country[rank]') #\                        tag             标签
root.findall('country[rank="2"]') #\                    tag="text"      标签内容
root.findall('country[.="2"]') #\                       .="text"        所有内容
root.findall('country[1]') #\                           position        int    last()   last() - 1