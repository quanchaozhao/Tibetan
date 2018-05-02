#coding:utf-8

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from skimage import io,data,morphology
from skimage import measure
from sklearn.cluster import KMeans
import numpy as np
import os,re

def segmentation(image):
    cow,col = image.shape

    print("crow=" + str(cow))
    col_start = int (col / 2 - col / 10)
    col_end = int (col / 2 + col/ 10)
    image_option = image[ : ,col_start:col_end]
    image_left = np.zeros((cow,col_end - col_start))
    image_right = np.zeros((cow,col_end - col_start))

    cow_,col_ = image_option.shape;
    cent_col = int(col_ / 2)

    line = [[0,cent_col]]
    start = 0
    while(start < cow):
        rol_tem =  get_cow(image_option,start)
        print(rol_tem)
        if rol_tem > 0:
            line_start = [rol_tem,cent_col]
            line.append(line_start)

            image_tem = image_option[rol_tem:cow ,:]
            h_profile = np.sum(np.where(image_tem ==1,0,1),axis=0)
            min_value = np.min(h_profile)
            index=get_index( np.min(h_profile),h_profile)

            print(len(h_profile))
            line_second = [rol_tem,index]
            line.append(line_second)

            line_third = [rol_tem + min_value,index]
            line.append(line_third)

            line_fourth = [rol_tem + min_value , cent_col]
            line.append(line_fourth)

            start = rol_tem + min_value
            image_option = image_option[start:cow,:]
            print(line)
        else:
            break
    return image[ : ,col_start:col_end]

def get_index(value,array):

    for i in  range(len(array)):
        if array[i] == value:
            return i
def get_index2(value_X,value_Y,array):

    for i in  range(len(array)):
        if array[i][0] == value_X and array[i][1] == value_Y:
            return i

def get_cow (image,start):

    cow,rol = image.shape
    if start <= cow:
        rol = int(rol / 2)
        count = 0
        while(start < cow):
            if image[start][rol] == 1:
                count = count + 1
            if count > 1:
                break
            start = start + 1
    elif start >= cow:
        print("刀模为了" + str(start)  + "d" +  str (cow))
    return start - 1

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
        if minr == 0 or minc == 0 or maxr >= rows or maxc == cols or region.area < 40 or (maxr - minr) < 8:
            # print("****************************************************************************" + str(region.area))
            for point in region.coords:
                row,col = point
                img[row,col] = 1
    return img

if __name__ == '__main__':
    com = io.imread("D:\藏文识别\相关文献\data\gt_text_lines\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0149_0_0.png")
    name,type = os.path.basename("D:\藏文识别\相关文献\data\gt_text_lines\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0149_0_0.png").split('.')
    print("basename:" + name)
    com = com / 255
    com = remove_noise(com)
    com = np.where(com < 0.9,1,0)

    lb_img = measure.label(com)
    regions = measure.regionprops(lb_img)

    lb_img = morphology.remove_small_objects(lb_img, min_size=40, connectivity=1)
    p2 = plt.subplot(311)
    # p2.xaxis.set_major_locator(MultipleLocator(5.0))
    # p2.yaxis.set_major_locator(MultipleLocator(5.0))
    # p2.grid(which="major",color="#111111")
    p2.imshow(com,cmap="gray")

    ax = plt.subplot(312)
    ax.imshow(lb_img)
    count = 0
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        count = count + (max_col - min_col)
    count = count / len(regions)

    print ("均值：" + str(count))

    # count2 = np.zeros(500)
    # for region in regions:
    #     min_row, min_col, max_row, max_col = region.bbox
    #     count2[(max_col - min_col)] = count2[(max_col - min_col)] + 1
    # value = get_index(np.max(count2),count2)
    #
    # print(count2)
    # print("中位值：" + str(value))

    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        if (max_col - min_col)  > count * 1.5:
            rec = Rectangle((min_col-1,min_row-1),max_col-min_col,max_row-min_row,fill=False,edgecolor="red")
            ax.add_patch(rec)
            # p3 = plt.subplot(223)
            # p3.imshow(region.image)
            # p4 = plt.subplot(212)
            # p4.imshow(segmentation(region.image))
            # plt.imsave(str(min_col) + ".jpg",region.image,cmap = 'gray' )

    ax2 = plt.subplot(313)
    ax2.imshow(lb_img)
    array = []
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        array_tem = [0, max_col - min_col]
        array.append(array_tem)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(array)
    label = kmeans.labels_
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        if label[get_index2(0, max_col - min_col, array)] == 1:
            rec = Rectangle((min_col - 1, min_row - 1), max_col - min_col, max_row - min_row, fill=False,
                            edgecolor="red")
            ax2.add_patch(rec)

    plt.show()
