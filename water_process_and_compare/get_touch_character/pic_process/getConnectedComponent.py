# *** coding:utf-8 ***
import os
from skimage import io,morphology,measure
import numpy as np
import copy
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt

from skimage.draw import line
def nmovlp(pnt1,pnt2):
    '''
    两个距离CC 的距离 left:l right:r top:t bottom:b
    :param pnt1: t_1,l_1,b_1,r_1
    :param pnt2: t_2,l_2,b_2,r_2
    :return:
    '''
    if pnt1[1] > pnt2[1]:
        pnt1,pnt2 = pnt2,pnt1
    t_1, l_1, b_1, r_1 = pnt1
    t_2, l_2, b_2, r_2 = pnt2
    dist =0.5 *abs(l_2+r_2-r_1-l_1)
    w_1 = r_1 - l_1
    w_2 = r_2 - l_2
    ovlp = w_2  if r_1 > r_2 else r_1 - l_2
    span = w_1  if r_1 > r_2 else r_2 - l_1
    if w_1 < w_2:
        ret = ovlp / w_1 - dist / span
    else:
        ret = ovlp / w_2 - dist / span
    return ret

# 删除路径中冗余点
def alter_point(image,point):
    temx,temy = [],[]
    pointx,pointy = point
    if(image[pointx[0]][pointy[0]] == 1):
        temx.append(pointx[0])
        temy.append(pointy[0])
    for i in range(0,len(pointx) - 1,1):
        if(image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][pointy[i + 1]] == 1) or \
                (image[pointx[i - 1]][pointy[i - 1]] == 1 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0):
            temx.append(pointx[i])
            temy.append(pointy[i])
        if (image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0) or \
                (image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0):
            temx.append(pointx[i])
            temy.append(pointy[i])
            temx.append(pointx[i])
            temy.append(pointy[i])
    if (image[pointx[-1]][pointy[-1]] == 1):
        temx.append(pointx[-1])
        temy.append(pointy[-1])
    return temx,temy
# 修正XML文件，fileName为传入的图片，xxx.png，
#TODO ད修正图像大小
def alterXml(fileName,info,path = 'd:'):

    imageHeight, imageWidth,pointx,pointy = info
    print(imageHeight, imageWidth)
    root = ET.Element('root',{'Author':'Quanchao Zhao','Email':'quanchaozhao@yeah.net'})
    pg = ET.SubElement(root,'Page',attrib = {'imageHeight':imageHeight,'imageWidth':imageWidth,'imageFilename':fileName,'class':'','strokeWidth':'8'})
    for i in range(len(pointx)):
        textRegion = ET.SubElement(pg,'TextRegion')
        coods = ET.SubElement(textRegion, 'Coords')
        for j in range(len(pointx[i])):
            ET.SubElement(coods, 'Point', attrib={'x': str(pointx[i][j]), 'y': str(pointy[i][j])})
    tree = ET.ElementTree(root)
    tree.write(os.path.join(path,fileName.split('.')[0] + '.xml'),encoding = 'utf-8',xml_declaration = True)
    pass
