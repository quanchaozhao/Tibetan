# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from skimage.draw import polygon
import numpy as np
import copy
import os
from skimage import io, transform, filters, morphology
from pylab import figure,mpl
import copy
mpl.rcParams['font.sans-serif'] = ['SimHei']
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
    return pointx - 1,pointy + 1

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
    return pointx + 1,pointy + 1

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
def find(image,x,y):
    row,col = image.shape
    for i in range(y,row,1):
        if image[i][x] != 1:
            return i;

def get_fileter_image(image):
    row,col = image.shape
    filter_image = image[:]
    for i in range (row):
        for j in range(1,col - 2):
            if(image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] ==1) or (image[i][j - 1] == 1 and image[i][j] == 0 and image[i][j + 1] ==0 and image[i][j + 1] ==1):
                filter_image[i][j] = 1
            if (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] ==0) or (image[i][j - 1] == 0 and image[i][j] == 1 and image[i][j + 1] ==1 and image[i][j + 1] ==0):
                filter_image[i][j] = 0
    return image
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
def get_min_index_rol(pointx,pointy):
    pointy = np.array(pointy)
    pointx = np.array(pointx)
    # print(pointy[-1])
    count = np.sum(pointy == pointy[-1])
    return pointx[-count]
def get_min_index(pointx,pointy):
    pointy = np.array(pointy)
    pointx = np.array(pointx)
    # print(pointy[-1])
    count = np.sum(pointy == pointy[-1])
    return len(pointx) - count
def alter_point(image,point):
    temx,temy = [],[]
    pointx,pointy = point
    if(image[pointx[0]][pointy[0]] == 1):
        temx.append(pointx[0])
        temy.append(pointy[0])
    for i in range(0,len(pointx) - 1,1):
        if(image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][pointy[i + 1]] == 1) or \
                (image[pointx[i - 1]][pointy[i - 1]] == 1 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0):
            temx.append(pointx[i])
            temy.append(pointy[i])
        if (image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0) or \
                (image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0):
            temx.append(pointx[i])
            temy.append(pointy[i])
            temx.append(pointx[i])
            temy.append(pointy[i])
    if (image[pointx[-1]][pointy[-1]] == 1):
        temx.append(pointx[-1])
        temy.append(pointy[-1])
    return temx,temy
def get_point_left_start_location(image):
    row, column = image.shape
    start = int(column / 4)
    end = int(column / 2)
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
    plt.subplot(111).imshow(image)
    plt.show()

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
    start = int(column / 2  - column / 4)
    end = int(column / 2 + column / 4)
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

def drop_failing(file, position = 'left',rotate = True):
    image = io.imread(file)
    image = adjunction_image(image)
    if(rotate):
        image = transform.rotate(image, 180)
    # rember delete
    image = image.astype(int)
    image = np.where(image > 0.9, 1, 0)
    print("image shape :" + str(image.shape))
    row, column = image.shape
    image = get_fileter_image(image)
    pointx = []
    pointy = []
    temp_x = temp_y = 0
    spilte_point = []
    if(position == "left"):
        pointx, pointy = get_point_left_start_location(image)
        if(len(pointx)):
            temp_y = pointy[-1]
            temp_x = pointx[-1]

        while temp_y < row - 1:
            temp_x, temp_y = get_Next_Point_Left(image, int(temp_x), (temp_y),pointx)
            if(0 == temp_y and 0 == temp_x):
                return pointx,pointy,[]
            if (len(pointx) > 2):
                if (pointx[-2] == temp_x and pointy[-2] == temp_y):
                    print("left出现回溯现象：[" + str(temp_x) + "," + str(temp_y) + "]")
                    t1_y = temp_y + 1
                    t1_x = temp_x + 1
                    index = get_min_index_rol(pointx,pointy)
                    tempx, tempy = get_min_point(image,temp_x + 2,temp_y,index)
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
                        print('count:', count)

                        print("[" + str(tempx) + "," + str(tempy) + "],index = ",index)
                        '''路径最优滴水算法'''
                        pointx = pointx[:count + 1]
                        pointy = pointy[:count + 1]
                        pointy.append(tempy )
                        pointx.append(tempx )
                        temp_y = tempy
                        temp_x = tempx
                        '''传统滴水算法'''
                        # pointy.append(temp_y + 1)
                        # pointx.append(temp_x + 1)
                        # temp_y = temp_y + 1
                        # temp_x = temp_x + 1
                        spilte_point.append([t1_x,t1_y,temp_x, temp_y - 1])
                else:
                    pointy.append(temp_y)
                    pointx.append(temp_x)
            else:
                if (pointx[-1] > temp_x and pointy[-1] == temp_y):
                    print(temp_x,temp_y)
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
            return 0,0,[]
        while temp_y < row - 1:

            temp_x, temp_y = get_Next_Point_Right(image, int(temp_x), int(temp_y))
            if (len(pointx) > 2):
                if (pointx[-2] == temp_x and pointy[-2] == temp_y):
                    print("right出现回溯现象：[" + str(temp_x) + "," + str(temp_y) + "]")

                    index = get_min_index(pointx, pointy)
                    print('index: ',index,'point:',get_min_index_rol(pointx, pointy))
                    # print(index)
                    pointy = pointy[:index + 1]
                    pointx = pointx[:index + 1]

                    temp_y = pointy[-1] + 1
                    temp_x = pointx[-1]
                    pointy.append(temp_y)
                    pointx.append(temp_x)

                    ty2 = find(image, temp_x, temp_y)
                    spilte_point.append([temp_x, temp_y , temp_x, ty2 - 1])

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

    print(pointx)
    print(pointy)
    return pointx,pointy,spilte_point
