#-_-/// coding:utf-8 -_-///

import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from skimage import io,transform
from pylab import figure

def get_Next_Point_Left(image, pointx,pointy,point):
    # print(image.shape)
    # print(image[pointy][pointx -1])
    # print(image[pointy + 1][pointx - 1])
    # print(image[pointy + 1][pointx])
    # print(image[pointy + 1][pointx + 1])
    # print(image[pointy ][pointx + 1])
    row,rol = image.shape
    if((pointx - 1) < 0 or (pointx + 1) >= rol or (pointy + 1) >= row):
        return 0,0;
    if((image[pointy][pointx - 1] == 1 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
                image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 1)
           or (image[pointy][pointx - 1] == 0 and image[pointy + 1][pointx - 1] == 0 and image[pointy + 1][pointx ] == 0 and
                image[pointy + 1][pointx + 1] == 0 and image[pointy ][pointx + 1] == 0)
       or (image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx] == 0 )):
        return pointx,pointy + 1

    if( image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx + 1] == 0 ):
        return pointx + 1,pointy + 1
    #5
    if(image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 0):
        return pointx + 1,pointy
    # 6
    if(image[pointy ][pointx - 1] == 0 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 1):
        return pointx - 1,pointy
    return  pointx - 1,pointy + 1

def get_Next_Point_Right(image, pointx,pointy):
    # print(image.shape)
    # print(image[pointy][pointx -1])
    # print(image[pointy + 1][pointx - 1])
    # print(image[pointy + 1][pointx])
    # print(image[pointy + 1][pointx + 1])
    # print(image[pointy ][pointx + 1])
    if((image[pointy][pointx - 1] == 1 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
                image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 1)
       or (image[pointy][pointx - 1] == 0 and image[pointy + 1][pointx - 1] == 0 and image[pointy + 1][pointx ] == 0 and
                image[pointy + 1][pointx + 1] == 0 and image[pointy ][pointx + 1] == 0)
       or (image[pointy + 1][pointx + 1] == 1 and image[pointy + 1][pointx] == 0 )):
        return pointx,pointy+1

    if( image[pointy + 1][pointx + 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx - 1] == 0 ):
        return pointx - 1,pointy + 1
    #5
    if(image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx - 1] == 0):
        return pointx - 1,pointy
    # 6
    if(image[pointy ][pointx - 1] == 1 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 0):
        return pointx + 1,pointy
    return  pointx + 1,pointy + 1

def get_Next_Point_Right_B(image, pointx,pointy,B = 1):
    # print(image.shape)
    # print(image[pointy][pointx -1])
    # print(image[pointy + 1][pointx - 1])
    # print(image[pointy + 1][pointx])
    # print(image[pointy + 1][pointx + 1])
    # print(image[pointy ][pointx + 1])
    if((image[pointy][pointx - 1] == 1 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
                image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 1)):
        return pointx,pointy+1
    if((image[pointy][pointx - 1] == 0 and image[pointy + 1][pointx - 1] == 0 and image[pointy + 1][pointx ] == 0 and
                image[pointy + 1][pointx + 1] == 0 and image[pointy ][pointx + 1] == 0)
       or (image[pointy + 1][pointx + 1] == 1 and image[pointy + 1][pointx] == 0 )):
        return pointx - 1,pointy

    if( image[pointy + 1][pointx + 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx - 1] == 0 ):
        return pointx - 1,pointy + 1
    #5
    if(image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx ] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx - 1] == 0):
        return pointx - 1,pointy
    # 6
    if(image[pointy ][pointx - 1] == 1 and image[pointy + 1][pointx - 1] == 1 and image[pointy + 1][pointx] == 1 and
       image[pointy + 1][pointx + 1] == 1 and image[pointy ][pointx + 1] == 0):
        return pointx + 1,pointy
    return  pointx + 1,pointy + 1

def get_fileter_image(image):
    row,col = image.shape
    filter_image = image[:]
    for i in range (row):
        for j in range(1,col - 2):
            if(image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] ==1) or (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] == 0 and image[i][j + 1] == 1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] ==0) or (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] == 1 and image[i][j + 1] == 0):
                filter_image[i][j] = 0
    return filter_image
def get_min_index_rol(pointx,pointy):
    pointy = np.array(pointy)
    pointx = np.array(pointx)
    # print(pointy[-1])
    count = np.sum(pointy == pointy[-1])
    return pointx[-count]
def get_min_point(image,pointx,pointy,index):

    row,col = image.shape
    flag = False
    for i in range(pointy + 1,row):
        for j in range(pointx - 1,index - 1,-1):
            if(image[i][j] == 0):
                pointx = j
                pointy = i
                flag = True
                break
        if(flag):
            break
    return  pointx,pointy

def get_point_left_start_location(image):
    row, column = image.shape
    start = int(column / 2 - column / 4)
    end = int(column / 2 + column / 5)
    array = np.arange(start , end + 1, 1)
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
    return pointx, pointy
def get_multiple_point_left_start_location(image):
    row, column = image.shape
    start = int(column / 2 - column / 5)
    end = int(column / 2 + column / 5)
    array = np.arange(start / 10, end + 1, 1)
    pointx = []
    pointy = []
    count = 0;
    for i in range(row):
        for j in array:
            if ((image[int(i)][int(j) - 1] == 1) and (image[int(i)][int(j)] == 0)):

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
    return pointx, pointy

