# coding:utf-8

import copy
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage import measure
from skimage.morphology import skeletonize

from class_character.SVM_predict import get_class_and_ratio as get_class_and_ratio
from pic_process.utils import fill_image as fill_image

img = cv2.imread("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_292.png")
from skimage.transform import probabilistic_hough_line
from matplotlib import cm


def adjunction_image(image):
    # row, col = image.shape
    # ad_image = np.zeros((row + 6, col + 6))
    # for i in range(row):
    #     for j in range(col):
    #         ad_image[i + 3][j + 3] = image[i][j]
    return image


def get_fileter_image(image):
    row, col = image.shape
    filter_image = np.zeros((row, col))
    # # 列消除锯齿
    for i in range(col):
        for j in range(2, row - 2):
            # if (image[j - 1][i] == 1 and image[j][i] == 0 and image[j + 1][i] == 1):
            #         # or (image[j - 1][i] == 1 and image[j][i] == 0 and image[j + 1][i] == 0 and image[j + 2][i] == 1) or \
            #         # (image[j - 2][i] == 1 and image[j - 1][i] == 0 and image[j][i] == 0 and image[j - 1][i] == 1):
            #     filter_image[j][i] = 1;
            #     continue
            # if (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 0):
            #     filter_image[j][i] = 0;
            #     continue
            filter_image[j][i] = image[j][i]
    image = filter_image
    # 行消除锯齿
    for i in range(row):
        for j in range(2, col - 2):
            if (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 1):
                # or (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][j + 2] == 1) or \
                # (image[i][j - 2] == 1 and image[i][j - 1] == 0 and image[i][j] == 0 and image[i][j - 1] == 1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0):
                # or ( image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 and image[i][
                #         j + 2] == 0):
                filter_image[i][j] = 0

    return filter_image


def get_outline(image):
    rows, cols = image.shape
    image_copy = np.zeros((rows, cols))
    for i in range(1, rows - 2, 1):
        for j in range(1, cols - 2, 1):
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1) or \
                    (image[i][j - 1] == 1 and image[i][j] == 1 and image[i][j + 1] == 0) or \
                    (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 0):
                image_copy[i][j] = 1
    for i in range(1, cols - 2, 1):
        for j in range(1, rows - 2, 1):
            if (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 1) or \
                    (image[j - 1][i] == 1 and image[j][i] == 1 and image[j + 1][i] == 0) or \
                    (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 0):
                image_copy[j][i] = 1
    # edge_scharr = roberts(image)
    # edge_scharr = np.where(edge_scharr > 0.6, 1, 0)
    # plt.subplot(111).imshow(edge_scharr)
    # plt.show()
    return image_copy


# imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# imgGray = np.float32(imgGray)
def collect_up_point(image, prox, proy, pointx, pointy, temlist, only_point):
    pass


def alter_point(image, pointx, pointy):
    if (image[pointx - 1][pointy]):
        return pointx - 1, pointy
    if (image[pointx + 1][pointy]):
        return pointx + 1, pointy
    if (image[pointx][pointy - 1]):
        return pointx, pointy - 1
    if (image[pointx][pointy + 1]):
        return pointx, pointy + 1

    if (image[pointx - 1][pointy - 1]):
        return pointx - 1, pointy - 1
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
    if (image[pointx - 3][pointy]):
        return pointx - 3, pointy
    if (image[pointx + 3][pointy]):
        return pointx + 3, pointy
    if (image[pointx][pointy - 3]):
        return pointx, pointy - 3
    if (image[pointx][pointy + 3]):
        return pointx, pointy + 3

    if (image[pointx - 3][pointy - 3]):
        return pointx - 3, pointy - 3
    if (image[pointx - 3][pointy + 3]):
        return pointx - 3, pointy + 3
    if (image[pointx + 3][pointy + 3]):
        return pointx + 3, pointy + 3
    if (image[pointx + 3][pointy - 3]):
        return pointx + 3, pointy - 3


