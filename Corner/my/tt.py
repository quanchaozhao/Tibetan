# coding:utf-8

import copy

import matplotlib.pyplot as plt
import numpy as np
from skimage import measure, io


def adjunction_image(image):
    row, col = image.shape
    ad_image = np.zeros((row + 2, col + 2))
    for i in range(row):
        for j in range(col):
            ad_image[i + 1][j + 1] = image[i][j]
    return ad_image


def adjunction_image_min(image):
    row, col = image.shape
    ad_image = np.zeros((row - 2, col - 2))
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            ad_image[i - 1][j - 1] = image[i][j]
    return ad_image


def fff():
    img_ori = io.imread("./Test_Img/chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0002_1_369.png",
                        as_grey=True)
    img_ori = adjunction_image(img_ori)
    img = np.where((copy.copy(img_ori)) > 245, 0, 1)
    lab_img = measure.label(img)
    regions = measure.regionprops(lab_img)
    for region in regions:
        if region.label != 1:
            area = region.coords
            for i in range(len(area)):
                row, col = area[i][0], area[i][1]
                img_ori[row][col] = 255
    p1 = plt.subplot(211)
    p1.imshow(adjunction_image_min(lab_img), cmap='gray')

    p2 = plt.subplot(212)
    p2.imshow(adjunction_image_min(img_ori), cmap='gray')
    plt.show()


import time

nowtime = time.time()
time.sleep(1)
print(time.strftime('%M-%S', time.localtime(time.time() - nowtime)))

s = np.arange(0, 32, 2)
print(len(s))
