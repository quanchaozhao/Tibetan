import numpy as np
import os
from skimage.transform import probabilistic_hough_line
from matplotlib import cm
from skimage.feature import canny
from skimage import data,io

import matplotlib.pyplot as plt


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
            if (image[j - 1][i]== 0 and image[j][i] == 1 and image[j + 1][i] == 1) or \
                    (image[j - 1][i] == 1 and image[j][i] == 1 and image[j + 1][i] == 0) or \
                    (image[j - 1][i] == 0 and image[j][i] == 1 and image[j + 1][i] == 0):
                image_copy[j][i] = 1
    return image_copy

path = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total_alter'

def get_line(file):
    image = io.imread(file)

    image = image / 255
    edges = get_outline(image)
    lines = probabilistic_hough_line(edges, threshold=10, line_length=10,
                                     line_gap=3)

    # Generating figure 2
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(image, cmap=cm.gray)
    ax[0].set_title('Input image')

    ax[1].imshow(edges, cmap=cm.gray)
    ax[1].set_title('Canny edges')

    ax[2].imshow(edges * 0)
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
for i in os.listdir(path):
    if i.endswith('.png'):
        file = os.path.join(path,i)
        # show_point(r"./Test_Img/chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-10-0560_0_475.png")
        get_line(file)