def total_point(image, pointx, pointy):
    return image[pointx][pointy - 1] + \
           image[pointx][pointy + 1] + \
           image[pointx - 1][pointy] + \
           image[pointx + 1][pointy] + \
           image[pointx - 1][pointy - 1] + \
           image[pointx - 1][pointy + 1] + \
           image[pointx + 1][pointy - 1] + \
           image[pointx + 1][pointy + 1]


def alter_index_points(image, index):
    row, col = image.shape
    pointx = []
    pointy = []
    if col < 100:
        start = int(col / 3 + 0.5 + 2)
        end = int(col / 3 * 2 + 0.5 - 2)
    else:
        start = int(col / 3 + 0.5 + 2)
        end = int(col / 4 * 3 + 0.5 - 2)
    for i in range(start - 1, end + 1, 1):
        cout = image[index][i - 1] + \
               image[index][i + 1] + \
               image[index - 1][i] + \
               image[index + 1][i] + \
               image[index - 1][i - 1] + \
               image[index - 1][i + 1] + \
               image[index + 1][i - 1] + \
               image[index + 1][i + 1]
        if (cout > 4 and image[index][i] == 1 and i):
            pointx.append(index)
            pointy.append(i)
            # image[index][i] = 1
    return pointy, pointx


def check_point(pointx, pointy, totalpointx):
    for i in range(len(totalpointx)):
        if (pointx == totalpointx[i][0] and pointy == totalpointx[i][1]):
            return True
    return False


def upget_next_feature_point(image, prox, proy, pointx, pointy, temlist, only_point):
    global totalpoint
    [row, col] = image.shape
    [i, j] = pointx, pointy
    if (image[i][j] == 1 and i - 1 > -1 and j - 1 > -1 and i + 1 < row and j + 1 < col):
        count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
        if (count == 0 or check_point(pointx, pointy, only_point)):
            return
        only_point.append([i, j])
        temlist.append([i, j])
        if (count == 1 and (len(temlist) > 2)):

            if (len(temlist) > 2):
                # print(temlist)
                t = []
                t.extend(temlist)
                print("到达终点", len(t))
                totalpoint.append(t)
            # print(temlist)
            temlist.pop(-1)
            return

        if (not (prox == i - 1 and proy == j - 1)) and image[i - 1][j - 1] == 1:
            upget_next_feature_point(image, i, j, i - 1, j - 1, temlist, only_point)

        if (not (prox == i + 1 and proy == j - 1)) and image[i + 1][j - 1] == 1:
            upget_next_feature_point(image, i, j, i + 1, j - 1, temlist, only_point)

        if (not (prox == i - 1 and proy == j + 1)) and image[i - 1][j + 1] == 1:
            upget_next_feature_point(image, i, j, i - 1, j + 1, temlist, only_point)

        if (not (prox == i and proy == j - 1)) and image[i][j - 1] == 1:
            upget_next_feature_point(image, i, j, i, j - 1, temlist, only_point)

        if (not (prox == i - 1 and proy == j)) and image[i - 1][j] == 1:
            upget_next_feature_point(image, i, j, i - 1, j, temlist, only_point)

        if (not (prox == i and proy == j + 1)) and image[i][j + 1] == 1:
            upget_next_feature_point(image, i, j, i, j + 1, temlist, only_point)

        if (not (prox == i + 1 and proy == j + 1)) and image[i + 1][j + 1] == 1:
            upget_next_feature_point(image, i, j, i + 1, j + 1, temlist, only_point)

        if (not (prox == i + 1 and proy == j)) and image[i + 1][j] == 1:
            upget_next_feature_point(image, i, j, i + 1, j, temlist, only_point)
        temlist.pop(-1)


