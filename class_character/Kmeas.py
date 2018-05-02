#coding:utf-8
import numpy as np
import os
from sklearn.cluster import KMeans
from skimage import io,transform
import shutil
path_in = r'D:\database\character\vowel-data'
path_out = r'D:\database\character\class'
def read_file(path):
    data = []
    data_name = []
    print('loading start')
    for file in os.listdir(path):
        file_name = os.path.join(path,file)
        img_tem = io.imread(file_name,as_grey=True)
        row,col = img_tem.shape
        if(row > 100 or col > 100):
            continue
        img_tem = transform.resize(transform.resize(img_tem,(100,100),mode='edge'),(50,50),mode='edge')
        img1 = np.asarray(img_tem).reshape((1,-1))
        data.append(img1.tolist())
        data_name.append(file_name)
        print('loading file:', file_name)
    print('loading finished', 'total: ', len(data))
    return data,data_name
def pre(x):
    str = ''
    for i in range(x):
        str = str + '▆'
    return str
data,name = (read_file(path_in)) #生成一个随机数据，样本大小为100, 特征数为3
data = np.asarray(data).astype(np.float64).reshape(-1,2500)
# 构造一个聚类数为370的聚类器
print('processing image...')
estimator = KMeans(n_clusters=4)#构造聚类器
estimator.fit(data)#聚类
label_pred = estimator.labels_ #获取聚类标签
centroids = estimator.cluster_centers_ #获取聚类中心
inertia = estimator.inertia_ # 获取聚类准则的总和
print('save file starting.....')
for i in range(len(data)):
    index = label_pred[i]
    out = os.path.join(path_out,str(index))
    if not os.path.isdir(out):
        os.mkdir(out)
    shutil.copy(name[i], out)
    if((i+1) % 1000 == 0):
        print('[',pre(int(i / len(data) * 20)),int(i / len(data) * 100),'%]')

print('[',pre(int( 20)),int(100),'%]')