# coding:utf-8

import os

import numpy as np
from skimage import io

origin_path = r'C:\Users\Zqc\Desktop\数据库\paper-picture\pic\origin_image\totalpic-two'
result_path = r'C:\Users\Zqc\Desktop\数据库\paper-picture\pic\result_image\two'

for i in os.listdir(origin_path):
    image = io.imread(os.path.join(origin_path, i), as_grey=True)
    image = np.where(image > 240, 0, 255)
    io.imsave(os.path.join(result_path, i.replace("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-", '')),
              image)
    print(i, 'is be saved')