def isolate_character(image,pointx,pointy,isdisplay = True):
    """
    分割图像块，并合并连通区域
    :param image:
    :param file:
    :param file2:
    :return:
    """
    Img_copy = copy.copy(image)
    mark_x, mark_y = [], []
    alter_x,alter_y = [],[]
    if(isdisplay):
        for i in range(0, len(pointx) - 1, 2):
            rr, cc = line(pointx[i], pointy[i], pointx[i + 1], pointy[i + 1])
            if (mark_x):
                mark_x.extend(rr[1:])
                mark_y.extend(cc[1:])
            else:
                mark_x.extend(rr[0:])
                mark_y.extend(cc[0:])
        image[mark_x,mark_y] = 0
    else:
        for i in range(len(pointx)):
            mark_x, mark_y = [], []
            for j in range(0,len(pointx[i]) - 1,2):
                rr, cc = line(pointx[i][j], pointy[i][j], pointx[i][j + 1], pointy[i][j + 1])
                if (mark_x):
                    mark_x.extend(rr[1:])
                    mark_y.extend(cc[1:])
                else:
                    mark_x.extend(rr[0:])
                    mark_y.extend(cc[0:])
                x, y = alter_point(image, [rr, cc])
                if(len(x) > 0 and len(y) > 0):
                    alter_x.append(x)
                    alter_y.append(y)
            image[mark_x, mark_y] = 0


    lb_image = measure.label(image,connectivity=1)
    regions = measure.regionprops(lb_image)

    # p1 =plt.subplot(111)
    # p1.imshow(image)
    # plt.show()

    totallist = []
    for region in regions:
        totallist.append([region.bbox, region.image.astype(np.int32),0])
    for i in range(len(totallist)):
       for j in range((len(totallist))):
            confidence_value = nmovlp(totallist[i][0],totallist[j][0])
            if totallist[i][0][1] < totallist[j][0][1] and totallist[i][0][3] < totallist[j][0][3]:
                 min_x1,mid_x1,mid_x2,max_x2 = totallist[i][0][1],totallist[j][0][1],totallist[i][0][3],totallist[j][0][3]
            elif (totallist[i][0][1] > totallist[j][0][1] and totallist[i][0][3] > totallist[j][0][3]):
                min_x1, mid_x1, mid_x2, max_x2 = totallist[j][0][1],totallist[i][0][1],totallist[j][0][3],totallist[i][0][3]
            else:
                min_x1, mid_x1, mid_x2, max_x2 = np.sort([totallist[j][0][1], totallist[i][0][1], totallist[j][0][3],totallist[i][0][3]])
            if totallist[i][2] == 2:
                break
            if totallist[j][2] == 2:
                continue
            if i == j:
                continue
            print(totallist[i][0], totallist[j][0], "confidence",confidence_value)
            if (confidence_value > 0):
                totallist[i][2] = 1
                if(totallist[j][2] == 1):
                    totallist[j][2] == 2
                if(totallist[i][0][1] < totallist[j][0][1] and totallist[i][0][3] > totallist[j][0][3]) or (totallist[j][0][1] < totallist[i][0][1] and totallist[j][0][3] >totallist[i][0][3]):
                    min_x1, mid_x1, mid_x2, max_x2 = np.sort([totallist[i][0][1], totallist[j][0][1], totallist[i][0][3], totallist[j][0][3]])
                    min_y1, a, b, max_y2 = np.sort(
                        [totallist[i][0][0], totallist[j][0][0], totallist[i][0][2], totallist[j][0][2]])
                    a1_y1, a1_y2, a1_x1, a1_x2 = totallist[i][0][1] - min_x1, totallist[i][0][3] - min_x1, totallist[i][0][
                                                     0] - min_y1, totallist[i][0][2] - min_y1
                    b1_y1, b1_y2, b1_x1, b1_x2 = totallist[j][0][1] - min_x1, totallist[j][0][3] - min_x1, totallist[j][0][
                                                     0] - min_y1, totallist[j][0][2] - min_y1
                    tem_image1 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    tem_image2 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))

                    row,col = totallist[i][1].shape
                    for ii in range(row):
                        for jj in range(col):
                            tem_image1[a1_x1 + ii][a1_y1 + jj] = totallist[i][1][ii][jj]
                    row, col = totallist[j][1].shape
                    for iii in range(row):
                        for jjj in range(col):
                            tem_image2[b1_x1 + iii][b1_y1 + jjj] = totallist[j][1][iii][jjj]


                    tem_image = tem_image1 + tem_image2
                    tem = np.where(tem_image > 0.6, 1, 0)
                    # print(tem_image.shape)
                    totallist[i][1] = tem
                    totallist[i][0] = [min_y1, min_x1, max_y2, max_x2]
                    totallist[j][2] = 2

                else :
                    min_y1, a, b, max_y2 = np.sort(
                        [totallist[i][0][0], totallist[j][0][0], totallist[i][0][2], totallist[j][0][2]])
                    a1_y1, a1_y2, a1_x1, a1_x2 = totallist[i][0][1] - min_x1, totallist[i][0][3] - min_x1, totallist[i][0][
                        0] - min_y1, totallist[i][0][2] - min_y1
                    b1_y1, b1_y2, b1_x1, b1_x2 = totallist[j][0][1] - min_x1, totallist[j][0][3] - min_x1, totallist[j][0][
                        0] - min_y1, totallist[j][0][2] - min_y1
                    tem_image1 = np.zeros((max_y2 - min_y1, max_x2 - min_x1 ))
                    tem_image2 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))

                    tem_image1[a1_x1:a1_x2, a1_y1:a1_y2] = totallist[i][1]
                    tem_image2[b1_x1:b1_x2, b1_y1:b1_y2] = totallist[j][1]
                    tem_image = tem_image1 + tem_image2
                    tem = np.where(tem_image > 0.6,1, 0)
                    totallist[i][1] = tem
                    totallist[i][0] = [min_y1,min_x1,max_y2,max_x2]
                    totallist[j][2] = 2
    t = []
    print("The Nnumber of Total Connected Component :", len(totallist))
    for i in range(len(totallist)):
        if(totallist[i][2] != 2):

            min_row, min_col, max_row, max_col = totallist[i][0][0], totallist[i][0][1], totallist[i][0][2],totallist[i][0][3]
            tem = []
            tem.append((max_col - min_col) / 2 + min_col)
            tem.append(totallist[i][1])
            region = [min_row, min_col, max_row, max_col]
            tem.append(region)
            t.append(tem)
    print("The Number of Marget Connected Component",len(t))
    row,col = image.shape
    image = np.zeros((row,col))
    t = sorted(t, key = by_Horizontal_Position)
    if (isdisplay):
        if(len(t) == 2):
            if(t[0][0] < t[1][0]):
                return t[0][1],t[1][1],filter_image(image,t[1]),1
            else:
                return t[1][1], t[0][1],filter_image(image,t[0]),1
        else:
            return Img_copy,Img_copy,Img_copy,0
    else:
        tem = []

        for i in range(len(t)):
            tem.append(t[i][1])
        return tem,alter_x,alter_y

