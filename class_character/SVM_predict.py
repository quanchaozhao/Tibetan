# coding:utf-8

import os
from skimage import io, transform
from matplotlib import pyplot as plt
import numpy as np
from sklearn.externals import joblib

path = r'D:\database\character\pre'
clf = joblib.load(r'D:\pycharm\C-Process-photo\class_character\SVM_class.pkl')
def get_class_and_ratio(image):
    img_tem = image
    data = []
    row, col = img_tem.shape
    if (row > 100 or col > 100):
        return []
    img_tem = transform.resize(transform.resize(img_tem, (100, 100), mode='edge'), (50, 50), mode='edge')
    img1 = np.asarray(img_tem).reshape((1, -1))
    data.append(img1.tolist())
    data = np.array(data)
    nsample, nx, ny = data.shape
    data = data.reshape(nsample, nx * ny)
    probability = clf.predict_proba(data)[0]
    for i in range(len(probability)):
        probability[i] = round(probability[i],3)
    index = np.where(probability == np.max(probability))[0][0]
    row,col = image.shape
    if(np.max(probability) < 0.85 or row / col > 2):
        # print(probability, row, col, row/col)
        return 0,0
    else:
        return np.max(probability),index

def loda_file(file_name):
    data = []
    img_tem = io.imread(file_name, as_grey=True)
    row, col = img_tem.shape
    if (row > 100 or col > 100):
        return []
    img_tem = transform.resize(transform.resize(img_tem, (100, 100), mode='edge'), (50, 50), mode='edge')
    img1 = np.asarray(img_tem).reshape((1, -1))
    data.append(img1.tolist())
    return np.array(data)
if __name__ == "__main__":
    for curent_path in os.listdir(path):
        absolute_file_name = os.path.join(path, curent_path)
        data = loda_file(absolute_file_name)
        nsample,nx,ny = data.shape
        data = data.reshape(nsample,nx * ny)
        probability = clf.predict_proba(data)[0]
        for i in range(len(probability)):
            probability[i] = round(probability[i],3)
        index = np.where(probability == np.max(probability))[0][0]
        img = io.imread(absolute_file_name)
        row,col = img.shape
        if(np.max(probability) < 0.986 or row / col > 1.3):
            index = 'not vowel'
            continue
        print(probability, 'MAX_porba = ', index + 1)
        p1 = plt.subplot(111)
        p1.imshow(img)
        p1.set_title('lable: '+ str(index))
        print(absolute_file_name)
        plt.show()


