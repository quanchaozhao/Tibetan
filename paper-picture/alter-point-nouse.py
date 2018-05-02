# 8_8 coding:utf-8 8_8

import copy
import os
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
from skimage import io

from pic_process.getConnectedComponent import isolate_character, alterXml

mpl.rcParams['font.sans-serif'] = ['SimHei']

path_Xml = r'./Img'
path_image = r'./Img'
Alter_Xml_path = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\test'


def alter_point(point):
    for i in range(len(point)):
        for j in range(len(point[i])):
            point[i][j] = int((point[i][j] - 15) / 3 + 0.5)
    return point


def get_part_image(XmlFile, isDisplayPart=False, isAlterXml=False):
    text = open(XmlFile, encoding='utf-8').read()
    # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
    root = ET.fromstring(text)
    imageFilename = os.path.join(path_image, root[-1].attrib['ImageFileName'])
    image = None
    try:
        image = np.where(io.imread(imageFilename) > 220, 1, 0)
    except FileNotFoundError:

        print('File:', imageFilename, "Not Found")
        return -1;
    image_copy = copy.copy(image)
    image_copy_1 = copy.copy(image)
    print(imageFilename)
    row, col = image.shape
    img = np.zeros((row, col))
    total_x, total_y = [], []
    point_x, point_y = [], []
    for i, textRegion in enumerate(root[-1]):
        listx = []
        listy = []
        if (len(textRegion[0]) % 2 == 0):
            index = len(textRegion[0])
        else:
            index = -1
        for j, pnt in enumerate(textRegion[0][:index]):
            x = int(pnt.attrib['x'])
            y = int(pnt.attrib['y'])
            x = 0 if x < 0 else x
            x = col if x > col else x
            y = 0 if y < 0 else y
            y = row if y > row else y
            listx.append(x)
            listy.append(y)
            point_x.append(x)
            point_y.append(y)
        if (isDisplayPart):
            im1, im2, image, flag = isolate_character(image, listy, listx)
            if (flag == 1):
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
    total_image, alter_x, alter_y = isolate_character(image_copy, total_y, total_x, isDisplayPart)
    print(alter_x)
    print(alter_y)
    print(imageFilename)
    print('    ', len(alter_x) * 2, '  VS  ', len(point_x))
    print(point_x)
    print(point_y)
    if (not isAlterXml):
        # print(alter_x)
        # print(alter_y)
        # print('    ',len(alter_x) * 2,'  VS  ',len(point_x))
        # print(point_x)
        # print(point_y)
        k = len(total_image)

        # if not(k == 1):
        #     total_x, total_y = [], []
        #     point_x, point_y = [], []
        #     return 0
        # for i in range(k):
        #     plt.subplot(2,k,(k + i + 1)).imshow(total_image[i])
        #     # plt.text(20,20,"fff")
        # p = np.zeros(k)
        tk = plt.subplot(1, 1, 1)
        # tk.plot(point_x,point_y,"r")
        tk.plot([y for x in alter_y for y in x], [y for x in alter_x for y in x], "r.")
        tk.plot([0, 75], [23, 23], 'g.-')
        tk.set_title(str(imageFilename.split("\\")[-1].split(".")[0]) + ",Pt:" + str(len(point_x)))
        tk.imshow(image_copy_1, cmap='gray')
        plt.show()
    else:
        fileName = root[-1].attrib['imageFilename']
        imageHeight = str(row)
        imageWidth = str(col)
        alterXml(fileName, [imageHeight, imageWidth, alter_point(alter_y), alter_point(alter_x)], Alter_Xml_path)
        # row, col = image_copy_1.shape
        # image_copy_1 = (image_copy_1 * 255).astype(np.uint8)
        # new_img = np.zeros((int((row - 30) / 3),int((col - 30) / 3)))
        # new_img = cv2.resize(image_copy_1,(int(col / 3), int(row / 3)), interpolation = cv2.INTER_CUBIC)[5:-5,5:-5]
        # io.imsave(os.path.join(Alter_Xml_path,fileName),new_img)
        # # shutil.copyfile(imageFilename,os.path.join(Alter_Xml_path,fileName))
        # print("save file:" + os.path.join(Alter_Xml_path,fileName))


if __name__ == "__main__":
    # path_Xml = "D:\\database\\2\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-19-0875_0_228_anonymous@unknown.com.xml"
    # path = "D:\\database\\2\\"
    # path = "C:\\Users\\Zqc\\Desktop\\Three_touch_part3\\"
    # path = "H:\\mark\\image_two_touchwei16\\touch\\"
    # path = "C:\\Users\\Zqc\\Desktop\\three_touch_part1\\three_touch_part1\\xml\\"
    # path = "E:\\two\\twor\\"
    # path = "H:\\mark\\finish\\image_three_touch\\three_touch_part2\\"
    # path = r"C:\Users\Zqc\Desktop\王森Part31部分(1)\王森Part31部分\touch"
    #
    # path_Xml = "C:\\Users\\Zqc\\Desktop\\test\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_020_anonymous@unknown.com.xml"
    # path = r'C:\Users\Zqc\Desktop\test'
    for i in os.listdir(path_Xml):
        file = os.path.join(path_Xml, i)
        if file.endswith('.xml'):
            get_part_image(file, isAlterXml=False)
