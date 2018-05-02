# coding:utf-8
from skimage import measure, data, io,feature,morphology,filters
import matplotlib.pyplot as plt
from skimage.morphology import disk,skeletonize
import numpy as np
from skimage.feature import corner_fast,corner_peaks
import re
import math
import  cv2
from skimage.feature import corner_harris, corner_peaks
totalpoint = []


def get0_1(image):
    for i in range(2):
        for j in range(2):
            if (image[i][j] == 'False'):
                image[i][j] = 1
            else:
                image[i][j] = 0
    return image


def min(image):
    array = np.sum(image, axis=0)
    start = 5
    end = len(array) - 5

    index = 5

    while (start < end):
        if (array[start] < array[index]):
            index = start
        start = start + 1
    return index


def get_min_point(image, pointx, pointy, index):
    row, col = image.shape
    flag = False
    for i in range(pointy + 1, row):
        for j in range(pointx - 1, index - 1, -1):
            if (image[i][j] == 0):
                pointx = j
                pointy = i
                # print("fFDFFFFFFFFFFFFFFFFFFFFFFFF")
                flag = True
                break
        if (flag):
            break
    return pointx, pointy

def adjunction_image(image):
    row,col = image.shape
    ad_image = np.zeros((row + 4, col + 4))
    for i in range(row):
        for j in range(col):
            ad_image[i + 1][ j + 1] = image[i][j]
    return ad_image

def get_fileter_image(image):
    row, col = image.shape
    filter_image = image[:]
    for i in range(row):
        for j in range(1, col - 3):
            if (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 1) or (
                                    image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][
                            j + 2] == 1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0) or (
                                    image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 2] == 1 and image[i][
                            j + 1] == 0):
                filter_image[i][j] = 0
    return filter_image


def get_min_index_rol(pointx, pointy):
    pointy = np.array(pointy)
    pointx = np.array(pointx)
    # print(pointy[-1])
    count = np.sum(pointy == pointy[-1])
    return pointx[-count]

