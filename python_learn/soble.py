# coding:utf-8

from skimage import io,filters
import numpy as np
import matplotlib.pyplot as plt

image = io.imread('test.png',as_grey = True)

image = np.where(image > 0, 1,0)
img_x = filters.sobel_h(image)
img_y = filters.sobel_v(image)
img_ang = np.arctan( img_y / img_x)
img_ang_t = np.where(image == 0,img_ang,0)
p1 = plt.subplot(211)
p1.imshow(img_ang_t)

plt.subplot(212).imshow(image)
plt.show()
