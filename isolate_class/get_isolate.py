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
def isolate_character(image,file,file2):
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
        # if ((max_col - min_col) > count * 1.6 and (max_col - min_col) / (max_row - min_row) < 1.8 )or ((max_col - min_col) / (max_row - min_row)  > count * 2.5):
        totallist.append([region.bbox, region.image.astype(np.int32),0])
    tem_image = 0
    # for i in range(len(totallist)):
    #     for j in range(i + 1,(len(totallist)),1):
    #         if totallist[i][0][1] < totallist[j][0][1] and totallist[i][0][3] < totallist[j][0][3]:
    #             min_x1,mid_x1,mid_x2,max_x2 = totallist[i][0][1],totallist[j][0][1],totallist[i][0][3],totallist[j][0][3]
    #         elif (totallist[i][0][1] > totallist[j][0][1] and totallist[i][0][3] > totallist[j][0][3]):
    #             min_x1, mid_x1, mid_x2, max_x2 = totallist[j][0][1],totallist[i][0][1],totallist[j][0][3],totallist[i][0][3]
    #         else:
    #             min_x1, mid_x1, mid_x2, max_x2 = np.sort([totallist[j][0][1], totallist[i][0][1], totallist[j][0][3],totallist[i][0][3]])
    #         if totallist[i][2] == 2:
    #             break
    #         if totallist[j][2] == 2:
    #             continue
    #         min_width = np.min([totallist[i][0][3] - totallist[i][0][1], totallist[j][0][3] - totallist[j][0][1]])
    #         confidence_value = (mid_x2 - mid_x1) / min_width
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
                    min_x1, mid_x1, mid_x2, max_x2 =np.sort( [totallist[i][0][1], totallist[j][0][1], totallist[i][0][3],totallist[j][0][3]])
                    min_y1, a, b, max_y2 = np.sort(
                        [totallist[i][0][0], totallist[j][0][0], totallist[i][0][2], totallist[j][0][2]])
                    a1_y1, a1_y2, a1_x1, a1_x2 = totallist[i][0][1] - min_x1, totallist[i][0][3] - min_x1, totallist[i][0][
                                                     0] - min_y1, totallist[i][0][2] - min_y1
                    b1_y1, b1_y2, b1_x1, b1_x2 = totallist[j][0][1] - min_x1, totallist[j][0][3] - min_x1, totallist[j][0][
                                                     0] - min_y1, totallist[j][0][2] - min_y1
                    tem_image1 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    tem_image2 = np.zeros((max_y2 - min_y1, max_x2 - min_x1))

                    a1_y2 =  a1_y2  - 1
                    b1_y2 =  b1_y2 - 1
                    # print(totallist[i][1].shape)
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
                    tem_image = np.zeros((max_y2 - min_y1, max_x2 - min_x1))
                    # dd = plt.figure()
                    # dd.add_axes([0, 0, 1, 1]).imshow(totallist[i][1])
                    # plt.show()

                    tem_image1[a1_x1:a1_x2, a1_y1:a1_y2] = totallist[i][1]
                    tem_image2[b1_x1:b1_x2, b1_y1:b1_y2] = totallist[j][1]
                    tem_image = tem_image1 + tem_image2
                    tem = np.where(tem_image > 0.6,1, 0)
                    # print(tem_image.shape)
                    totallist[i][1] = tem
                    totallist[i][0] = [min_y1,min_x1,max_y2,max_x2]
                    totallist[j][2] = 2
    for i in range(len(totallist)):
        if(totallist[i][2] != 2):
            min_row, min_col, max_row, max_col = totallist[i][0][0], totallist[i][0][1], totallist[i][0][2],totallist[i][0][3]
            if  (max_col - min_col) <= 1.3 * count:
                io.imsave("D:\\datebase\\character\\isolate_character\\" + file.split(".")[0] + str(i) + ".png",totallist[i][1] * 255, cmap="gray")
                print("D:\\datebase\\character\\isolate_character\\" + file.split(".")[0] + str(i) + ".png")
            elif((max_col - min_col) > 1.3 * count and (max_col - min_col) <= 1.7 * count):
               io.imsave("D:\\datebase\\character\\touch_character\\two_touch_character\\" + file.split(".")[0] + str(i) + ".png", totallist[i][1] * 255, cmap="gray")
               print("D:\\datebase\\character\\touch_character\\two_touch_character\\" + file.split(".")[0] + str(i) + ".png")
            else:
                io.imsave("D:\\datebase\\character\\touch_character\\three_touch_character\\" + file.split(".")[0] + str(i) + ".png", totallist[i][1] * 255, cmap="gray")
                print("D:\\datebase\\character\\touch_character\\three_touch_character\\" + file.split(".")[0] + str(i) + ".png")

   # 标注原始行

    # DPI = 100
    # rows, cols = image.shape
    # figsize = cols / DPI, rows / DPI
    # fig = plt.figure(figsize=figsize)
    # ax = fig.add_axes([0, 0, 1, 1])
    # k = 0
    # for i in range(len(totallist)):
    #     min_row, min_col, max_row, max_col  = totallist[i][0][0],totallist[i][0][1],totallist[i][0][2],totallist[i][0][3]
    #     if (totallist[i][2] != 2 and (max_col - min_col) > count * 1.3):
    #         k = k + 1
    #         # plt.imsave(path2 + str(i) + ".png", region.image,cmap = "gray")
    #         # print(path2 + str(i) + ".png")
    #         io.imsave("d:\\datebase\\mark_lines\\2\\"  + str(i) + ".png",
    #                   totallist[i][1] * 255, cmap="gray")
    #         rec = Rectangle((min_col - 1, min_row - 1), max_col - min_col, max_row - min_row, fill=False,
    #                         edgecolor="red")
    #         ax.add_patch(rec)
    #         # if(k == 2):
    #         #     break
    # ax.imshow(image, cmap="gray")
    # fig.savefig(file2)
    # print(file2)



if __name__ == "__main__":

    path = 'D:\\藏文识别\\相关文献\\data\\gt_text_lines'
    path2 = "d:\\datebase\\mark_lines\\"
    for i in os.listdir(path):
        file = os.path.join(path, i)
        if file.endswith('.png'):
            image = io.imread(file)
            image = image / 255
            # p2 = plt.subplot(211)
            # p2.imshow(image,cmap = "gray")
            image = remove_noise(image)
            # p1 = plt.subplot(212)
            isolate_character(image,i,path2 + i)
            # p1.imshow(isolate_character(image),cmap = "gray")
            # plt.show()