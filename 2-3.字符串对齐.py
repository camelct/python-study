'''
    问题：如何对字符串进行 左，右，居中对齐

    案例：某个字典存储了-系列属性值，
    {
        "lodDist": 100.0,
        "Smallull": 0.04,
        "DistCull": 500.0,
        "trilinear": 40,
        "farclip": 477
    }

    在程序中，我们想以以下工整的格式将其内容输出，如何处理?
    Smallull:0.04
    farclip :477
    lodDist : 100.0
    DistCull : 500.0
    trilinear :40 

    解决：方法一:使用字符串的str.ljust(). str.rjust(),str.center()进行左，右,居中对齐.
        方法二:使用format()方法，传递类似"<20','>20', '^20参数完成同样任务.

'''

# 方法一：
s = 'abc'
print(s.ljust(20))
print(s.ljust(20, '='))

print(s.rjust(20))
print(s.rjust(20, '='))

print(s.center(20))
print(s.center(20, '='))

# 方法二：
print(format(s, '<20'))
print(format(s, '>20'))
print(format(s, '^20'))


d = {
    "lodDist": 100.0,
    "Smallull": 0.04,
    "DistCull": 500.0,
    "trilinear": 40,
    "farclip": 477
}

w = max(map(len, d.keys()))
for k, v in d.items():
    print(k.ljust(w), ':', v)


str = '''
    <script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "VideoObject",
        "name": "小米王嵋应该因屌丝言论辞职，但小米粉丝不必因此弃用小米",
        "Description": "-",
        "thumbnailUrl": "//nimg.ws.126.net/?url=http%3A%2F%2Fvideoimg.ws.126.net%2Fcover%2F20201130%2F4binD2UZh_cover.jpg&thumbnail=750x2147483647&quality=85&type=jpg",
        "duration": "PT8M44S",
        "uploadDate": "2020-11-30 09:04:11",
        "contentUrl":"https://flv2.bn.netease.com/6bdca74bcbf8d079d62a95b28d20fcebe721ff0dabe2ae4b27dda3fcbb4f3238a2c1d47c477d7ff22cd232deef069519c46c2e0f167a5ebdb74d0b5cd74db6ba2a7c2dd322beff69f98cf5ee33bf448db8de41307bf74fc5bb84e0859e38c679d9ea05c025db29586ccd01be7f57ba4c1a7a7e98988f9ba0.mp4"
    }
    </script>
    '''

import re
start, end = re.search(r'"uploadDate":', str).span()
print(str[end: end + len("' 2020-11-30 09:04:11'")])