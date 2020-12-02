'''
    问题：如何读写csv数据?

    实际案例
        http://table.finance.yahoo.com/table.csvs-00001.sz
        我们可以通过雅虎网站获取了中国股市(深市)数据集，它以csv数据格式存储:
        Date,Open,High,Low,Close,Volume,Adj Close
        2016-06-30,8.69,8.74,8.66,8.70,36220400,8.70
        2016-06-29,8.63,8.69,8.62,8.69,36961100,8.69
        2016-06-28,8.58,8.64,8.56,8.63,33651900,8.63
        ...
        请将平安银行这支股票，在2016年中成交量超过500000000的记录存储到另一个csv文件中.

    解决方案：
        使用标准库中的csv模块，可以使用其中reader和writer完成csv文件读写.

'''


# import urllib.request
# urllib.request.urlretrieve('http://table.finance.yahoo.com/table.csvs-00001.sz', 'pingan.csv')

import csv
with open('pingan.csv', 'rt', newline='') as rf:
    reader = csv.reader(rf)

    with open('pingan_copy.csv', 'w', newline='') as wf:
        writer = csv.writer(wf)
        headers = next(reader)
        writer.writerow(headers)
        print(reader)
        for row in reader:
            print(row)
            if row[0] < '2016-01-01':
                break
            if int(row[5]) >= 1000:
                
                writer.writerow(row)


print('end')


