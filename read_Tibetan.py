#coding:utf-8

with open('Tibetan_dir.txt','r',encoding='utf-8') as fr:
    Tibetan_dir = {}
    tem = fr.readline()
    while(tem):
        key,value = tem.split(':')
        Tibetan_dir[key] = value
        tem = fr.readline()
    print(Tibetan_dir['ཨ ོ'])