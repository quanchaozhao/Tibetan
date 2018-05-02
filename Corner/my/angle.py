# coding:utf-8

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io
from pic_process.utils import fill_image as fill_image
img = cv2.imread("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_292.png")
from skimage.transform import probabilistic_hough_line
from matplotlib import cm
def adjunction_image(image):
    row, col = image.shape
    ad_image = np.zeros((row + 6, col + 6))
    for i in range(row):
        for j in range(col):
            ad_image[i + 3][j + 3] = image[i][j]
    return ad_image
def get_fileter_image(image):
    row, col = image.shape
    filter_image = image[:]
    # 行消除锯齿
    for i in range(row):
        for j in range(2, col - 2):
            if (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 1) or \
                    (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][j + 2] == 1) or \
                    (image[i][j - 2] == 1 and image[i][j - 1] == 0 and image[i][j] == 0 and image[i][j - 1] == 1):
                filter_image[i][j] = 1
            # if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0) or (
            #                         image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 and image[i][
            #                 j + 2] == 0):
            #     filter_image[i][j] = 0
    # # 列消除锯齿
    for i in range(col):
        for j in range(2, row - 2):
            if(image[j - 1][i] == 1 and image[j][i] == 0 and image[j + 1][i] == 1) or \
                    (image[j - 1][i] == 1 and image[j][i] == 0 and image[j + 1][i] == 0 and image[j + 2][i] == 1) or \
                    (image[j - 2][i] == 1 and image[j - 1][i] == 0 and image[j][i] == 0 and image[j - 1][i] == 1):
                filter_image[j][i] = 1;

    return filter_image
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
            if (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 1) or \
                    (image[j - 1][i] == 1 and image[j][i] == 1 and image[j + 1][i] == 0) or \
                    (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 0):
                image_copy[j][i] = 1
    return image_copy
# imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# imgGray = np.float32(imgGray)
def alter_point(image,pointx,pointy):
    if(image[pointx - 1][pointy]):
        return pointx - 1,pointy
    if (image[pointx + 1][pointy]):
        return pointx + 1, pointy
    if (image[pointx][pointy -1]):
        return pointx, pointy - 1
    if (image[pointx][pointy + 1]):
        return pointx, pointy + 1

    if (image[pointx - 1][pointy - 1]):
        return pointx - 1, pointy -1
    if (image[pointx - 1][pointy + 1]):
        return pointx - 1, pointy + 1
    if (image[pointx + 1][pointy + 1]):
        return pointx + 1, pointy + 1
    if (image[pointx + 1][pointy - 1]):
        return pointx + 1, pointy - 1
    if (image[pointx - 2][pointy]):
        return pointx - 2, pointy
    if (image[pointx + 2][pointy]):
        return pointx + 2, pointy
    if (image[pointx][pointy - 2]):
        return pointx, pointy - 2
    if (image[pointx][pointy + 2]):
        return pointx, pointy + 2

    if (image[pointx - 2][pointy - 2]):
        return pointx - 2, pointy - 2
    if (image[pointx - 2][pointy + 2]):
        return pointx - 2, pointy + 2
    if (image[pointx + 2][pointy + 2]):
        return pointx + 2, pointy + 2
    if (image[pointx + 2][pointy - 2]):
        return pointx + 2, pointy - 2
def total_point(image, pointx, pointy):
    return image[pointx][pointy - 1] + \
    image[pointx][pointy + 1] + \
    image[pointx - 1][pointy] + \
    image[pointx + 1][pointy] + \
    image[pointx - 1][pointy - 1] + \
    image[pointx - 1][pointy + 1] + \
    image[pointx + 1][pointy - 1] + \
    image[pointx + 1][pointy + 1]
