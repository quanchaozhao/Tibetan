import numpy as np
import matplotlib.pyplot as plt
from skimage import io

def gradient():
    los = 0.00000001
    x = 2000
    y = 1000
    z = 20
    f = (x - 10) * ( x - 10) + (y - 10) * (y - 10) + z * z
    print(f)
    ratio = 0.01
    while(f > los):
        x = x - 2 * ratio * (x - 10)
        y = y - 2 * ratio * (y - 10)
        z = z - 2 * ratio * z
        f = (x - 10) * (x - 10) + (y - 10) * (y - 10) + z * z
        print(x, y,z,f)

def del_T_type(image):
    row,col = image.shape

    for i in range(1, row - 1, 1):
        for j in range(1, col - 1, 1):
            if image[i][j] == 1:
                # 修正T型

                if( image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 0
                     and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0): #    1
                    image[i][j] = 0                #  1 1 1
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 1 and image[i - 1][j] == 1 and image[i][j + 1] == 0 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0):#    1
                    image[i][j] = 0               #  1 1
                    image[i + 1][j] = 0           #    1
                if (image[i][j - 1] == 1 and image[i - 1][j] == 0 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0): # 1 1 1
                    image[i][j] = 0                #   1
                    image[i][j - 1] = 0
                if (image[i][j - 1] == 0 and image[i - 1][j] == 1 and image[i][j + 1] == 1 and image[i + 1][j] == 1
                        and image[i - 1][j - 1] == 0 and image[i - 1][j + 1] == 0 and image[i + 1][j + 1] == 0 and
                        image[i + 1][j - 1] == 0): #  1
                    image[i][j] = 0                #  1 1
                    image[i + 1][j] = 0            #  1
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

# image = io.imread('tt.png') / 255
# image = image.astype(np.int8)
#
# p1 = plt.subplot(211)
# p1.imshow(image)
#
# p2 = plt.subplot(212)
# p2.imshow(del_T_type(image))
# plt.show()
s = [[40, 12],[10,90]]
d = list((12,4))
d.extend(np.array(s)[:,0])
print(d)


ss = list([[54, 31, 'neardown', 0], [45, 40, 'nearup', 0], [13, 48, 'neardown', 0]])
print(ss[1][2])