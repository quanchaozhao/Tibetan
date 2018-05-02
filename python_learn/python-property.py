#*_* coding=utf-8 *_*

import numpy as np
from skimage import io,data,filters
import matplotlib.pyplot as plt
def get_fileter_image(image):
    row, col = image.shape
    filter_image = image[:]
    for i in range(row):
        for j in range(2, col - 2):
            if (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 1) or \
                    (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][j + 2] == 1) or \
                    (image[i][j - 2] == 1 and image[i][j - 1] == 0 and image[i][j] == 0 and image[i][j - 1] == 1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0) or (
                                    image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 and image[i][
                            j + 2] == 0):
                filter_image[i][j] = 0
    return filter_image

def get_outline(image):

    rows,cols = image.shape
    image_outline = np.zeros((rows,cols))

    for i in range (rows):
        for j in range(cols):
            pass

import cv2 as cv
import numpy as np

from math import atan,pi

def contours(img):
    dst = cv.GaussianBlur(img, (3, 3), 0)
    # 转换为灰度图像
    gray = cv.cvtColor(dst, cv.COLOR_RGB2GRAY)
    # 转换为二值图像
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("bi", binary)

    cloneImg, contours, heriachy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        cv.drawContours(img, contours, i, (0, 0, 255), 2)
    cv.imshow("contpurs", img)
    p1 = plt.subplot(111)
    p1.imshow(img)
    plt.show()

# src = cv.imread("D:\\database\\2\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-10-0551_0_313.png")
# cv.imshow('def', src)
# contours(src)
# cv.waitKey(0)
# cv.destroyAllWindows()
# import cv2
# img = cv2.imread("D:\\database\\2\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-10-0551_0_313.png")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# _,contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
# cv2.imshow("img", img)
# p1 = plt.subplot(111)
# p1.imshow(img)
# plt.show()
# cv2.waitKey(0)
import  os
s = [x for x in os.listdir(".") if os.path.isdir(x)]
s = []
for x in os.listdir("D:\\藏文识别\\相关文献"):
    if os.path.isfile(x):
        s.append(x)

# import pickle
# d = dict(name='Bob', age=20, score=88)
#
# import json
# class Student(object):
#     def __init__(self, name, age, score):
#         self.name = name
#         self.age = age
#         self.score = score
# s = Student('Bob', 20, 88)
# def dict2student(d):
#     return Student(d['name'], d['age'], d['score'])
# print(json.dumps(s, default = lambda obj: obj.__dict__))
# json_str = '{"age": 20, "score": 88, "name": "Bob"}'
# print(json.loads(json_str, object_hook=dict2student).name)
import copy
def get_fileter_image(image):
    row, col = image.shape
    filter_image = image[:]
    for i in range(row):
        for j in range(2, col - 2):
            if (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 1) or \
                    (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][j + 2] == 1) or \
                    (image[i][j - 2] == 1 and image[i][j - 1] == 0 and image[i][j] == 0 and image[i][j - 1] == 1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0) or (
                                    image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 and image[i][
                            j + 2] == 0):
                filter_image[i][j] = 0
    return filter_image
def adjunction_image(image):
    row, col = image.shape
    ad_image = np.zeros((row + 6, col + 6))
    for i in range(row):
        for j in range(col):
            ad_image[i + 3][j + 3] = image[i][j]
    return ad_image
def get_outline(image):
    rows,cols = image.shape
    image_copy = np.zeros((rows,cols))
    for i in range(1,rows - 2,1):
        for j in range(1,cols - 2,1):
            if(image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 ) or \
                    (image[i][j - 1] == 1 and image[i][j ] == 1 and image[i][j + 1] == 0) or\
                    (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0):
                image_copy[i][j] = 1
    for i in range(1, cols - 2, 1):
        for j in range(1, rows - 2, 1):
            if (image[j - 1][i]== 0 and image[j][i] == 1 and image[j + 1][i] == 1) or \
                    (image[j - 1][i] == 1 and image[j][i] == 1 and image[j + 1][i] == 0) or \
                    (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 0):
                image_copy[j][i] = 1
    return image_copy
def getCornerPoint(image):
    rows,cols = image.shape
