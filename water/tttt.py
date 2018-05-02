from  skimage import io
import numpy as np

def get_point_left_start_location(image):
    row, column = image.shape
    start = int(column / 2 - column / 6)
    end = int(column / 2 + column / 6)
    array = np.arange(start , end, 1)
    pointx = []
    pointy = []
    count = 0
    for i in range(row):
        for j in array:
            if ((image[int(i)][int(j) - 1] == 1) and (image[int(i)][int(j)] == 0)):

                for k in range (i):
                    count = count + image[k][j]
                if(count > 0):
                    count = 0
                    break;
                # append start point
                pointx.append(j)
                pointy.append(0)
                # append first point
                pointx.append(j)
                pointy.append(i)
                print("start point: [" + str(pointx[1]) + "," + str(pointy[1]) + "]")
                break
        if (len(pointx)):
            break;

    total = np.sum(image,axis=0)
    index = np.where(total == np.min(total[10:-10]))
    print(index,np.min(total[10:-10]))
    final_point = index[0][int(len(index[0]) / 2)]
    return pointx, pointy
def get_fileter_image(image):
    row,col = image.shape
    filter_image = image[:]
    for i in range (row):
        for j in range(1,col - 2):
            if(image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] ==1) or (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] ==0 and image[i][j + 1] ==1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] ==0) or (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] ==1 and image[i][j + 1] ==0):
                filter_image[i][j] = 0
    return filter_image
def adjunction_image(image):
    row,col = image.shape
    ad_image = np.zeros((row + 2, col + 2))
    for i in range(row):
        for j in range(col):
            ad_image[i + 1][ j + 1] = image[i][j]
    return image

image = io.imread("./Img/chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0002_1_21.png")
image = adjunction_image(image)
# image = transform.rotate(image, 180)
# rember delete
image = image.astype(int)
image = np.where(image > 0.9, 1, 0)
print("image shape :" + str(image.shape))
row, column = image.shape
image = get_fileter_image(image)
pointx = []
pointy = []
temp_x = temp_y = 0
spilte_point = [[0,0,0,0]]
pointx, pointy = get_point_left_start_location(image)
print(pointx,pointy)