def del_T_type(image):
    row, col = image.shape

    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if image[i][j] == 1:
                # 修正T型

                if (image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 0
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):  # 1
                    image[i][j] = 0  # 1 1 1
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 0 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):  # 1
                    image[i][j] = 0  # 1 1
                    image[i + 1][j] = 0  # 1
                if (image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):  # 1 1 1
                    image[i][j] = 0  # 1
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):  # 1
                    image[i][j] = 0  # 1 1
                    image[i + 1][j] = 0  # 1
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
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if image[i][j] == 1:
                count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                        image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
                if (count <= 1):
                    image[i][j] = 0
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if image[i][j] == 1:
                count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                        image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
                if (count <= 1):
                    image[i][j] = 0
    return image


def end_point(image):
    row, col = image.shape;
    image = image * 1
    pointx, pointy = [], []
    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if (image[i][j] == 1):
                count = image[i - 1][j - 1] + image[i + 1][j - 1] + image[i - 1][j + 1] + image[i + 1][j + 1] + \
                        image[i][j - 1] + image[i - 1][j] + image[i + 1][j] + image[i][j + 1]
                if (count == 1):
                    pointx.append(i)
                    pointy.append(j)
            # else:
            #     if (image[i - 1][j - 1] == 0 and image[i + 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and \
            #     image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i + 1][j] == 0 and image[i][j + 1] == 0) \
            #         or (image[i - 1][j - 1] == 0 and image[i + 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and \
            #     image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i + 1][j] == 1 and image[i][j + 1] == 0) \
            #         or (image[i - 1][j - 1] == 0 and image[i + 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and \
            #     image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i + 1][j] == 0 and image[i][j + 1] == 1) \
            #         or (image[i - 1][j - 1] == 0 and image[i + 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and \
            #     image[i][j - 1] == 0 and image[i - 1][j] == 0 and image[i + 1][j] == 1 and image[i][j + 1] == 1):
            #         pointx.append(i)
            #         pointy.append(j)

    return pointx, pointy


def find_extreme_point(image, index):
    row, col = image.shape
    print(row, col)
    for i in range(col):
        if image[index][i] == 1:
            left_top = [index, i]
            image[index][i] = 0
            image[index][i - 1] = 0
            image[index + 1][i] = 0
            image[index + 1][i - 1] = 0
            break
    for i in range(col - 1, -1, -1):
        if image[index][i] == 1:
            right_top = [index, i]
            image[index][i] = 0
            image[index][i + 1] = 0
            image[index + 1][i] = 0
            image[index + 1][i + 1] = 0
            break
    flag = True
    for i in range(col):
        for j in range(row - 1, -1, -1):
            if image[j][i] == 1 and not (j == left_top[0] and i == left_top[1]) and flag:
                left_below1 = [j, i]

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
            if image[i][j] == 1 and not (i == right_top[0] and j == right_top[1]) and flag:
                right_below1 = [i, j]

                flag = False
    flag = True
    for i in range(col - 1, -1, -1):
        for j in range(row - 1, -1, -1):
            if image[j][i] == 1 and not (j == right_top[0] and i == right_top[1]) and flag:
                right_below2 = [j, i]
                flag = False
    if ((row - right_below1[0]) * (row - right_below1[0]) + (col - right_below1[1]) * (col - right_below1[1]) >
            (row - right_below2[0]) * (row - right_below2[0]) + (col - right_below2[1]) * (col - right_below2[1])):
        right_below = right_below2
    else:
        right_below = right_below1
    # image[right_below[0]][right_below[1]] = 0
    return image, left_top, right_top, left_below, right_below


def del_near_point(pointx, pointy):
    alter_pointx, alter_pointy = [], []
    print('pointx length: ', len(pointx))
    for i in range(len(pointx) - 1):
        flag = True
        for j in range(i + 1, len(pointx), 1):

            if (pointx[i] - pointx[j]) * (pointx[i] - pointx[j]) + (pointy[i] - pointy[j]) * (
                    pointy[i] - pointy[j]) < 9:
                flag = False
                break;
        if (flag):
            alter_pointx.append(pointx[i])
            alter_pointy.append(pointy[i])
    if (len(pointx) > 0):
        alter_pointx.append(pointx[-1])
        alter_pointy.append(pointy[-1])
    return alter_pointx, alter_pointy


