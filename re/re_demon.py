# coding:utf-8

import re

pattern = re.compile(r'hello[0,3]', re.IGNORECASE)
match = pattern.match('Hello world')

if match:
    print(match.group())
import re

line = "Cats are smarter than dogs"

matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)

if matchObj:
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))

pattern = re.compile(r'[a-z]*')
# print(pattern.match('Wdsdg').group())
print(re.search(r'(^[A-Z]+)(|[a-z]+$)','WSdfd').group())

w = re.findall('\btina','tian tinaaaa')
print(w)
s = re.findall(r'\btina','tian tinaaaa')
print(s)
v = re.findall(r'\btina','tian#tinaaaa')
print(v)
a = re.findall(r'\btina\b','tian#tina@aaa')
print(a)

# pattern = re.compile('com+')
# print(pattern.match('fcom.cd').group())
print(re.match('com','comwww.runcomoob').group())
print(re.match('com','Comwww.runcomoob',re.I).group())
print(re.search('\dcom','www.4comrunoob.5com').group())

text = "JGood  is a handsome boy, he is cool, clever, and so on..."
print(re.sub(r'\s+', '-', text))


s = r'_quanchaozhaodf23@yeah.net'

pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
match = pattern.match(s)
if(match):
    print(match.group())

pattern = re.compile(r'[^abc]+')
if pattern.search(r'gdfgdfgdfgdsg'):
    print('cdcdcdcd')
"""
1、匹配电话号码

p = re.compile(r'\d{3}-\d{6}')
print(p.findall('010-628888'))

2、匹配IP

re.search(r"(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\.)","192.168.1.1")

3、匹配邮箱
pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'

汉字的Unicode编码
[\u4e00-\u9fa5]
4 手机号码：^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$ 

"""