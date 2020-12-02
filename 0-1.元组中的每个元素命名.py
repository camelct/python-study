# -*- coding:utf-8 -*-
from collections import namedtuple


# 问题描述：
student = ('Jim', 16, 'male', 'jim8721@mail.com')

NAME, AGE, SEX, MAIL = range(4)
# NAME = 0
# AGE = 1
# SEX = 2
# EMAIL = 3

# name
print(student[NAME])

# age
if student[1] >= 18:
    print(student[AGE])

# sex
if student[2] == 'male':
    print(student[SEX])


# 解决方案：
Student = namedtuple('Student', ['name', 'age', 'sex', 'email'])

s = Student('Jim', age=16, sex='male', email='jim8721@gmail.com')

s2 = Student(name='JIm', age=16, sex='male', email='jim123@gmail.com')

print(s.name)
print(s2.age)
