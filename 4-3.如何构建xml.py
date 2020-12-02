'''
    问题：如何构建xml文档?

    实际案例
        某些时候，我们需要将其他格式数据转换为xml,
        例如，我们要把平安股票csv文件，转换成相应xml. 
        pingan.csv:
            Date,Open,High,Low,Close,Volume,Adj Close
            2016-06-30,8.69,8.74,8.66,8.70,36220400,8.70
            2016-06-29,8.63,8.69,8.62,8.69,36961100,8.69
            2016-06-28,8.58,8.64,8.56,8.63,33651900,8.63

        pingan.xml:
            <Data>
                <Row>
                    <Date>2016-07-05</Date>
                    <Open>8.80-/Open>
                    <High>8.83</High>
                    <Low>8.77</Low>
                    <Close>8.81</Close>
                    <Volume>42203700</Volume>
                    <AdjClose>8.81</AdjClose>
                </Row>
            </Data>

    解决方案：
        使用标准 库中的xml.etreeElementTree构建ElementTree,使用write方法写入文件

'''

import csv
from xml.etree.ElementTree import Element, ElementTree, tostring

# e = Element('Data')
# print(e.tag)

# e.set('name', 'abc')



# e2 = Element('Row')
# e3 = Element('Open')
# e3.text='8.80'
# e2.append(e3)
# print(tostring(e2))
# e.text = None
# e.append(e2)
# print(tostring(e))

# et = ElementTree(e)
# et.write('demo2.xml')

def pretty(e, level=0):
    if len(e) > 0:
        e.text = '\n' + '\t' * (level + 1)
        for child in e:
            pretty(child, level + 1)
        child.tail =  child.tail[:-1]
    e.tail = '\n' + '\t' * level

def csvToXml(fname):
    with open(fname, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)

        root = Element('Data')
        for row in reader:
            eRow = Element('Row')
            root.append(eRow)
            for tag, text in zip(headers, row):
                e = Element(tag)
                e.text = text
                eRow.append(e)

    pretty(root)
    return ElementTree(root)

et = csvToXml('pingan.csv')
et.write('pingan.xml')