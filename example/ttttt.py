# -*- coding:utf-8 -*-
from skimage import io
from skimage.morphology import skeletonize,skeletonize_3d
from skimage.filters import roberts,sobel,scharr,prewitt
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature

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

def adjunction_image(image):
    row, col = image.shape
    ad_image = np.zeros((row + 10, col + 10))
    for i in range(row):
        for j in range(col):
            ad_image[i + 5][j + 5] = image[i][j]
    return ad_image

def skeleton_image(file):
    image_origin = io.imread(file, as_grey=True)

    image_origin = np.where(image_origin > 0, 1, 0)
    image_origin = adjunction_image(image_origin)
    # 骨架
    edge_roberts = roberts(image_origin)
    edge_roberts = feature.canny(image_origin, sigma = 1)
    edge_roberts = np.where(edge_roberts > 0, 3, 0)
    skeleton = skeletonize_3d(image_origin)
    # back_image = np.where(image_origin > 0, 0, 1)
    back_image = np.where(image_origin > 0, 0, 1)
    back_thin_images = skeletonize(back_image)
    [row, col] = back_thin_images.shape
    back_thin_image = np.zeros((row, col))
    back_thin_image[:, int(col / 5):int(col / 5) * 4] = back_thin_images[:, int(col / 5):int(col / 5) * 4]
    p2 = plt.subplot(421)
    p2.imshow(image_origin + back_thin_images, cmap="gray")

    total_image = edge_roberts + back_thin_images
    p2 = plt.subplot(422)
    p2.imshow(total_image)


    p3 = plt.subplot(425)
    p3.imshow(np.where(roberts(image_origin) > 0, 1, 0))
    p3 = plt.subplot(426)
    p3.imshow(np.where(sobel(image_origin) > 0, 2, 0))
    p3 = plt.subplot(427)
    p3.imshow(np.where(scharr(image_origin) > 0, 2, 0))
    p3 = plt.subplot(428)
    p3.imshow(np.where(prewitt(image_origin) > 0, 2, 0))

    plt.show()


if __name__ == "__main__":
    path = 'D:\藏文识别\相关文献\data\gt_text_lines'
    path2 = 'D:\藏文识别\相关文献\data\Sticky_text'
    path3 = 'D:\藏文识别\相关文献\data\marke_Sticky_text\ '

    for i in os.listdir(path2):
        file = os.path.join(path2,i)
        if file.endswith('.png'):
            skeleton_image(file)
    ddd = []
    ss = []
    ddd.append([1,3])
    ddd.append([2,4])
    ddd.pop(-1)
    ss.append(ddd)
    print(len(ss))