def judge_vowel(image, index, vewol):
    row, col = image.shape
    new_vewol = []
    if (index > 10):
        image_vowel = image[0:index, :]
        for i in range(col):
            image[index][i] = 0
        lb_image = measure.label(image_vowel, connectivity=1)
        regions = measure.regionprops(lb_image)
        k = 1
        num = len(regions)
        for region in regions:
            if (region.area < 30):
                continue
            min_row, min_col, max_row, max_col = region.bbox
            if (max_col - min_col) / (max_row - min_row) > 2.5:
                for i in range(len(vewol)):
                    x, y = vewol[i][0], vewol[i][1]
                    print('x  y yyyyyyyyyyyy', x, y)
                    print(min_row, min_col, max_row, max_col)
                    print("Using SVM to predict...")
                    if (max_row - min_row < 6):
                        break
                    images = segmentation_image(region.image, x - min_col, y - min_row)
                    if (len(images) < 2):
                        break
                    image1 = images[0]
                    image2 = images[1]
                    print([x, y])
                    # plt.subplot(2, 2, 1).imshow(image1.astype(np.int8))
                    ratio1, classification = get_class_and_ratio(image1.astype(np.uint8) * 255)
                    print(1, ratio1, classification)
                    # plt.subplot(2, 2, 2).imshow(image2.astype(np.int8))
                    ratio2, classification = get_class_and_ratio(image2.astype(np.uint8) * 255)
                    print(2, ratio2, classification)
                    if (ratio1 > 0 and ratio2 > 0):
                        new_vewol.append([x, y])
    #     plt.subplot(212).imshow(image)
    #     plt.show()
    # else:
    #     plt.subplot(111).imshow(image)
    #     plt.show()
    # return False,image
    return new_vewol


def segmentation_image(image, pointx, pointy):
    print(pointx, pointy)

    # plt.subplot(111).imshow(image)
    image = image * 1
    row, col = image.shape
    print(row, col, "DDDDDDDDDDDD")
    if (pointx < 0 or pointy < 0 or pointx > col or pointy > row):
        return []
    # plt.show()
    # searching up
    for i in range(pointy - 1, -1, -1):
        if (image[i][pointx]) == 1:
            image[i][pointx] = 0
        else:
            break
    for i in range(pointy, row, 1):
        if (image[i][pointx]) == 1:
            image[i][pointx] = 0
    image_lab = measure.label(image, connectivity=1)
    regions = measure.regionprops(image_lab)
    images = []
    k = 1
    for region in regions:
        images.append(region.image)
    #     plt.subplot(2,1,k).imshow(region.image)
    #     k = k + 1
    # plt.show()
    return images


