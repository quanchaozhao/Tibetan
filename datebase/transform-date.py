#*_* coding :utf-8 *_*

from skimage import io,transform
import os
import numpy as np
import cv2

def transform_image(path):
    tempath = "D:\\database\\character\\touch_character\\three_touch_character_resize\\"
    tempath = "C:\\Users\\Zqc\\Desktop\\标注数据\\image_two_touch\\part30\\"
    tempath = "C:\\Users\\Zqc\\Desktop\\twor\\"
    tempath = r'C:\Users\Zqc\Desktop\test\test'
    for i in os.listdir(path):
        file = os.path.join(path,i)
        image = io.imread(file)
        image = np.where(image > 1, 1, 0)
        # new_image = transform.rescale(image,[5,5]).astype(np.int8)
        row,col = image.shape
        # new_image = transform.resize(image,(row * 3, col * 3), mode = "wrap")
        new_image = cv2.resize(image,(int(col / 3), int(row / 3)), interpolation = cv2.INTER_CUBIC).astype(np.int32)
        tttt = np.zeros((row * 3 + 30,col * 3 + 30))
        tttt[15:3 * row + 15,15: 3 * col + 15] = new_image
        io.imsave(os.path.join(tempath ,os.path.basename(file)) ,(tttt.astype(np.uint16)))
        print("ojk")
def transform_imageMin(path):
    tempath = "D:\\database\\character\\touch_character\\three_touch_character_resize\\"
    tempath = "D:\\藏文识别\\标准数据集\\藏文\\藏文\\base_character\\"
    tempath = r'C:\Users\Zqc\Desktop\test\test'
    for i in os.listdir(path):
        file = os.path.join(path,i)
        image = io.imread(file,as_grey=True)
        # image = np.where(image > 0, 1, 0)
        # new_image = transform.rescale(image,[5,5]).astype(np.int8)
        row,col = image.shape
        new_image = transform.resize(image,(int(row / 3 * 2), int(col / 3 * 2)), mode = "wrap")
        # new_image = cv2.resize(image,(int(col / 2), int(row / 2)), interpolation = cv2.INTER_CUBIC).astype(np.int32)
        io.imsave(tempath + os.path.basename(file) ,((255 * new_image).astype(np.uint16)))
        print("ojk")

if __name__ == "__main__":
    path = "D:\\database\\character\\touch_character\\three_touch_character"
    path = "C:\\Users\\Zqc\\Desktop\\three"
    path = "D:\\藏文识别\\标准数据集\\藏文\\藏文\\基础"
    path = "C:\\Users\\Zqc\\Desktop\\two"
    path = r'C:\Users\Zqc\Desktop\test'
    # transform_imageMin(path)
    transform_image(path)