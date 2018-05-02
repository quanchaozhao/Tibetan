# =_= coding:utf-8 =_=

import matplotlib.pyplot as plt
import numpy as np
from skimage import io, measure, color
from skimage.morphology import skeletonize, thin,skeletonize_3d
from skimage.filters import roberts, sobel, scharr, prewitt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

def adjunction_image(image):
    row, col = image.shape
    ad_image = np.zeros((row + 2, col + 2))
    for i in range(row):
        for j in range(col):
            ad_image[i + 1][j + 1] = image[i][j]
    return ad_image


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


def get0_1(image):
    cow, rol = image.shape
    for i in range(cow):
        for j in range(rol):
            if (image[i][j] == 'False'):
                image[i][j] = 1
            else:
                image[i][j] = 0
    return image


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


if __name__ == '__main__':
    image_origin = io.imread(
        "D:\藏文识别\相关文献\data\Sticky_text\ chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0004_0_113.png",
        as_grey=True)
    image_origin = io.imread("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_292.png", as_grey=True)
    # image_origin = io.imread('t.bmp',as_grey = True)
    image_origin = np.where(image_origin > 0, 1, 0)
    image_origin = adjunction_image(image_origin)
    # 骨架
    skeleton = skeletonize(image_origin)
    # image = get_fileter_image(image_origin)
    image = image_origin
    # 细化
    thinned = thin(image)

    # 边缘
    edge_scharr = scharr(image)
    pointx, pointy = [], []
    row, col = edge_scharr.shape
    edge_scharr = np.where(edge_scharr > 0, 1, 0)
    for i in range(row):
        for j in range(col):
            if (edge_scharr[i][j] == 1):
                pointx.append(j)
                pointy.append(i)
    # ax2 = plt.subplot(234)
    # ax2.set_title("scharr")
    # ax2.imshow(image_origin, cmap='gray')

    # ax2.plot(pointx, pointy, 'm.')

    # 边缘
    edge_roberts = roberts(image)
    pointx, pointy = [], []
    row, col = edge_roberts.shape
    edge_roberts = np.where(edge_roberts > 0, 1, 0)
    for i in range(row):
        for j in range(col):
            if (edge_roberts[i][j] == 1):
                pointx.append(j)
                pointy.append(i)
    # ax3 = plt.subplot(235)
    # ax3.imshow(image_origin, cmap='gray')
    # ax3.set_title("robert")
    # ax3.plot(pointx, pointy, 'g.')


    back_image = np.where(image_origin > 0, 0, 1)
    pro_thin_image = skeletonize(image_origin)
    back_thin_images = skeletonize(back_image)
    back_thin_image = np.zeros((row, col))
    back_thin_image[:, int(col / 5):int(col / 5) * 4] = back_thin_images[:, int(col / 5):int(col / 5) * 4]
    total_image = edge_roberts
    p1 = plt.subplot(221)
    pointX, pointY, countX, countY,point_image = get_fork_point(total_image)
    p1.imshow(total_image, cmap="gray")
    p1.set_title("粘连字丁串前景轮廓")
    p1.axis("off")
    # p1.plot(pointX, pointY, "r.")

    total_image = np.where(back_thin_image > 0,2,0) + pro_thin_image
    p2 = plt.subplot(222)
    p2.set_title("粘连字丁串前景与背景骨架")
    p2.axis("off")
    p2.imshow(total_image)

    io.imsave("skeleton1.png", total_image, cmap="gray")

    edge_roberts = np.where(edge_roberts > 0, 6, 0)
    total_image = edge_roberts + np.where(back_thin_image > 0,30,0)
    p3 = plt.subplot(224)
    pointX, pointY, countX, countY, point_image= get_fork_point(back_thin_image)
    p3.imshow(total_image)
    p3.plot(pointX, pointY, "r.")
    p3.plot(countX, countY, "w.")
    p3.set_title("粘连字丁串信息及特征点")



    p4 = plt.subplot(223)
    p4.imshow(point_image + back_thin_image)
    p4.set_title("粘连字丁串背景骨架特征点")
    plt.show()
