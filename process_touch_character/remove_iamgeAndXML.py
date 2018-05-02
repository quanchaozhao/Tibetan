# coding:utf-8


import os
import shutil
import matplotlib.pyplot as plt
origianPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine'  # 原始图像目录
temPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine1'  # 临时输出
for i in os.listdir(origianPath):
    if i.endswith('.xml'):
        filename = os.path.join(origianPath, i.replace('xml', 'png'))
        try:
            file = open(filename)
            print(i)
        except FileNotFoundError:
            plt.subplot(111)
            plt.show
# shutil.move(os.path.join(origianPath, i), temPath)
# shutil.move(filename, temPath)
# print(filename, "has been moved.