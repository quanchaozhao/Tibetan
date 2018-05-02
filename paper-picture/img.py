#coding:utf-8

import numpy as np
from skimage import io
import os
path = r'C:\Users\Zqc\Desktop\新建文件夹 (3)'


for file in os.listdir(path):
    if file.endswith('.png'):
        image = io.imread(os.path.join(path,file),as_grey=True).astype(np.uint8)
        io.imsave(os.path.join(path,file),image*255)
        print(file)