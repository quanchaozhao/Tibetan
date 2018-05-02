# coding:utf-8

import numpy as np
import os
from sklearn.cluster import KMeans
from skimage import io,transform
from sklearn.externals import joblib
import shutil
path_in = r'D:\database\test_out\3'
path_out = r'D:\database\test'

def read_file(path,bypath = True):
    print('loading file')
    if(not bypath):
        img_tem = io.imread(path, as_grey=True)
        row, col = img_tem.shape
        if (row > 100 or col > 100):
            return []
        img_tem = transform.resize(transform.resize(img_tem, (100, 100), mode='edge'), (50, 50), mode='edge')
        img1 = np.asarray(img_tem).reshape((1, -1))
        return img1.tolist(),path


estimator = joblib.load('./km.pkl')
print('start classing....')
for file in os.listdir(path_out):
    data_tem,nam = read_file(os.path.join(path_out,file),bypath=False)
    print(file, ':', estimator.predict(data_tem),'pro',estimator.predict_proba(data_tem))