def show_point(file):
    global totalpoint
    img = io.imread(file, as_grey=True)
    tt = (get_outline(fill_image((get_fileter_image(adjunction_image(np.where(img / 255 > 0.9, 1, 0))))))).astype(
        np.uint8)
    img_filter = get_fileter_image(adjunction_image(np.where(img / 255 > 0.9, 1, 0)))
    fill_img = fill_image((get_fileter_image(adjunction_image(np.where(img / 255 > 0.9, 1, 0)))))
    skelenton_image = skeletonize(fill_img)
    end_pointx, end_pointy = end_point(skelenton_image)
    # plt.subplot(211).imshow(fill_img)
    # pp = plt.subplot(212)
    # pp.imshow(skelenton_image)
    # pp.plot(end_pointy, end_pointx, 'r.')
    # plt.show()

    # plt.show()
    row, col = tt.shape
    # get_line(tt)
    horizontal_projection = np.sum(tt[:int(col / 2), :], axis=1)
    horizontal_projection_t = horizontal_projection[4:-4]
    index_zero = np.where(horizontal_projection_t < 2)
    index = np.where(horizontal_projection == np.max(horizontal_projection))[0][0]
    if (len(index_zero[0]) != 0):
        print("change index position")
        index = index_zero[0][-1] + 4 + 2
    # print(horizontal_projection)
    print('基线位置： ', index)

    pointx, pointy = [], []
    vewol_point = []
    corners = cv2.goodFeaturesToTrack((tt).astype(np.uint8), 20, 0.2, 7)
    """
    1.8 skeleton
    water: 71.97

    outline:
    feature point 20,0.25,7 SVM 0.85  81.33 11859-5461
    feature point 20,0.30,7 SVM 0.85  79.72 11180-5353
    feature point 20,0.20,7 SVM 0.85  82.44 12751-5535
    feature point 20,0.20,7 SVM 0.85  82.23 12151-5521   alter-col

    1.4 skeleton
    water:  67.887

    the best result of outline:
    feature point 20,0.20,7 SVM 0.85  78.41 12151-5265   alter-col

    """

    # corners = np.int0(corners)
    # for item in corners:
    #     x, y = item.ravel()
    #     # cv2.circle(img, (x, y), 3, [0, 255, 255], -1)
    #     if (x <= int(col / 3 + 0.5 + 2) or x >= int(col / 3 * 2 + 0.5 - 2) and col < 100):
    #         continue
    #     if (x <= int(col / 3 + 0.5 + 2) or x >= int(col / 4 * 3 + 0.5 - 2) and col > 100):
    #         continue
    #     point_flag = True
    #     if (tt[y][x] == 0):
    #         y, x = alter_point(tt, y, x)
    #     vewol = 0
    #     for i in range(len(end_pointx)):
    #         if ((end_pointy[i] - x) * (end_pointy[i] - x) + (end_pointx[i] - y) * (end_pointx[i] - y) < 25) and (
    #                 abs(y - index) >= 3):
    #             point_flag = False
    #             break;
    #         elif (((end_pointy[i] - x) * (end_pointy[i] - x) + (end_pointx[i] - y) * (end_pointx[i] - y) > 25) and (
    #                 index - y >= 2)):
    #             vewol = vewol + 1
    #     if (len(end_pointx) == vewol):
    #         vewol_point.append([x, y])
    #     if (not point_flag):
    #         continue
    #     if (abs(y - index) < 3 and not (total_point(tt, y, x) > 3) or y < index):
    #         continue
    #
    #     pointx.append(x)
    #     pointy.append(y)
    #
    # alter_pointx, alter_pointy = alter_index_points(tt, index)
    # pointx = pointx + alter_pointx
    # pointy = pointy + alter_pointy
    # alter_pointx, alter_pointy = alter_index_points(tt, index + 1)
    # pointx = pointx + alter_pointx
    # pointy = pointy + alter_pointy
    # alter_pointx, alter_pointy = alter_index_points(tt, index + 2)
    # pointx = pointx + alter_pointx
    # pointy = pointy + alter_pointy
    # alter_pointx, alter_pointy = alter_index_points(tt, index + 3)
    # pointx = pointx + alter_pointx
    # pointy = pointy + alter_pointy
    #
    # pointx, pointy = del_near_point(pointx, pointy)
    # if (len(pointx) == 0):
    #     print("MDZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    #     for item in corners:
    #         x, y = item.ravel()
    #         # cv2.circle(img, (x, y), 3, [0, 255, 255], -1)
    #         point_flag = True
    #
    #         if (tt[y][x] == 0):
    #             y, x = alter_point(tt, y, x)
    #         if (abs(y - index) < 3 and not (total_point(tt, y, x) > 3)):
    #             continue
    #         if (x <= int(col / 3 + 0.5 + 1) or x >= int(col / 3 * 2 + 0.5 - 1)):
    #             continue
    #         if (3 < abs(y - index) < 8):
    #             pointx.append(x)
    #             pointy.append(y)
    # print('vewol: ', vewol_point)
    #
    # if (len(vewol_point) > 0):
    #     new_vewol = judge_vowel(img_filter, index, vewol_point)
    #
    #     if (len(new_vewol) > 0):
    #         print('newwol: ', new_vewol)
    #         for i in range(len(new_vewol)):
    #             pointx.append(new_vewol[i][0])
    #             pointy.append(new_vewol[i][1])
    # position_point = get_position(skelenton_image, pointx, pointy)
    # if (len(pointx) < 1):
    #     print("can't find feature point!")
    #     return 0
    #
    # result_point = find_segmention_point(adjunction_image(img), index, pointy, pointx, position_point)
    # # print(pointx)
    # # print(pointy)
    # print(position_point)
    wrfile.write(os.path.basename(file) + ',')
    # for i in range(len(result_point)):
    #     wrfile.write(str(result_point[i][1] - 3) + ' ' + str(result_point[i][0] - 3) + ' '
    #                  + str(result_point[i][3] - 3) + ' ' + str(result_point[i][2] - 3) + ',')
    wrfile.write(str(index))
    wrfile.write('\n')
    wrfile.flush()

    # result_pointx, result_pointy = [], []
    # for result in result_point:
    #     result_pointy.append(result[0])
    #     result_pointy.append(result[2])
    #     result_pointx.append(result[1])
    #     result_pointx.append(result[3])
    p2 = plt.subplot(211)
    p2.imshow(fill_image(get_fileter_image(adjunction_image(np.where(img / 255 > 0.9, 1, 0)))))
    p2.imshow(img)
    # print(corners)
    p1 = plt.subplot(212)
    p1.plot([1, col - 1], [index, index])
    p1.plot([int(col / 3 + 0.5), int(col / 3 + 0.5)], [0, row - 1], label[0])
    if (col < 100):
        p1.plot([int(col / 3 * 2 + 0.5), int(col / 3 * 2 + 0.5)], [0, row - 1], label[0])
    else:
        p1.plot([int(col / 4 * 3 + 0.5), int(col / 4 * 3 + 0.5)], [0, row - 1], label[0])
    # p2.plot(result_pointx, result_pointy, 'b.')
    p2.imshow(adjunction_image(img))
    p1.imshow(adjunction_image(img))
    p1.plot(pointx, pointy, "r.")
    plt.show()

    # tt = tt.astype(np.uint8)
    # io.imsave('tt.png', tt * 255)
    # tt_new, point1, point2, point3, point4 = find_extreme_point(tt, index)
    # p1.plot([point1[1]], [point1[0]], 'g.')
    # p1.plot([point2[1]], [point2[0]], 'g.')
    # p1.plot([point3[1]], [point3[0]], 'y.')
    # p1.plot([point4[1]], [point4[0]], 'y.')
    # print([point1[1]], [point1[0]], 'g.')
    # print([point2[1]], [point2[0]], 'k.')
    # print([point3[1]], [point3[0]], 'y.')
    # print([point4[1]], [point4[0]], 'y.')


