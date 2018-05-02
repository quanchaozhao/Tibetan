#coiding:utf-8

import os
from skimage import io,morphology,measure
import numpy as np
import  matplotlib.pyplot as plt
from  matplotlib.patches import Rectangle
import copy

NOISE_SIZE_THRESHOLD = 40
def remove_noise(img):
    # 噪声分为两类，一类是小的像素点，一类是和边框连在一起的
    rows, cols = img.shape
    img_bin = np.where(img >= 0.99, 0, 1)
    img_labeled = measure.label(img_bin)

    regions = measure.regionprops(img_labeled)

    for region in regions:
        region_label = region.label
        minr, minc, maxr, maxc = region.bbox
        # 和边框连接在一起的噪声去除
        if minr == 0 or minc == 0 or maxr >= rows or maxc == cols or region.area < NOISE_SIZE_THRESHOLD or (maxr - minr) < 8:
            # print("****************************************************************************" + str(region.area))
            for point in region.coords:
                row,col = point
                img[row,col] = 1
    return img

def isolate_character(image,file):
    image = np.where(image > 0.5,0, 1)
    lb_image = measure.label(image)
    lb_image = morphology.remove_small_objects(lb_image,min_size = 50 , connectivity = 1 )

    regions = measure.regionprops(lb_image)
    count = 0
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        count = count + (max_col - min_col)
    count = count / len(regions)

    i = 0
    DPI = 100
    tem = 0
    rows, cols = image.shape
    figsize = cols / DPI, rows / DPI
    # fig = plt.figure(figsize=figsize)
    # ax = fig.add_axes([0, 0, 1, 1])
    # # regions[0][0] = regions[0][0] + regions[0][1]
    # for region in regions:
    #     min_row, min_col, max_row, max_col = region.bbox
    #     if (max_col - min_col) < count * 6:
    #         # plt.imsave(path2 + str(i) + ".png", region.image,cmap = "gray")
    #         # print(path2 + str(i) + ".png")
    #         rec = Rectangle((min_col - 1, min_row - 1), max_col - min_col, max_row - min_row, fill=False,
    #                         edgecolor="red")
    #         ax.add_patch(rec)
    #
    #         # io.imsave(file2 + str(i) + ".png", region.image.astype(np.uint8) * 255, cmap="gray")
    #         # print(file2 + str(i) + ".png")
    #     # i = i + 1
    # ax.imshow(image,cmap = "gray")

    totallist = []
    for region in regions:
        min_row, min_col, max_row, max_col= region.bbox
        if (max_col - min_col) < count * 1.3:
            totallist.append([region.bbox, region.image.astype(np.int32),0])
    tem_image = 0
    for i in range(len(totallist)):
        for j in range(i + 1,(len(totallist)),1):
            if totallist[i][0][1] < totallist[j][0][1]:
                min_x1,mid_x1,mid_x2,max_x2 = totallist[i][0][1],totallist[j][0][1],totallist[i][0][3],totallist[j][0][3]
            elif (totallist[i][0][1] > totallist[j][0][1]):
                min_x1, mid_x1, mid_x2, max_x2 = totallist[j][0][1],totallist[i][0][1],totallist[j][0][3],totallist[i][0][3]
            else:
                min_x1, mid_x1, mid_x2, max_x2 = np.sort([totallist[j][0][1], totallist[i][0][1], totallist[j][0][3],totallist[i][0][3]])
            if totallist[i][2] == 2:
                break
            confidence_value = (mid_x2 - mid_x1)/(max_x2 - min_x1)
            print(min_x1,mid_x1,mid_x2,max_x2,"confidence",confidence_value)
            # if( 1 > confidence_value > 0.3):
            #     min_y1,a,b,max_y2 = np.sort([totallist[i][0][0],totallist[j][0][0],totallist[i][0][2],totallist[j][0][2]])
            #     a1_y1, a1_y2, a1_x1, a1_x2 = totallist[i][0][1] - min_x1, totallist[i][0][3] - min_x1, totallist[i][0][0] - min_y1, totallist[i][0][2] - min_y1
            #     b1_y1, b1_y2, b1_x1, b1_x2 = totallist[j][0][1] - min_x1, totallist[j][0][3] - min_x1, totallist[j][0][0] - min_y1, totallist[j][0][2] - min_y1
            #     tem_image = np.zeros((max_y2 - min_y1 + 8,max_x2 - min_x1 + 8))
            #     dd = plt.figure()
            #     dd.add_axes([0, 0, 1, 1]).imshow(totallist[i][1])
            #     plt.show()
            #     tem_image[a1_x1:a1_x2, a1_y1:a1_y2] = totallist[i][1]
            #     tem_image[b1_x1:b1_x2, b1_y1:b1_y2] = totallist[j][1]
            #     print(tem_image.shape)
            if (confidence_value > 0.4):
                totallist[i][2] = 1
                if(totallist[i][0][1] < totallist[j][0][1] and totallist[i][0][3] > totallist[j][0][3]) or (totallist[j][0][1] < totallist[i][0][1] and totallist[j][0][3] >totallist[i][0][3]):
                    min_x1, mid_x1, mid_x2, max_x2 =np.sort( [totallist[i][0][1], totallist[j][0][1], totallist[i][0][3],totallist[j][0][3]])
                    min_y1, a, b, max_y2 = np.sort(
                        [totallist[i][0][0], totallist[j][0][0], totallist[i][0][2], totallist[j][0][2]])
                    a1_y1, a1_y2, a1_x1, a1_x2 = totallist[i][0][1] - min_x1, totallist[i][0][3] - min_x1, totallist[i][0][
                                                     0] - min_y1, totallist[i][0][2] - min_y1
                    b1_y1, b1_y2, b1_x1, b1_x2 = totallist[j][0][1] - min_x1, totallist[j][0][3] - min_x1, totallist[j][0][
                                                     0] - min_y1, totallist[j][0][2] - min_y1
                    tem_image1 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    tem_image2 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    # dd = plt.figure()
                    # dd.add_axes([0, 0, 1, 1]).imshow(totallist[i][1])
                    # plt.show()
                    a1_y2 =  a1_y2  - 1
                    b1_y2 =  b1_y2 - 1
                    print(totallist[i][1].shape)
                    # print(tem_image.shape)
                    # tem_image1[0:19,0:32] = totallist[i][1]
                    row,col = totallist[i][1].shape
                    for ii in range(row):
                        for jj in range(col):
                            tem_image1[a1_x1 + ii][a1_y1 + jj] = totallist[i][1][ii][jj]
                    row, col = totallist[j][1].shape
                    for iii in range(row):
                        for jjj in range(col):
                            tem_image2[b1_x1 + iii][b1_y1 + jjj] = totallist[j][1][iii][jjj]
                    # tem_image1[a1_x1:a1_x2 , a1_y1:(a1_y2 + 1)] = totallist[i][1]
                    # tem_image2[b1_x1:b1_x2 , b1_y1:(b1_y2 + 1)] = totallist[j][1]

                    tem_image = tem_image1 + tem_image2
                    tem = np.where(tem_image > 0.6, 1, 0)
                    print(tem_image.shape)

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
                    tem_image = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    # dd = plt.figure()
                    # dd.add_axes([0, 0, 1, 1]).imshow(totallist[i][1])
                    # plt.show()

                    tem_image1[a1_x1:a1_x2, a1_y1:a1_y2] = totallist[i][1]
                    tem_image2[b1_x1:b1_x2, b1_y1:b1_y2] = totallist[j][1]
                    tem_image = tem_image1 + tem_image2
                    tem = np.where(tem_image > 0.6,1, 0)
                    print(tem_image.shape)
                    totallist[i][1] = tem
                    totallist[i][0] = [min_y1,min_x1,max_y2,max_x2]
                    totallist[j][2] = 2
    # for i in range(len(totallist)):
    #     if(totallist[i][2] != 2):
    #         io.imsave("D:\\datebase\\isolate_character\\" + file.split(".")[0] + str(i) + ".png",totallist[i][1] * 255, cmap="gray")
    #         print("D:\\datebase\\isolate_character\\" + file.split(".")[0] + str(i) + ".png")


if __name__ == "__main__":

    path = 'D:\藏文识别\相关文献\data\gt_text_lines'
    for i in os.listdir(path):
        file = os.path.join(path, i)
        if file.endswith('.png'):
            image = io.imread(file)
            image = image / 255
            # p2 = plt.subplot(211)
            # p2.imshow(image,cmap = "gray")
            image = remove_noise(image)
            # p1 = plt.subplot(212)
            print(file,"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",i)
            isolate_character(image,i)
            # p1.imshow(isolate_character(image),cmap = "gray")
            # plt.show()