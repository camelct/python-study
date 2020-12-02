'''
    问题：如何读写json数据?

    实际案例
        在web应用中常用JSON(JavaScript Object Notation)格式传输数据,
        例如我们利用Baidu语音识别服务做语音识别,
        将本地音频数据post到Baidu语音识别服务器，服务器响应结果为json字符串:
        {"corpus_ no":" 6303355448008565863",
        "err. mg'"ccess."e"r no":0,"result:"你好, 
        "sn":"418359718861467614305"}

        在python中如何读写json数据

    解决方案：
        使用标准库中的json模块其中loads, dumps函数可以完成json数据的读写，

'''

# from secret import API_KEY, SECRET_KEY
# import requests
import json

# # 录音
# from record import Record
# record = Record(channels=1)
# audioData = record.record(2)

# # 获取token
# authUrl = 'https://openapi.baidu.com/xxxx'+API_KEY+SECRET_KEY
# response = requests.get(authUrl)
# res = json.loads(response.content)
# token = res['access_token']

# # 语音识别
# cuid = 'xxxxx'
# srvUrl = 'xxx'
# httpHeader = {
#     'Content-Type': 'audio/wav: rate = 8000'
# }
# response = requests.post(srvUrl, headers=httpHeader, data=audioData)
# res = json.loads(response.content)
# text = res['result'][0]

# print(text)

# 对象 转 json
L = [1, 2, 'abc', {'nane': 'Bob', 'age': 13, 'b': None}]

print(json.dumps(L))

#  将空格删除
print(json.dumps(L, separators=[',', ':']))

#  排序
print(json.dumps(L, sort_keys=True))

# json 转 对象
d2 = json.loads('{"nane": "Bob", "age": 13, "b": null}')
print(d2)

# 文件的读取
with open('demo.json', 'w') as f:
    json.dump(L, f)