def findPoint(image,point,isHorizontal = True):
    rows,cold = image.shape
    pointx,pointy = point[0],point[1]
    tempx, tempy = point[0],point[1]
    prex, prey = pointx,pointy
    if(isHorizontal):
        while(abs(tempx - pointx) < 4 and abs(tempy - pointy) < 4):
            print(tempx,tempy,"fsfsdf")
            if(image[tempx - 1][tempy] == 1 and image[tempx - 1][tempy - 1] == 0 and
                       image[tempx][tempy - 1] == 0 and image[tempx + 1][tempy - 1] == 0 and
                       image[tempx + 1][tempy] == 0):
                pass
            if (image[tempx - 1][tempy] == 1) and (not(tempx - 1 == prex and tempy == prey)):
                tempx = tempx - 1
                prex, prey = tempx, tempy

                continue
            if(image[tempx - 1][tempy - 1] == 1) and (not(tempx - 1 == prex and tempy - 1 == prey)):
                tempx = tempx - 1
                tempy = tempy - 1
                prex, prey = tempx, tempy
                continue
            if(image[tempx][tempy - 1] == 1) and (not(tempx == prex and tempy - 1 == prey)):
                tempx,tempy = tempx,tempy - 1
                prex, prey = tempx, tempy
                continue
            if(image[tempx + 1][tempy - 1] == 1) and (not(tempx + 1 == prex and tempy - 1 == prey)):
                tempx,tempy = tempx + 1,tempy - 1
                prex, prey = tempx, tempy
                continue
            if(image[tempx + 1][tempy] == 1) and (not(tempx + 1 == prex and tempy == prey)):
                tempx,tempy = tempx + 1,tempy
                prex, prey = tempx, tempy
                continue
    else:
        while (abs(tempx - pointx) < 4 and abs(tempy - pointy) < 4):
            print(tempx,tempy,"fsfsdf")
            if (image[tempx - 1][tempy] == 1 and image[tempx - 1][tempy - 1] == 0 and
                        image[tempx][tempy - 1] == 0 and image[tempx + 1][tempy - 1] == 0 and
                        image[tempx + 1][tempy] == 0):
                pass
            if (image[tempx - 1][tempy] == 1) and (not (tempx - 1 == prex and tempy == prey)):
                tempx = tempx - 1
                prex, prey = tempx, tempy
                continue
            if (image[tempx - 1][tempy + 1] == 1) and (not (tempx - 1 == prex and tempy + 1 == prey)):
                tempx = tempx - 1
                tempy = tempy + 1
                prex, prey = tempx, tempy
                continue
            if (image[tempx][tempy + 1] == 1) and (not (tempx == prex and tempy + 1 == prey)):
                tempx, tempy = tempx, tempy + 1
                prex, prey = tempx, tempy
                continue
            if (image[tempx + 1][tempy + 1] == 1) and (not (tempx + 1 == prex and tempy + 1 == prey)):
                tempx, tempy = tempx + 1, tempy + 1
                prex, prey = tempx, tempy
                continue
            if (image[tempx + 1][tempy] == 1) and (not (tempx + 1 == prex and tempy == prey)):
                tempx, tempy = tempx + 1, tempy
                prex, prey = tempx, tempy
                continue
    print("目标点，",point,"========>>>>",[tempx,tempy])
    x,y =[],[]
    x.append(tempx)
    y.append(tempy)
    return x,y

image_origin = io.imread(
        "D:\pycharm\C-Process-photo\example\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_292.png",
        as_grey=True) / 255
image_origin = io.imread( "test.png",as_grey=True) / 255
image_origin = np.where(image_origin > 0,0,1)
p1 = plt.subplot(211)
p1.imshow(image_origin,cmap = "gray")
x,y = 7,15
x1,y1 = findPoint(image_origin,[x,y])
p1.plot(y1,x1,"b.")
p1.plot([y],[x],"g.")
x2,y2 = findPoint(image_origin,[x,y],isHorizontal = False)
print("dd")
from skimage.draw import line

p1.plot(y2,x2,"r.")

angle = abs(atan((y - y1[0] ) / (x - x1[0])) - atan((y2[0] - y) / (x2[0] - x)))
# angle = abs(atan(0))
angle = angle * 180 / pi
print([10,7],"角度为：",angle)


p2 = plt.subplot(212)
p2.imshow((get_outline(adjunction_image(image_origin))),cmap = "gray")

plt.show()