def get_position(image, pointx, pointy):
    row, col = image.shape
    position_point = []
    for i in range(len(pointx)):
        xx = search_point(image * 1, pointx[i], pointy[i])
        yy = search_point(image * 1, pointx[i], pointy[i], up=False)
        print([xx, yy], pointy[i])
        if (xx == 0 and yy == 0):
            position_point.append("in")
            continue
        # if (xx == 0):
        #     position_point.append("up")
        #     continue
        # if (yy == 0):
        #     position_point.append("down")
        #     continue
        if pointy[i] - xx == 1:
            position_point.append("neardown")
            continue

        if (abs(xx - pointy[i]) > abs(yy - pointy[i])):
            if (pointy[i] - yy == -1):
                position_point.append("nearup")
            else:
                position_point.append("up")
        elif pointy[i] - xx == 1:
            position_point.append("neardown")
        else:
            position_point.append("down")
    print(position_point)
    return position_point


def search_point(image, pointx, pointy, up=True):
    # plt.subplot(211).imshow(image)
    # plt.show()
    row, col = image.shape
    if (up):
        for i in range(pointy - 1, - 1, -1):
            if (image[i][pointx] == 1):
                return i
    else:
        for i in range(pointy + 1, row, 1):
            if (image[i][pointx] == 1):
                return i
    return 0


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
    x, y = (lines[0][0][0], lines[0][1][0]), (lines[0][0][1], lines[0][1][1])
    radio = 90
    for line in lines:
        p0, p1 = line
        ax[2].plot((p0[0], p1[0]), (p0[1], p1[1]))
        if (p1[1] == p0[1]):
            x, y = (p0[0], p1[0]), (p0[1], p1[1])
            break
        tem = abs(abs(abs((p1[0] - p0[0])) / (p1[1] - p0[1])))
        if (tem < radio):
            radio = tem
            x, y = (p0[0], p1[0]), (p0[1], p1[1])
    ax[2].plot(x, y, 'w')
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
def check_near_point(x1, y1, x2, y2):
    return True


