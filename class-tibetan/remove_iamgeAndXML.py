# coding:utf-8


import os
import shutil
from skimage import io
import matplotlib.pyplot as plt
origianPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total_alter - 副本'   #原始图像目录
temPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\test'      #临时输出目录
while(True):
    for i in os.listdir(origianPath):
        if i.endswith('.xml'):
            filename = os.path.join(origianPath,i.split('@')[0].replace('_anonymous','.png'))
            # image = io.imread(filename)
            # ss = plt.subplot(111)
            # ss.imshow(image)
            # plt.show()
            print(i)
            # if os.path.isfile(os.path.join(temPath,i)):
            #     os.remove(os.path.join(temPath,i))
            #     print(filename,"has been altered.")
            #     continue
            shutil.move(os.path.join(origianPath,i),temPath)
            shutil.move(filename,temPath)
            print(filename,"has been moved.")
