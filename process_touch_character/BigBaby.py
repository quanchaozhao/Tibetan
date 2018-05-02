# coding:utf-8
"""
Author: quanchaozhao
Email：quanchaozhao@yeah.net
Date: 2018/4/12
"""
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(6, 4))  # 设置图片大小
A = np.linspace(0, 1, 10)  # [1,10]中取10个点
B = np.linspace(0, 1, 10)
C = np.linspace(0, 1, 10)
x = np.linspace(0, 1, 50)  # 在[0，50)中取50个点
for i in A:
    for h in B:
        for k in C:
            plt.plot(x, (i + 6 * h) * x * x + (k - 5 * h) * x + (h + k) * (h + k),
                     )
plt.legend()  # 显示图例
plt.show()  # 显示画图