def find_segmention_point(image_or, index, pointx, pointy, position_point):
    row, col = image_or.shape
    image = copy.copy(image_or)
    # if (index > 10):
    #     for j in range(index - 1):
    #         for i in range(col):
    #             image[j][i] = 0
    #             image_or[j][i] = 0
    below_image = np.where(image_or.astype(np.uint8) / 255 > 0.1, 1, 0)
    result_segmentation_point = []
    # result = [[x, y, position, 0] for (x, y, position) in (pointx, pointy, position_point)]
    result = []
    for i in range(len(pointx)):
        result.append([pointx[i], pointy[i], position_point[i], 0])
    print("result:        ", result)
    for i in range(len(result) - 1):
        max = 100000
        tem = -1
        flag = True
        if (result[i][3] == 1):
            continue
        for j in range(i + 1, len(result), 1):
            if (result[j][3] == 0 and result[i][3] == 0 and result[i][2] != result[j][2]):
                if (abs(result[i][0] - result[j][0]) * abs(result[i][0] - result[j][0]) +
                        abs(result[i][1] - result[j][1]) * abs(result[i][1] - result[j][1]) < max):
                    max = abs(result[i][0] - result[j][0]) * abs(result[i][0] - result[j][0]) / 4 + abs(
                        result[i][1] - result[j][1]) * abs(result[i][1] - result[j][1])
                    tem = j

        if (max < 64):
            result_segmentation_point.append([result[i][0], result[i][1], result[tem][0], result[tem][1]])
            result[i][3] = 1
            result[tem][3] = 1
            continue
        point_flag = True
        t = result[i][0]
        if (result[i][2] == 'up'):
            t = t + 1
            while (t < row and below_image[t][result[-1][1]] == 0):
                t = t + 1
            if (t == row):
                t = result[i][0]
            for k in range(t + 1, row, 1):
                if (below_image[k][result[i][1]] == 0):
                    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                    if not (check_near_point(t, result[i][1], k - 1, result[i][1])):
                        break
                    result_segmentation_point.append([t, result[i][1], k - 1, result[i][1]])
                    result[i][3] = 1
                    flag = False
                    break
        elif (result[i][2] == 'down'):
            t = t - 1
            while (below_image[t][result[i][1]] == 0):
                t = t - 1
            for k in range(t - 1, -1, -1):
                if (below_image[k][result[i][1]] == 0):
                    print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                    if not (check_near_point(t, result[i][1], k + 1, result[i][1])):
                        break
                    result_segmentation_point.append([t, result[i][1], k + 1, result[i][1]])
                    result[i][3] = 1
                    flag = False
                    break
        elif (result[i][2] == 'neardown'):
            for k in range(t - 1, -1, -1):
                if (below_image[k][result[i][1]] == 0):
                    print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                    if not (check_near_point(t, result[i][1], k + 1, result[i][1])):
                        break
                    result_segmentation_point.append([t, result[i][1], k + 1, result[i][1]])
                    result[i][3] = 1
                    flag = False
                    break
        elif (result[i][2] == "nearup") or (result[i][2] == "in"):
            for k in range(t + 1, row, 1):
                if (below_image[k][result[i][1]] == 0):
                    print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                    if not (check_near_point(t, result[i][1], k - 1, result[i][1])):
                        break
                    result_segmentation_point.append([t, result[i][1], k - 1, result[i][1]])
                    result[i][3] = 1
                    flag = False
                    break

    t = result[-1][0]
    if (result[-1][2] == 'up' and result[-1][3] == 0):
        t = t + 1
        while (t < row and below_image[t][result[-1][1]] == 0):
            t = t + 1
        if (t == row):
            t = result[-1][0]
        for k in range(t + 1, row, 1):
            if (below_image[k][result[-1][1]] == 0):
                print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU2")
                if not (check_near_point(t, result[-1][1], k - 1, result[-1][1])):
                    break
                result_segmentation_point.append([t, result[-1][1], k - 1, result[-1][1]])
                result[-1][3] = 1
                break
    elif (result[-1][2] == 'down' and result[-1][3] == 0):
        t = t - 1
        while (below_image[t][result[-1][1]] == 0):
            t = t - 1
        for k in range(t - 1, -1, -1):
            if (below_image[k][result[-1][1]] == 0):
                print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD2")
                if not (check_near_point(t, result[-1][1], k + 1, result[-1][1])):
                    break
                result_segmentation_point.append([t, result[-1][1], k + 1, result[-1][1]])
                result[-1][3] = 1
                break
    elif (result[-1][2] == 'neardown' and result[-1][3] == 0):
        for k in range(t - 1, -1, -1):
            if (below_image[k][result[-1][1]] == 0):
                print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD2")
                if not (check_near_point(t, result[-1][1], k + 1, result[-1][1])):
                    break
                result_segmentation_point.append([t, result[-1][1], k + 1, result[-1][1]])
                result[-1][3] = 1
                break
    elif ((result[-1][2] == 'nearup' or result[-1][2] == 'up') and result[-1][3] == 0):
        for k in range(t + 1, row, 1):
            if (below_image[k][result[-1][1]] == 0):
                print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUU2")
                if not (check_near_point(t, result[-1][1], k - 1, result[-1][1])):
                    break
                result_segmentation_point.append([t, result[-1][1], k - 1, result[-1][1]])
                result[-1][3] = 1
                break

    print('finish reult: ', result)
    print(result_segmentation_point)
    print("over")
    # plt.subplot(212).imshow(below_image)
    # plt.show()
    return result_segmentation_point


path = r'./t1'
# path = r'./Test_Img'
path = r"H:\mark\finish\holiday\ResizeThree\alterxml"
# path = r'./nono'
# TODO 是否滤波 t2
# TODO 路径修改，第一个点为空白点
# path = r't2'

result_txt = r'H:\mark\finish\image_three_touch\base_line_three.txt'
wrfile = open(result_txt, 'a')
totalpoint = []
label = ["g.-", "b.-", "r.-", "k.-", "w.-", "c.-"]
for i in os.listdir(path):
    if i.endswith('.png'):
        # i = "chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0046_0_517.png"
        file = os.path.join(path, i)
        print(file)
        # show_point(r"./Test_Img/chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-10-0560_0_475.png")
        show_point(file)
wrfile.close()