def get_fork_point(image):
    [row, col] = image.shape
    tem_image = np.zeros((row, col))
    pointx, pointy = [], []
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            count = 0
            if (image[i][j] == 1):
                count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                        image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
                if (count > 2):
                    tem_image[i][j] = 1
                    continue
    tem = np.zeros((row, col))
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            count = 0
            if (tem_image[i][j] == 1):
                if (tem_image[i][j - 1] == 1 and tem_image[i - 1][j] == 1 and tem_image[i][j + 1] and tem_image[i + 1][
                    j] == 1):
                    tem[i][j] = 1
                    continue
                if (tem_image[i][j - 1] == 1 and tem_image[i - 1][j] == 1):
                    tem[i][j] = 1
                    continue
                if (tem_image[i - 1][j] == 1 and tem_image[i][j + 1] == 1):
                    tem[i][j] = 1
                    continue
                if (tem_image[i][j + 1] and tem_image[i + 1][j] == 1):
                    tem[i][j] = 1
                    continue
                if (tem_image[i][j - 1] == 1 and tem_image[i + 1][j] == 1):
                    tem[i][j] = 1
                    continue
                count = tem_image[i - 1][j - 1] + tem_image[i + 1][j - 1] + tem_image[i - 1][j + 1] + tem_image[i + 1][
                    j + 1] + \
                        tem_image[i][j - 1] + tem_image[i - 1][j] + tem_image[i + 1][j] + tem_image[i][j + 1]
                if (count < 2):
                    tem[i][j] = 1
                    continue
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if (tem[i][j] == 1):
                pointx.append(j)
                pointy.append(i)
    angle = np.zeros((row, col))
    # for i in range(1, row - 1, 1):
    #     for j in range(1, col - 1, 1):
    #         if(image[i][j] == 1):
    #             count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
    #                     image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
    #             if (count == 2):
    #                 # 叉4 横竖4
    #                 if(image[i - 1][j - 1] == 1 and image[i + 1][j - 1] == 1) or (image[i - 1][j - 1] == 1 and image[i - 1][j + 1] == 1)\
    #                         or (image[i - 1][j + 1] == 1 and image[i + 1][j + 1] == 1) or(image[i + 1][j + 1] == 1 and image[i + 1][j - 1] == 1)\
    #                         or (image[i][j - 1] == 1 and image[i - 1][j] == 1) or (image[i - 1][j] == 1 and image[i][j + 1] == 1)\
    #                         or (image[i][j + 1] == 1 and image[i + 1][j] == 1) or (image[i + 1][j] == 1 and image[i][j - 1] == 1):
    #                     angle[i][j] = 90
    #                     print("90gggggggggfffffff")
    #                     continue
    #                 if (image[i - 1][j - 1] == 1 and image[i + 1][j + 1] == 1) or (image[i - 1][j + 1] == 1 and image[i + 1][j - 1] == 1)\
    #                         or (image[i - 1][j] == 1 and image[i + 1][j] == 1) or (image[i][j - 1] == 1 and  image[i][j + 1] == 1):
    #                     angle[i][j] = 0
    #                     print("0")
    #                     continue
    #                 if (image[i - 1][j - 1] == 1 and image[i][j - 1] == 1) or (image[i - 1][j - 1] == 1 and image[i - 1][j] == 1)\
    #                         or (image[i - 1][j ] == 1 and image[i - 1][j + 1] == 1) or (image[i - 1][j + 1] == 1 and image[i][j + 1] == 1)\
    #                         or (image[i][j + 1] == 1 and image[i + 1][j + 1] == 1) or (image[i + 1][j + 1] == 1 and image[i + 1][j ] == 1)\
    #                         or (image[i + 1][j] == 1 and image[i + 1][j - 1] == 1) or (image[i + 1][j - 1] == 1 and image[i][j - 1] == 1):
    #                     angle[i][j] = 45
    #                     print("kkkkkkkkkkkkkkkkkkkkkkkkk45")
    #                     continue
    #                 angle[i][j] = 135
    #                 print("135end")
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if (image[i][j] == 1):
                count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                        image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
                if (count == 1):
                    angle[i][j] = 1
    pointxx, pointyy = [], []
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if (angle[i][j] != 0):
                pointxx.append(j)
                pointyy.append(i)

    return pointx, pointy, pointxx, pointyy, angle + tem

def judge_point_in_base_segmentation(pointx,pointy,up_segmentation,down_segmentation):
    for i in range(len(uper_segment)):
        if(pointx == up_segmentation[i][0] and pointy == up_segmentation[i][1]) or (pointx == down_segmentation[i][0] and pointy == down_segmentation[i][1]):
            return True
    return False

def check_point(pointx,pointy,totalpointx):
    for i in range(len(totalpointx)):
        if(pointx == totalpointx[i][0] and pointy == totalpointx[i][1]):
            return True
    return False
