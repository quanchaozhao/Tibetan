# *_* coding:utf-8 *_*


import numpy as np
import os
from skimage import measure, io
def get_isolate_character(image,path):
    lb_image = measure.label(image, connectivity=1)
    regions = measure.regionprops(lb_image)
    totallist = []
    for region in regions:
        totallist.append([region.bbox, region.image.astype(np.int32), 0])


if __name__ == "__main__":
    path = 'D:\藏文识别\相关文献\data\gt_text_lines'
    path2 = 'D:\藏文识别\相关文献\data\Sticky_text\ '
    path3 = 'D:\藏文识别\相关文献\data\marke_Sticky_text\ '

    for i in os.listdir(path):
        file = os.path.join(path,i)
        if file.endswith('.png'):
            image = io.imread(file)
            image = image / 255
            name,type = os.path.basename(file).split('.')
            # process_and_save_photo(path2 + name,image)
            get_isolate_character(image, path2)
