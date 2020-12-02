'''
    问题：如何读写excel文件?

    实际案例
        Microsoft Excel是8常办公中使用最频繁的软件,
        其数据格式为xls, xlsx,-种非 常常用的电子表格.
        小学某班成绩，记录在excel文件中:
        姓名 语文 数学 外语
        李雷 95 99 96
        韩梅 98 100 93
        张峰 94 95 95
        ...

    解决方案：
        利用python读写excel,添加"总分"列，计算每人总分.
        (使用pip安装) pip install xlrd xlwt
        使用第三方库xlrd和xlwt,这两个库分别用于excel读和写.

'''

# # 读 xls
# import xlrd

# book = xlrd.open_workbook('demo.xls')
# print(book.sheets())
# print(book.sheet_by_index(0))
# sheet = book.sheet_by_index(0)
# print(sheet.nrows) # 行
# print(sheet.ncols) # 列

# cell = sheet.cell(1, 1) # 单元格
# print(cell)
# print(cell.ctype)
# print(cell.value)

# row = sheet.row(1) # 行
# print(row)

# print(sheet.row_values(1)) # 行值
# print(sheet.row_values(1, 1)) # 可切片
# # sheet.col_xxx  列也是同理

# # sheet.put_cell(row, col, ctype, value, xf_index)  xf_index = None 字体/对齐

# # 写 xls
# import xlwt
# wbook = xlwt.Workbook()
# wsheet = wbook.add_sheet('sheet1')
# # wsheet.write(r, c, lable, style)
# wsheet.save('output.xls')

import xlrd
import xlwt

rbook = xlrd.open_workbook('demo.xlsx')
rsheet = rbook.sheet_by_index(0)

nc = rsheet.ncols
rsheet.put_cell(0, nc, xlrd.XL_CELL_TEXT, '总分', None)

for row in range(1, rsheet.nrows):
    t = sum(rsheet.row_values(row, 1))
    rsheet.put_cell(row, nc, xlrd.XL_CELL_NUMBER, t, None)


wboot = xlwt.Workbook()
wsheet = wboot.add_sheet(rsheet.name)
style = xlwt.easyxf('align: vertical center, horizontal center')

for r in range(rsheet.nrows):
    for c in range(rsheet.ncols):
        wsheet.write(r, c, rsheet.cell_value(r, c), style)

wboot.save('output.xlsx')