def adjunction_image(image):
    row,col = image.shape
    ad_image = np.zeros((row + 2, col + 2))
    for i in range(row):
        for j in range(col):
            ad_image[i + 1][ j + 1] = image[i][j]
    return ad_image

if __name__ == '__main__':

    file = "D:\藏文识别\相关文献\data\Test_character\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0007_1_09.png"
    path = 'D:\藏文识别\相关文献\data\Test_character'
    path = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total_alter'
    k = 0
    for i in os.listdir(path):
        file = os.path.join(path,i)
        if file.endswith('.png'):
            k = k + 1
            figure(k)
            image = io.imread(file)
            image = transform.rotate(image,180)

            print(file)

            image = adjunction_image(image)
            image = get_fileter_image(np.where(image > 0,1,0))
            image_copy = copy.copy(image)
            row,col = image.shape
            # pointx_right, pointy_right,spilte_point = drop_failing(file, position='right')
            pointx_left, pointy_left,spilte_point = drop_failing(file, position='right')
            pointx_left_copy = copy.copy(pointx_left)
            pointy_left_copy = copy.copy(pointy_left)
            pointx_left.insert(0,0)
            pointy_left.insert(0,0)
            pointx_left.append(0)
            pointy_left.append(row - 1)
            pointx_left.append(0)
            pointy_left.append(0)
            img = np.zeros((row,col))
            rr, cc = polygon( pointy_left,pointx_left)
            img[rr, cc] = 1
            img = img.astype(int)
            image = image.astype(int)
            img = np.bitwise_and(np.array(img),np.array(image))
            left = np.sum(img)
            img2 = image - img
            right = np.sum(img2)
            ratio = left / right
            print('left', left, 'right', right, 'ratio', ratio)
            if( ratio < 0.4 or ratio > 1.7):
                print('right water start....')
                pointx_left, pointy_left, spilte_point = drop_failing(file, position='left',rotate=False)
                pointx_left_copy = copy.copy(pointx_left)
                pointy_left_copy = copy.copy(pointy_left)
                pointx_left.insert(0, 0)
                pointy_left.insert(0, 0)
                pointx_left.append(0)
                pointy_left.append(row - 1)
                pointx_left.append(0)
                pointy_left.append(0)
                img = np.zeros((row, col))
                rr, cc = polygon(pointy_left, pointx_left)
                img[rr, cc] = 1
                img = img.astype(int)
                image = transform.rotate(image.astype(np.float64), 180)
                image = image.astype(int)

                img2 = np.bitwise_and(np.array(img), np.array(image))
                left = np.sum(img)
                img = image - img2
                right = np.sum(img2)
                ratio = left / right
                print('left', left, 'right', right, 'ratio', ratio)
                image = transform.rotate(image.astype(np.float64), 180)
                img2 = filters.rank.median(img2.astype(np.uint8), morphology.disk(2))
                img = filters.rank.median(img.astype(np.uint8), morphology.disk(2))
                img2 = transform.rotate(img2.astype(np.float64), 180)
                img = transform.rotate(img.astype(np.float64), 180)
            p3 = plt.subplot(222)
            p3.imshow(image, cmap="gray")
            for i in range(len(spilte_point)):
                print('Point: ',image[31][22])
                print(spilte_point[i][0], spilte_point[i][1], 'ffff')
                p3.plot(spilte_point[i][0], spilte_point[i][1], 'r.-')
                p3.plot(spilte_point[i][2], spilte_point[i][3], 'r.-')
            # p3.plot(pointx_left,pointy_left,"r.-")
            p3.set_title("滴水算法形成的切割路径")
            p2 = plt.subplot(221)
            p2.imshow(transform.rotate(image.astype(np.float64), 180), cmap="gray")
            p2.set_title(u"藏文粘连字丁串")
            p1 = plt.subplot(224)
            p1.set_title("藏文字丁串分割的左半部分")
            p2.axis('off')
            img = filters.rank.median(img.astype(np.uint8), morphology.disk(2))
            p1.imshow(transform.rotate(img.astype(np.float64),180), cmap = "gray")

            p4 = plt.subplot(223)
            img2 = filters.rank.median(img2.astype(np.uint8), morphology.disk(2))
            p4.imshow(transform.rotate(img2.astype(np.float64),180),cmap = "gray")
            p4.set_title("藏文字丁串分割的右半部分")
            p3.axis('off')
            plt.show()
            # for i in range(len(pointy_left_copy)):
            #     print(image_copy[pointy_left_copy[i]][pointx_left_copy[i]])
            # alter_x = []
            # alter_y = []
            # for i in range(len(pointy_left_copy) - 1):
            #     rr, cc = line(pointy_left_copy[i], pointx_left_copy[i], pointy_left_copy[i+1], pointx_left_copy[i+1])
            #     print(rr)
            #     print(cc)
            #     x, y = alter_point(image_copy, [rr, cc])
            #     if(len(x) > 0 and len(y) > 0):
            #         alter_x.append(x)
            #         alter_y.append(y)
            # for i in range(len(alter_x)):
            #     print(image_copy[alter_x[i]][alter_y[i]])