def by_Horizontal_Position(t):
    return t[0]
def filter_image(image,tem):
    """根据原始图像及位置坐标还原图像"""
    image_part = tem[1]
    min_row, min_col, max_row, max_col = tem[2]
    row,col = image_part.shape
    for i in range(row):
        for j in range(col):
            image[i + min_row][j + min_col] = image_part[i][j]
    return image
def get_tibetan_code(key_is_tibeten = True):
    # 将藏文和编码组合成字典，默认格式为{'Tibetan',code}，注释部分为存储Tibetan_dir.txt
    if key_is_tibeten:
        with open('Tibetan_dir.txt', 'r', encoding='utf-8') as fr:
            Tibetan_dir = {}
            tem = fr.readline().strip('\n')
            while (tem):
                key, value = tem.split(':')
                Tibetan_dir[key] = value
                tem = fr.readline().strip('\n')
            print('key = ཨ  , value = ',Tibetan_dir['ཨ ོ'])
    else:
        with open('Tibetan_dir.txt', 'r', encoding='utf-8') as fr:
            Tibetan_dir = {}
            tem = fr.readline().strip('\n')
            while (tem):
                value, key = tem.split(':')
                Tibetan_dir[key] = value
                tem = fr.readline().strip('\n')
            print('key = F30A, value = ',Tibetan_dir['F30A'])
    return Tibetan_dir
# print(get_tibetan_code(key_is_tibeten = False))