def get_point_right_start_location(image):
    row, column = image.shape
    start = int(column / 2 -  column / 5 )
    end = int(column / 2 + column / 3)
    pointx = []
    pointy = []
    array = np.arange(start,end,1)
    for i in range(row):
        for j in array:
            # print(str(image[int(i)][int(j)]) + str(image[int(i)][int(j + 1)]))
            if ((image[int(i)][int(j)] == 0) and (image[int(i)][int(j + 1)] == 1)):
                # append start point
                pointx.append(j)
                pointy.append(0)

                # append first point
                pointx.append(j)
                pointy.append(i)
                print("start point: [" + str(pointx[1]) + "," + str(pointy[1]) + "]")
                break
        if (len(pointy)):
            break
    return pointx, pointy

def get_point_left_start_vertical(image):

    array = np.sum(image, axis=0)
    start = int(len(array) / 4)
    end = int(len(array) / 2) + int(len(array) / 20)

    index = int(len(array) / 4)
    pointx = []
    pointy = []
    while (start < end):
        if (array[start] < array[index]):
            index = start
        start = start + 1
    pointx.append(index)
    pointy.append(0)
    print(array)
    print("OOOOOOOOOOOOOOOOOOOOO  " + str(index) + " rrrr" + str(array[index]))
    return pointx,pointy

def drop_failing(file, position = 'left'):
    image = io.imread(file)

    # image = transform.rotate(image, 180)
    # rember delete
    image = image.astype(int)
    image = np.where(image > 0.9, 1, 0)
    print("image shape :" + str(image.shape))
    row, column = image.shape
    # 滤波操作
    # image = get_fileter_image(image)

    pointx = []
    pointy = []
    temp_x = temp_y = 0

    if(position == "left"):
        pointx, pointy = get_point_left_start_location(image)
        if(len(pointx)):
            temp_y = pointy[-1]
            temp_x = pointx[-1]

        while temp_y < row - 1:
            temp_x, temp_y = get_Next_Point_Left(image, int(temp_x), (temp_y),pointx)
            if(0 == temp_y and 0 == temp_x):
                return pointx,pointy
            if (len(pointx) > 2):
                if (pointx[-2] == temp_x and pointy[-2] == temp_y):
                    print("left出现回溯现象：[" + str(temp_x) + "," + str(temp_y) + "]")

                    index = get_min_index_rol(pointx,pointy)
                    tempx, tempy = get_min_point(image,temp_x + 1,temp_y,index)
                    if(tempx == temp_x + 1 and tempy == temp_y):
                        pointy.append(temp_y + 1)
                        pointx.append(temp_x + 1)
                        temp_y = temp_y + 1
                        temp_x = temp_x + 1
                    else:
                        for i in range(1, len(pointx)):
                            if (pointx[len(pointx) - i] == tempx):
                                count = len(pointx) - i;
                                break

                        '''路径最优滴水算法'''
                        # print('count:', count)
                        # print("[" + str(tempx) + "," + str(tempy) + "],index = ", index)
                        # pointx = pointx[:count + 1]
                        # pointy = pointy[:count + 1]
                        # pointy.append(tempy )
                        # pointx.append(tempx )
                        # temp_y = tempy
                        # temp_x = tempx
                        '''传统滴水算法'''
                        pointy.append(temp_y + 1)
                        pointx.append(temp_x + 1)
                        temp_y = temp_y + 1
                        temp_x = temp_x + 1
                else:
                    pointy.append(temp_y)
                    pointx.append(temp_x)
            else:
                if (pointx[-1] > temp_x and pointy[-1] == temp_y):
                    pointy.append(temp_y + 1)
                    pointx.append(temp_x + 1)
                    temp_y = temp_y + 1
                    temp_x = temp_x + 1
                else:
                    pointy.append(temp_y)
                    pointx.append(temp_x)
    else:
        pointx, pointy = get_point_right_start_location(image)
        if (len(pointx)):
            temp_y = pointy[-1]
            temp_x = pointx[-1]
        else:
            return 0,0
        while temp_y < row - 1:

            temp_x, temp_y = get_Next_Point_Right(image, int(temp_x), int(temp_y))
            if (len(pointx) > 2):
                if (pointx[-2] == temp_x and pointy[-2] == temp_y):
                    print("right出现回溯现象：[" + str(temp_x) + "," + str(temp_y) + "]")

                    pointy.append(temp_y + 1)
                    pointx.append(temp_x - 1)
                    temp_y = temp_y + 1
                    temp_x = temp_x - 1
                else:
                    pointy.append(temp_y)
                    pointx.append(temp_x)
            else:
                if (pointx[-1] < temp_x and pointy[-1] == temp_y):

                    pointy.append(temp_y + 1)
                    pointx.append(temp_x - 1)
                    temp_y = temp_y + 1
                    temp_x = temp_x - 1
                else:
                    pointy.append(temp_y)
                    pointx.append(temp_x)
    return pointx,pointy

if __name__ == '__main__':

    file = "D:\藏文识别\相关文献\data\Test_character\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0007_1_09.png"
    path = 'D:\藏文识别\相关文献\data\Test_character'
    k = 0
    for i in os.listdir(path):
        file = os.path.join(path,i)
        if file.endswith('.png'):
            k = k + 1
            figure(k)
            image = io.imread(file)
            # image = transform.rotate(image,180)

            print(file)
            pointx_right, pointy_right = drop_failing(file, position='right')
            pointx_left, pointy_left = drop_failing(file, position='left')
            p1 = plt.subplot(211)
            p1.imshow(image, cmap="gray")

            p2 = plt.subplot(212)
            p2.imshow(image, cmap="gray")
            p2.plot(pointx_left, pointy_left, 'r.-')
            p2.plot(pointx_right, pointy_right, 'b.-')
            plt.show()



