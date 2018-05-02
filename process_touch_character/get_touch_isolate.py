# 8_8 coding:utf-8 8_8

import copy
import os
from xml.etree import ElementTree as ET

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
from skimage import io

from pic_process.getConnectedComponent import isolate_character, alterXml

mpl.rcParams['font.sans-serif'] = ['SimHei']

path_Xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total-three\total-addbaseline'
path_image = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total-three\total-addbaseline'
path_Xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine'
path_image = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine'
temPath = r'H:\mark\finish\image_three_touch\three_touch_part1\three_touch_part1\tem'
# path_Xml = r'.\test'
# path_image = r'.\test'
Alter_Xml_path = r'.\_out'
count_file = 0


def alter_point(point):
    for i in range(len(point)):
        for j in range(len(point[i])):
            for k in range(len(point[i][j])):
                print('ffffffffffffff', point[i][j][k])
                point[i][j][k] = int((point[i][j][k] - 15) / 3 + 0.5)
    return point


def get_part_image(XmlFile, isDisplayPart=False, isAlterXml=False):
    global count_file
    text = open(XmlFile, encoding='utf-8').read()
    # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
    root = ET.fromstring(text)
    imageFilename = os.path.join(path_image, root[-1].attrib['ImageFileName'])
    image = None
    try:
        image = np.where(io.imread(imageFilename) > 220, 1, 0)
    except FileNotFoundError:

        print('File:', imageFilename, "Not Found")
        print('File:', XmlFile, "Not Found")
        plt.subplot(111)
        plt.show()
        return -1;
    image_copy = copy.copy(image)
    image_copy_1 = copy.copy(image)
    row, col = image.shape

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
            x = col - 1 if x > col else x
            y = 0 if y < 0 else y
            y = row - 1 if y > row else y
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
    # if(len(total_x) < 3):
    #     count_file = count_file + 3
    # else:
    #     count_file = count_file + len(total_x) + 1
    # return
    print(image_copy.shape)
    total_image, alter_x, alter_y = isolate_character(image_copy, total_y, total_x, isDisplayPart)
    print(alter_x)
    print(alter_y)
    print(imageFilename.split("\\")[-1].replace('chos lugs-pan chen blo chos kyi rgyal mtshan gsung', ''))
    print('    ', len(alter_x) * 2, '  VS  ', len(point_x))
    print(point_x)
    print(point_y)
    if (not isAlterXml):

        k = len(total_image)
        # if k > 2:
        #     return
        for i in range(k):
            row_each, col_each = np.array(total_image[i]).shape
            if(row_each < 10 or col_each < 10):
                continue
            count_file = count_file + 1
            plt.subplot(2, k, (k + i + 1)).imshow(total_image[i])
            # plt.text(20,20,"fff")
        p = np.zeros(k)
        tk = plt.subplot(2, 1, 1)
        tk.plot(point_x, point_y, "r.")
        # tk.plot([y for x in alter_y for y in x], [y for x in alter_x for y in x], "r.")
        tk.set_title(str(imageFilename.split("\\")[-1].split(".")[0]) + ",Pt:" + str(len(point_x)))
        tk.imshow(image_copy_1)
        plt.show()
    else:
        fileName = root[-1].attrib['imageFilename']
        imageHeight = str(int((row - 30) / 3 + 0.5))
        imageWidth = str(int((col - 30) / 3 + 0.5))
        alterXml(fileName, [imageHeight, imageWidth, alter_point(alter_y), alter_point(alter_x)], Alter_Xml_path)
        row, col = image_copy_1.shape
        image_copy_1 = (image_copy_1 * 255).astype(np.uint8)
        new_img = np.zeros((int((row - 30) / 3 + 0.5), int((col - 30) / 3 + 0.5)))
        new_img = cv2.resize(image_copy_1, (int(col / 3 + 0.5), int(row / 3 + 0.5)), interpolation=cv2.INTER_CUBIC)[
                  5:-5, 5:-5]
        io.imsave(os.path.join(Alter_Xml_path, fileName), new_img)
        # shutil.copyfile(imageFilename,os.path.join(Alter_Xml_path,fileName))
        print("save file:" + os.path.join(Alter_Xml_path, fileName))


if __name__ == "__main__":
    for i in os.listdir(path_Xml):
        file = os.path.join(path_Xml, i)
        if file.endswith('.xml'):
            get_part_image(file, isAlterXml=False)
    print('total character: ', count_file)
