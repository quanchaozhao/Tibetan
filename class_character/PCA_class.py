# -*- coding: utf-8 -*-
from PCV.tools import imtools
import pickle
from scipy import *
from pylab import *
from PIL import Image
from scipy.cluster.vq import *
from PCV.tools import pca
import os
from skimage import io
def falter_image(path):
    for i in os.listdir(path):
        file = os.path.join(path,i)
        image = io.imread(file)
        image = np.where(image > 1,0,1)
        new_image = np.ones((100,100))
        row,col = image.shape
        new_image[0:row,0:col] = image
        io.imsave(file,(new_image * 255).astype(np.int))
# Uses sparse pca codepath.
# imlist = imtools.get_imlist('C:/Users/Zqc/Desktop/PCV-book-data/data/selectedfontimages/a_selected_thumbs/')

# falter_image("D:/datebase/test11")

imlist = imtools.get_imlist('D:/datebase/test11/')
print(imlist)
# 获取图像列表和他们的尺寸
im = array(Image.open(imlist[0]))  # open one image to get the size
m, n = im.shape[:2]  # get the size of the images
imnbr = len(imlist)  # get the number of images
print("The number of images is %d" % imnbr)

# Create matrix to store all flattened images
immatrix = array([array(Image.open(imname)).flatten() for imname in imlist], 'f')

# PCA降维
V, S, immean = pca.pca(immatrix)

# 保存均值和主成分
#f = open('./a_pca_modes.pkl', 'wb')
# f = open('C:/Users/Zqc/Desktop/PCV-book-data/data/selectedfontimages/a_pca_modes.pkl', 'wb')

f = open('D:/datebase/a_pca_modes.pkl', 'wb')

pickle.dump(immean,f)
pickle.dump(V,f)
f.close()


# get list of images
# imlist = imtools.get_imlist('C:/Users/Zqc/Desktop/PCV-book-data/data/selectedfontimages/a_selected_thumbs/')
imlist = imtools.get_imlist('D:/datebase/test11/')
imnbr = len(imlist)
# load model file
# with open('C:/Users/Zqc/Desktop/PCV-book-data/data/selectedfontimages/a_pca_modes.pkl','rb') as f:
with open('D:/datebase/a_pca_modes.pkl','rb') as f:
    immean = pickle.load(f)
    V = pickle.load(f)
# create matrix to store all flattened images
immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')

# project on the 40 first PCs
immean = immean.flatten()
projected = array([dot(V[:40],immatrix[i]-immean) for i in range(imnbr)])

# k-means
projected = whiten(projected)
centroids,distortion = kmeans(projected,370)
code,distance = vq(projected,centroids)

filepath  = 'D:/datebase/1'
# plot clusters
for k in range(370):
    tempath = filepath + "/" + str(k)
    os.makedirs(tempath)
    ind = where (code == k)[0]
    for i in range(len(ind)):
        io.imsave(tempath + "/" + str(i) + ".png",immatrix[ind[i]].reshape((100,100)).astype(np.uint8),cmap = "gray")

#     ind = where(code==k)[0]
#     figure()
#     gray()
#     for i in range(minimum(len(ind),40)):
#         subplot(4,20,i+1)
#         imshow(immatrix[ind[i]].reshape((82,82)))
#         axis('off')
# show()