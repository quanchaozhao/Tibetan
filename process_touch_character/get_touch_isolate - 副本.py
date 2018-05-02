#8_8 coding:utf-8 8_8

from skimage import io
import numpy as np
import os
import re
from xml.etree import ElementTree
from skimage.draw import polygon
import matplotlib.pyplot as plt
import copy
from pic_process.getConnectedComponent import isolate_character
from pylab import figure,mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

def get_part_image(path,path1):
    text = open(path1).read()
    # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
    display = False
    root = ElementTree.fromstring(text)
    imageFilename = os.path.join(path,root[1].attrib['imageFilename'])
    image = np.where(io.imread(imageFilename) > 220, 1, 0)
    image_copy = copy.copy(image)
    row,col = image.shape
    img = np.zeros((row ,col ))
    total_x ,total_y = [],[]
    for i,textRegion in enumerate(root[1]):
        listx = []
        listy = []
        for j,pnt in enumerate(textRegion[0][:-1]):
            x = int(pnt.attrib['x'])
            y = int(pnt.attrib['y'])
            x = 0 if x < 0 else x
            x = col if x > col else x
            y = 0 if y < 0 else y
            y = row if y > row else y
            listx.append(x)
            listy.append(y)
        if(display):
            im1, im2,image,flag = isolate_character(image, listy, listx)
            if(flag == 1):
                p1 = plt.subplot(211)
                p1.set_title("原始图像")
                p1.imshow(image_copy)
                p2 = plt.subplot(223)
                p2.set_title("分割后的第一部分")
                p2.imshow(im1)
                p3 = plt.subplot(224)
                p3.set_title("剩余图像")
                p3.imshow(im2)
                plt.show()
            else:
                print("无法切分")
        total_x.append(listx)
        total_y.append(listy)
    print(image_copy.shape)
    total_image = isolate_character(image_copy,total_y,total_x,isdisplay = False)

    k = len(total_image)
    p = np.zeros(k)
    tk = plt.subplot(2,1,1)
    tk.set_title("整体切分图像，及分割后的基元部件")
    tk.imshow(image_copy)
    for i in range(k):
        plt.subplot(2,k,(k + i + 1)).imshow(total_image[i])
    plt.show()

    pass
if __name__ == "__main__":
    path1 = "D:\\database\\2\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-19-0875_0_228_anonymous@unknown.com.xml"
    path = "D:\\database\\2\\"
    path = "C:\\Users\\Zqc\\Desktop\\test\\"
    path = "C:\\Users\\Zqc\\Desktop\\Three_touch_part2\\"
    # path1 = "C:\\Users\\Zqc\\Desktop\\test\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_020_anonymous@unknown.com.xml"
    for i in os.listdir(path):
        file = os.path.join(path, i)
        if file.endswith('.xml'):
            get_part_image(path,file)
        # x1 = listx[0]
        # y1 = listy[0]
        #
        # x2 = listx[-1]
        # y2 = listy[-1]
        #
        # listx.insert(0,x1)
        # listy.insert(0,0)
        #
        # listx.insert(0, 0)
        # listy.insert(0, 0)
        #
        # listx.append(x2)
        # listy.append(row - 1)
        #
        # listx.append(0)
        # listy.append(row - 1)
        #
        # listy.append(0)
        # listy.append(0)
        #
        # rr, cc = polygon(listy, listx)
        # img[rr, cc] = 1
        # img = img.astype(int)
        # image = image.astype(int)
        # img = np.bitwise_and(np.array(img), np.array(image))
        # p1 = plt.subplot(223)
        # p1.imshow(img,cmap = 'gray')
        # image = image - img
        # p2 = plt.subplot(224)
        # p2.imshow(image)
        # p3 = plt.subplot(211)
        # p3.imshow(image_copy)
        # plt.show()
    # imageFile = os.path.join(path,file)
    # image = io.imread(imageFile)
    # image = np.where(image > 200, 1,0)
    # print(file)