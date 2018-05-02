# coding:utf-8

import os
from skimage import io, transform
from sklearn import svm
from sklearn.linear_model import  LogisticRegression
import numpy as np
from sklearn.externals import joblib
import shutil

path = r'D:\database\character\class'

def load_data(path):
    print('loading starting...')
    data = []
    labels = []
    for curent_path in os.listdir(path):
        if not os.path.isfile(curent_path):
            label = curent_path
            curent_path = os.path.join(path, curent_path)
            for file in os.listdir(curent_path):
                file_name = os.path.join(curent_path, file)
                img_tem = io.imread(file_name, as_grey=True)
                row, col = img_tem.shape
                if (row > 100 or col > 100):
                    continue
                img_tem = transform.resize(transform.resize(img_tem, (100, 100), mode='edge'), (50, 50), mode='edge')
                img1 = np.asarray(img_tem).reshape((1, -1))
                data.append(img1.tolist())
                labels.append(label)
                print('loading file:', file_name)
    return  np.array(data), np.array(labels)

data, labels = load_data(path)
clf = svm.SVC(probability=True)
nsamples,nx,ny = data.shape
clf.fit(data.reshape(nsamples,nx * ny), labels)
joblib.dump(clf,'./SVM_class.pkl')
print('save SVM model:', 'SVM_class.pkl')

