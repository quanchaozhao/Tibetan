#coding:utf-8

import os,re
from skimage import io,morphology,measure
import numpy as np
import matplotlib .pyplot as plt
from matplotlib.patches import Rectangle


NOISE_SIZE_THRESHOLD = 40

def process_and_save_photo(path2,image):

    image = np.where(image < 0.9, 1, 0)

    lb_img = measure.label(image)
    regions = measure.regionprops(lb_img)

    lb_img = morphology.remove_small_objects(lb_img, min_size = 40, connectivity=1)

    count = 0
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        count = count + (max_col - min_col)
    count = count / len(regions)
    i = 0
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        if (max_col - min_col) > count * 1.5:
            plt.imsave(path2 + str(i) + ".png", region.image,cmap = "gray")
            print(path2 + str(i) + ".png")
        i = i + 1


def marke_image(file,file2,image):

    image = np.where(image<0.9 , 1, 0)

    lb_img = measure.label(image)
    lb_img = morphology.remove_small_objects(lb_img, min_size=40, connectivity=1)
    regions = measure.regionprops(lb_img)
    count = 0
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        count = count + (max_col - min_col)
    count = count / len(regions)
    i = 0

    DPI = 100
    rows, cols = image.shape
    figsize = cols / DPI,rows / DPI
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0,0,1,1])
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        if (max_col - min_col) > count * 1.5:
            #plt.imsave(path2 + str(i) + ".png", region.image,cmap = "gray")
            #print(path2 + str(i) + ".png")
            rec = Rectangle((min_col - 1, min_row - 1), max_col - min_col, max_row - min_row, fill=False,
                            edgecolor="red")
            ax.add_patch(rec)

            io.imsave(file2 + str(i) + ".png", region.image.astype(np.uint8)*255, cmap="gray")
            print(file2 + str(i) + ".png")
        i = i + 1
    ax.imshow(image,cmap="gray")
    fig.savefig(file)
    print("file" + file)

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

if __name__ == "__main__":
    path = 'D:\藏文识别\相关文献\data\gt_text_lines'
    path2 = 'D:\藏文识别\相关文献\data\Sticky_text\ '
    path3 = 'D:\藏文识别\相关文献\data\marke_Sticky_text\ '

    for i in os.listdir(path):
        file = os.path.join(path,i)
        if file.endswith('.png'):
            image = io.imread(file)
            image = image / 255
            image = remove_noise(image)
            name,type = os.path.basename(file).split('.')
            # process_and_save_photo(path2 + name,image)
            marke_image(path3 + name,path2 + name,image)