def upget_next_feature_point(image,prox,proy,pointx,pointy,temlist,only_point):
    global totalpoint
    [row,col] = image.shape
    [i,j] = pointx,pointy
    if(image[i][j] == 1 and i - 1 > -1 and j - 1 > -1 and i + 1 < row and j + 1 < col):
        count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
        if (count == 0 or check_point(pointx,pointy,only_point)):
            return
        only_point.append([i,j])
        temlist.append([i, j])
        if (count == 1 and (len(temlist) > 2 )):
            print("到达终点")
            if(len(temlist) > 2):
                # print(temlist)
                t = []
                t.extend(temlist)
                print(t)
                totalpoint.append(t)
            # print(temlist)
            temlist.pop(-1)
            return

        if (not(prox == i - 1 and proy == j - 1)) and image[i - 1][j - 1] == 1:
            upget_next_feature_point(image,i, j, i - 1, j - 1,temlist,only_point)


        if (not(prox == i + 1 and proy == j - 1)) and image[i + 1][j - 1] == 1:
            upget_next_feature_point(image, i, j,i + 1, j - 1, temlist,only_point)


        if (not(prox == i - 1 and proy == j + 1)) and image[i - 1][j + 1] == 1:
            upget_next_feature_point(image, i, j, i - 1, j + 1, temlist,only_point)

        if (not(prox == i and proy == j - 1)) and image[i][j - 1] == 1:
            upget_next_feature_point(image, i, j,  i, j - 1, temlist,only_point)

        if (not(prox == i - 1 and proy == j)) and image[i - 1][j] == 1:
            upget_next_feature_point(image, i, j, i - 1, j, temlist,only_point)

        if (not(prox == i and proy == j + 1)) and image[i][j + 1] == 1:
            upget_next_feature_point(image, i, j, i, j + 1, temlist,only_point)

        if (not(prox == i + 1 and proy == j + 1)) and image[i + 1][j + 1] == 1:
            upget_next_feature_point(image,i, j,  i + 1, j + 1, temlist,only_point)

        if (not (prox == i + 1 and proy == j)) and image[i + 1][j] == 1:
                upget_next_feature_point(image, i, j, i + 1, j, temlist, only_point)
        temlist.pop(-1)