def alter_index_points(image,index):
    row,col = image.shape
    pointx = []
    pointy = []
    for i in range(1,col - 1,1):
       cout = image[index][i - 1] + \
              image[index][i + 1] + \
              image[index - 1][i] + \
              image[index + 1][i] + \
              image[index - 1][i - 1] + \
              image[index - 1][i + 1] + \
              image[index + 1][i - 1] + \
              image[index + 1][i + 1]
       if(cout > 4):
           pointx.append(index)
           pointy.append(i)
           # image[index][i] = 1
    return pointy,pointx
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

            if(len(temlist) > 2):
                # print(temlist)
                t = []
                t.extend(temlist)
                print("到达终点", len(t))
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
def del_T_type(image):
    row,col = image.shape

    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if image[i][j] == 1:
                # 修正T型
                if( image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 0
                     and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 0 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                    image[i][j - 1] = 0
    #             修正拐角 12,13,14,23,24,34
                if (image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 0 and image[i + 1][j] == 0
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                # if (image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i][j + 1] == 1 and image[i + 1][j] == 0
                #         and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                #         image[i + 1][j - 1] == 0):
                #     image[i][j] = 0
                if (image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i][j + 1] == 0 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                if (image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 0
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
                # if (image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i][j + 1] == 0 and image[i + 1][j] == 1
                #         and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                #         image[i + 1][j - 1] == 0):
                #     image[i][j] = 0
                if (image[i][j - 1] == 0 and image[i - 1][j] == 0 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):
                    image[i][j] = 0
    return image

def find_extreme_point(image,index):
    row,col = image.shape
    print(row,col)
    for i in range(col):
        if image[index][i] == 1:
            left_top = [index,i]
            image[index][i] = 0
            image[index][i - 1] = 0
            image[index + 1][i] = 0
            image[index + 1][i - 1] = 0
            break
    for i in range(col - 1, -1, -1):
        if image[index][i] == 1:
            right_top = [index,i]
            image[index][i] = 0
            image[index][i + 1] = 0
            image[index + 1][i] = 0
            image[index + 1][i + 1] = 0
            break
    flag = True
    for i in range(col):
        for j in range(row - 1, -1, -1):
            if image[j][i] == 1 and not(j == left_top[0] and i == left_top[1]) and flag:
                left_below1 = [j,i]

                flag = False
    flag = True
    for i in range(row - 1, -1, -1):
        for j in range(col):
            if image[i][j] == 1 and not (i == left_top[0] and j == left_top[1]) and flag:
                left_below2 = [i, j]

                flag = False
    if ((row - left_below1[0]) * (row - left_below1[0]) + (left_below1[1]) * (- left_below1[1]) >
            (row - left_below2[0]) * (row - left_below2[0]) + (left_below2[1]) * (left_below2[1])):
        left_below = left_below2
    else:
        left_below = left_below1


    flag = True
    for i in range(row - 1, -1, -1):
        for j in range(col - 1, -1, -1):
            if image[i][j] == 1 and not(i == right_top[0] and j == right_top[1]) and flag:
                right_below1 = [i, j]

                flag = False
    flag = True
    for i in range(col - 1, -1, -1):
        for j in range(row - 1, -1, -1):
            if image[j][i] == 1 and not(j == right_top[0] and i == right_top[1]) and flag:
                right_below2 = [j,i]
                flag = False
    if( (row - right_below1[0]) * (row - right_below1[0]) + (col - right_below1[1]) *  (col - right_below1[1]) >
            (row - right_below2[0]) * (row - right_below2[0]) + (col - right_below2[1]) * (col - right_below2[1]) ):
        right_below = right_below2
    else:
        right_below = right_below1
    # image[right_below[0]][right_below[1]] = 0
    return image, left_top, right_top, left_below, right_below

def show_point(file):
    global totalpoint
    img = io.imread(file, as_grey = True)
    plt.subplot(111).imshow(img)
    plt.show()
    p2 = plt.subplot(211)
    tt = (get_outline(fill_image(del_T_type(get_fileter_image(adjunction_image(np.where(img/255 > 0.9,1,0) ))))))
    p2.imshow(fill_image(get_fileter_image(adjunction_image(np.where(img/255 > 0.9,1,0) ))))

    # print(corners)
    p1 = plt.subplot(212)

    # plt.show()
    row, col = tt.shape
    # get_line(tt)
    horizontal_projection = np.sum(tt, axis=1)
    # print(horizontal_projection)
    index = np.where(horizontal_projection == np.max(horizontal_projection))[0][0]
    print('基线位置： ', index)
    p1.plot([1,col - 1],[index,index])

    pointx,pointy = [],[]
    corners = cv2.goodFeaturesToTrack((tt).astype(np.uint8), 1000, 0.4, 7)

    corners = np.int0(corners)
    for item in corners:
        x, y = item.ravel()
        # cv2.circle(img, (x, y), 3, [0, 255, 255], -1)
        if(tt[y][x] == 0):
            y,x = alter_point(tt,y,x)
        if(abs(y - index) < 8 and not(total_point(tt, y, x) > 3)) or (y < index):
            continue
        pointx.append(x)
        pointy.append(y)
    alter_pointx, alter_pointy = alter_index_points(tt, index)
    pointx = pointx + alter_pointx
    pointy = pointy + alter_pointy
    p1.plot(pointx,pointy,"r.")
    tt = tt.astype(np.uint8)
    io.imsave('tt.png', tt * 255)
    tt_new, point1, point2, point3, point4 = find_extreme_point(tt,index)
    p1.imshow(tt_new, cmap="gray")
    p1.plot([point1[1]],[point1[0]], 'g.')
    p1.plot([point2[1]], [point2[0]], 'g.')
    p1.plot([point3[1]], [point3[0]], 'y.')
    p1.plot([point4[1]], [point4[0]], 'y.')
    print([point1[1]], [point1[0]], 'g.')
    print([point2[1]], [point2[0]], 'k.')
    print([point3[1]], [point3[0]], 'y.')
    print([point4[1]], [point4[0]], 'y.')
    plt.show()
    tem, only_point = [], []
    upget_next_feature_point(tt_new, point1[0], point1[1], point1[0], point1[1] + 1, tem, only_point)
    k = len(totalpoint)
    print('total path: ', k)
    if k % 2 == 1:
        for i in range(k):
            point = totalpoint[i]
            point = np.array(point)
            pt = plt.subplot(2, int(k / 2 + 1), i + 1)
            pt.imshow(tt_new)
            x, y = point[:, 1], point[:, 0]
            pt.plot(x, y, str(label[i]))
    else:
        for i in range(k):
            point = totalpoint[i]
            point = np.array(point)
            pt = plt.subplot(2, int(k / 2 ), i + 1)
            pt.imshow(tt_new)
            x, y = point[:, 1], point[:, 0]
            pt.plot(x, y, str(label[i]))
    totalpoint = []
    plt.show()
    upget_next_feature_point(tt_new, point3[0], point3[1], point3[0], point3[1] + 1, tem, only_point)
    k = len(totalpoint)
    print('total path: ', k)
    if k % 2 == 1:
        for i in range(k):
            point = totalpoint[i]
            point = np.array(point)
            pt = plt.subplot(2, int(k / 2 + 1), i + 1)
            pt.imshow(tt_new)
            x, y = point[:, 1], point[:, 0]
            pt.plot(x, y, str(label[i]))
    else:
        for i in range(k):
            point = totalpoint[i]
            point = np.array(point)
            pt = plt.subplot(2, int(k / 2), i + 1)
            pt.imshow(tt_new)
            x, y = point[:, 1], point[:, 0]
            pt.plot(x, y, str(label[i]))
    totalpoint = []
    plt.show()

def get_line(image):

    lines = probabilistic_hough_line(image, threshold=10, line_length=10,
                                     line_gap=3)
    # Generating figure 2
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(image, cmap=cm.gray)
    ax[0].set_title('Input image')

    ax[1].imshow(image, cmap=cm.gray)
    ax[1].set_title('Canny edges')

    ax[2].imshow(image * 0)
    # ax[2].plot((lines[0][0][0], lines[0][1][0]), (lines[0][0][1], lines[0][1][1]),'r')
    x,y = (lines[0][0][0], lines[0][1][0]), (lines[0][0][1], lines[0][1][1])
    radio = 90
    for line in lines:
        p0, p1 = line
        ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
        if (p1[1] == p0[1]):
            x, y = (p0[0], p1[0]), (p0[1], p1[1])
            break
        tem = abs(abs( abs((p1[0] - p0[0])) / (p1[1] - p0[1])))
        if(tem < radio):
            radio = tem
            x, y = (p0[0], p1[0]), (p0[1], p1[1])
    ax[2].plot(x, y,'w')
    ax[2].set_xlim((0, image.shape[1]))
    ax[2].set_ylim((image.shape[0], 0))
    ax[2].set_title('Probabilistic Hough')

    for a in ax:
        a.set_axis_off()
        a.set_adjustable('box-forced')

    plt.tight_layout()
    plt.show()
# cv2.imshow('Corner', img)
# cv2.waitKey(0)
# cv2.destroyWindows()
path = r'./Test_Img'
totalpoint = []
label = ["g.-", "b.-", "r.-", "k.-", "w.-","c.-"]
for i in os.listdir(path):
    if i.endswith('.png'):
        # i = "chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0046_0_517.png"
        file = os.path.join(path,i)
        print(file)
        # show_point(r"./Test_Img/chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-10-0560_0_475.png")
        show_point(file)