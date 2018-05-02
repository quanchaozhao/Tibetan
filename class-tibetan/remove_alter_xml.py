# coding:utf-8

import os
import shutil
from skimage import io
import matplotlib.pyplot as plt
from datetime import datetime
origianPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total_alter'   #原始图像目录
temPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\test'      #临时输出目录
crate_time = datetime(2018,3,16,15,16)
while(True):
    k = 0
    for i in os.listdir(origianPath):
        if i.endswith('.xml'):
            k = k + 1
            filename = os.path.join(origianPath, i.replace('.xml', '.png'))
            altertime = datetime.fromtimestamp(os.path.getatime(os.path.join(origianPath,i)))
            if(altertime > crate_time):
            # filename = os.path.join(origianPath,i.split('@')[0].replace('_anonymous','.png'))
                print(i)
                shutil.move(os.path.join(origianPath,i),temPath)
                shutil.move(filename,temPath)
                print(filename,"has been moved.")