if __name__ == '__main__':

    s = [['False', 'True'], ['False', 'False']]
    # pointx = []
    # pointy = []
    # pointx.append(10)
    # pointy.append(10)
    # pointx.append(20)
    # pointy.append(20)
    # p2 = plt.subplot(212)
    # # p2.imshow(image,cmap = "gray")
    # p2.plot(pointx, pointy, 'r*-')
    # plt.show()
    image = io.imread("D:\藏文识别\相关文献\data\Sticky_text\ chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0007_1_015.png")
    # vertical = np.sum(image,axis=0)
    # print(image.shape)
    # print(vertical)
    # print(min(image))
    # image = io.imread('C:\\Users\Zqc\Desktop\\ttt.bmp',as_grey='true')
    row, col = image.shape
    # filter_image = np.zeros(row * col)
    # filter_image = filter_image.reshape(row, col)
    # pattern = re.compile(r'Hello[\w]*?')
    # match = pattern.match('Hello World !')
    # m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
    # m = re.match(r'(\d)abc(?P<ddddd>.{1})','1abc!1')
    # image = image.astype(int)
    # image = np.where(image > 0.9, 1, 0)
    # p1 = plt.subplot(211)
    # p1.imshow(image, cmap="gray")
    # image = get_fileter_image(image)
    #
    # edgs = feature.canny(image, sigma=2, low_threshold=5, high_threshold=10)
    # chull = morphology.convex_hull_object(edgs)
    # p2 = plt.subplot(212)
    # p2.imshow(chull, cmap='gray')
    #
    # pointx = [6, 6, 6, 6, 6, 6, 6, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    # pointy = [0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    #
    # tempx, tempy = get_min_point(image, 22, 7, 7)
    # print(pointx.index(tempx), "value = ", pointx[pointx.index(tempx)])
    # for i in range(1, len(pointx)):
    #     if (pointx[len(pointx) - i] == tempx):
    #         count = len(pointx) - i;
    #         print(count)
    #     print('count:', count)
    #
    # pointx = pointx[:count + 1]
    # pointy = pointy[:count + 1]
    # pointx.append(tempx)
    #
    # pointy.append(tempy)
    # print(str(tempx) + " " + str(tempy))
    # p2.plot(pointx, pointy, 'r.-')
    # plt.show()
    #
    # pointx = [18, 18, 19, 20, 20, 20, 20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 21, 22]
    # pointy = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 22]
    # # print(get_min_index_rol(pointx,pointy))
    # print(len(np.array(pointx)))
    # image = io.imread('C:\\Users\Zqc\Desktop\\test.tif',as_grey='true')
    # image = np.where(image > 0.9, 1, 0)
    #
    # p1 = plt.subplot(211)
    # p1.imshow(image, cmap="gray")
    #
    # ad_image = adjunction_image(image)
    # p2 = plt.subplot(212)
    # p2.imshow(ad_image, cmap="gray")
    #
    # print(image.shape)
    # print(ad_image.shape)
    # plt.show()
    image_origin = io.imread("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_292.png", as_grey=True)


    image = io.imread("skeleton1.png",as_grey = True)
    image = np.where(image > 0, 1,0)
    image = adjunction_image(image)



    pointx, pointy, anglex, angley, point_image = get_fork_point(image)

    p1 = plt.subplot(231)
    p1.imshow(image_origin, cmap='gray')

    point_image = corner_peaks(corner_fast(image_origin,9),min_distance = 1 )
    p2 = plt.subplot(232)
    p2.plot(point_image[:,1], point_image[:,0],"r.")
    p2.imshow(image_origin)

    p3 = plt.subplot(233)
    p3.imshow(image, cmap = "gray")
    p3.plot(pointx,pointy,"r.")
    p3.plot(anglex,angley,"b.")
    print(image.shape)

    lb_image = measure.label(image,neighbors = 8)
    regions = measure.regionprops(lb_image)
    p4 = plt.subplot(234)
    p4.imshow(np.where(lb_image > 0,1, 0),cmap = "gray")


    for region in regions:
        point = region.coords
        print("fffffffff",point)

    # p3 = plt.subplot(224)
    #  st = corner_peaks(corner_harris(image), min_distance=1)
    # p3.plot(pointx, pointy, "r.")
    # p3.imshow(image,cmap = "gray")
    # p3.plot(st[ : , 1], st[ : , 0],"b.")
    # # plt.scatter(st[:,1],st[:,0])
    [uper_segment,down_segment] = [],[]
    [row, col] = image.shape

    for j in range(1,col - 1,1):
        for i in range(0,row - 1,1):
            if(image[i][j] == 1):
                uper_segment.append([i,j])
                break
        for i in range(row - 1,1,-1):
            if(image[i][j] == 1):
                down_segment.append([i,j])
                break
    print(len(uper_segment),len(down_segment))
    uper_segment = np.array(uper_segment)
    down_segment = np.array(down_segment)
    # p4.plot(uper_segment[:,1],uper_segment[:,0],"r.")
    # p4.plot(down_segment[:,1],down_segment[:,0],"r.")
    # print((uper_segment), (down_segment))
    print(judge_point_in_base_segmentation(2,15,uper_segment,down_segment),"ffsdfgdfgdfgdfgdfg")
    print(judge_point_in_base_segmentation(46,51, uper_segment, down_segment))
    print(judge_point_in_base_segmentation(25, 15, uper_segment, down_segment))

    [tem, only_point] = [], []
    upget_next_feature_point(image, 3, 13, 3, 14, tem, only_point)
    # upget_next_feature_point(image,24,35,25,35,tem,only_point)
    print(len(totalpoint))
    print("最后的值：",totalpoint)
    point = totalpoint[2]
    point = np.array(point)
    p4.plot(point[:,1],point[:,0],"r.-")
    # totalpoint[0] = totalpoint[0] +[[25, 35], [26, 35], [27, 35], [28, 36], [29, 36], [30, 37], [31, 37], [32, 38], [33, 39], [33, 40], [34, 41], [35,42], [36, 43], [36, 44], [37, 45], [37, 46], [38, 47], [39, 48], [38, 49], [37, 50], [36, 51], [35, 52]]
    p5= plt.subplot(235)
    p5.imshow(np.where(lb_image > 0, 1, 0), cmap="gray")
    point = totalpoint[1]
    point = np.array(point)
    p5.plot(point[:, 1], point[:, 0], "r.-")
    ########藏文历史文献中黏连字丁串的切分与识别########


    p6 = plt.subplot(236)
    point = totalpoint[0]
    point = np.array(point)
    p6.plot(point[:, 1], point[:, 0], "r.-")
    p6.imshow(np.where(lb_image > 0, 1, 0), cmap="gray")

    plt.show()