# -*- coding:utf-8 -*-
import os
from skimage import io, transform


def transform_file_size(path):
    for i in os.listdir(path):
        file = os.path.join(path,i)
        image = io.imread(file)
        newfile = transform.resize(image,(25,25))
        io.imsave(file, newfile)

if __name__ == "__main__":
    path = "D:/datebase/test/"
    transform_file_size(path)
