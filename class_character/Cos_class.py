# *_8 coding:utf-8 *_8

import os
from shutil import copyfile,rmtree,copytree
import numpy as np
from skimage import io
from skimage import transform
from skimage import util
from sklearn.metrics.pairwise import cosine_similarity
TH = 0.9

def del_file(path):
    for i in os.listdir(path):
        file = os.path.join(path,i)
        image = io.imread(file)
        image = np.where(image > 1,0,1)
        new_image = np.ones((100,100))
        row,col = image.shape
        if(row > 100 or col > 100 ):
            os.remove(file)
            print(file)
# 比较两个图片的余弦相似度
def cosine_similarity_2(img1,img2):

    img1 = np.asarray(img1)
    img2 = np.asarray(img2)

    return cosine_similarity(img1.reshape((1,-1)), img2.reshape((1,-1))).ravel()[0]
def classify_image_by_cosine_similarity(path_in,path_out):
    counter = 0
    sample_img_list = []
    sample_file_name_list = []
    total = len(os.listdir(path_in))
    for i,file_name in enumerate(os.listdir(path_in)):
        img_path = path_in + os.path.sep + file_name
        if not os.path.isdir(img_path):
            img1 = io.imread(img_path, as_grey=True)
            img1 = util.invert(img1)
            img1 = transform.resize(img1, (100, 100),mode="edge")
            for index, img in enumerate(sample_img_list):
                if cosine_similarity_2(img, img1) > TH:
                    sample_file_name_list[index].append(file_name)
                    break
            else:
                img1 = transform.resize(img1, (100, 100),mode="edge")
                sample_img_list.append(img1)
                sample_file_name_list.append([file_name])
                counter += 1
        if i % 10 == 0:
            print("%d of %d" % (i,total))
    k = 0
    for i, file_names in enumerate(sample_file_name_list):

        if len(file_names) < 20:
            k = k + 1
            continue
        out_dir = path_out + os.path.sep + str(i - k)
        os.mkdir(out_dir)
        for file_name in file_names:
            src = path_in + os.path.sep + file_name
            dst = out_dir + os.path.sep + file_name
            copyfile(src, dst)
    return sample_img_list
if __name__ == "__main__":
    print("fff")
    # tttt.falter_image("D:\\datebase\\isolate_div\\2")
    # del_file("D:\\datebase\\character\\isolate_character")
    classify_image_by_cosine_similarity(path_in = "D:\\database\\character\\isolate_character_1",path_out = "D:\\database\\3")

