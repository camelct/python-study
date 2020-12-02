'''
  如何实现可迭代对象和迭代器对象

    问题：如果一次抓取所有信息，第一有延时，另外浪费存储空间
    
    方案：使用“用时访问”策略，能够把问题封装到一个对象中，然后进行迭代

    解决：
      1. 实现可迭代对象 next 方法每次返回一个城市气温
      2. 实现可迭代对象 __iter__ 方法 返回一个迭代器对象
'''

from collections import Iterable, Iterator
import requests

class WeatherIterator(Iterator):
    def __init__(self, cities):
        self.cities = cities
        self.index = 0

    def getWeather(self, city):
        r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city=' + city)
        data = r.json()['data']['forecast'][0]
        return ('%s: %s, %s' % (city, data['low'], data['high']))

    def __next__(self):
        if self.index == len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return self.getWeather(city)

class WeatherIterable(Iterable):
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        return WeatherIterator(self.cities)


for x in WeatherIterable(['北京', '上海', '广州']):
    print(x)