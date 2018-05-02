# coding:utf-8
import xml.etree.cElementTree as ET
import os
import numpy as np
from skimage import draw, io
from skimage import util
import matplotlib.pyplot as plt

IMG_FOLDER = r"D:\img_in_2"
GT_FOLDER = r"D:\gt_text_in_2"
GT_DATA_FOLDER = r'D:\gt_data_2'
LINE_OUTPUT_FOLDER = r'D:\gt_text_lines'

BLUE = [255,0,0]

def make_gt_from_file_2(gt_name, img, channel=1):

    cols,rows = img.shape
    with open(gt_name, encoding="gb2312") as f:
        file = "".join(f.readlines())
    rows, cols = img.shape
    root = ET.fromstring(file)
    lines = []

    for i, textRegion in enumerate(root[1]):
        line = []
        for pnt in textRegion[0][:-1]:
            x = int(pnt.attrib['x'])
            x = 0 if x < 0 else x
            x = cols if x > cols else x
            y = int(pnt.attrib['y'])
            y = 0 if y < 0 else y
            y = rows if y > rows else y
            line.append([x, y])
        lines.append(line)

    line2 = np.asanyarray(lines)
    if channel > 1:
        gt_img = np.ones((rows,cols,3),dtype=np.uint8)*255
    else:
        gt_img = np.zeros((rows,cols),dtype=np.uint8)

    for i in range(1, len(line2) - 1):
        last_pnt = None
        for pnt in line2[i]:
            start_pnt = last_pnt
            end_pnt = pnt
            if last_pnt is None:
                if pnt[0] > 0:
                    start_pnt = [0,pnt[1]]
                    end_pnt = pnt
            last_pnt = end_pnt
            rr,cc = draw.line(start_pnt[1],start_pnt[0],end_pnt[1],end_pnt[0])
            if channel > 1:
                gt_img[rr, cc] = BLUE
            else:
                gt_img[rr, cc] = 1

        else:
            if last_pnt[0] < cols:
                rr, cc = draw.line(last_pnt[1],last_pnt[0],last_pnt[1],cols-1)
                if channel > 1:
                    gt_img[rr, cc] = BLUE
                else:
                    gt_img[rr, cc] = 1

    # io.imshow(gt_img)
    # io.show()
    return gt_img


def make_ground_truth_from_folder(img_folder=IMG_FOLDER,gt_folder=GT_FOLDER,gt_data_folder=GT_DATA_FOLDER):
    img_file_names = os.listdir(img_folder)

    for img_file_name in img_file_names:
        file_base_name = os.path.splitext(img_file_name)[0]
        print(file_base_name)
        gt_name = "%s_anonymous@unknown.com.xml" % file_base_name
        img_full_name = os.path.join(img_folder,img_file_name)
        gt_full_name = os.path.join(gt_folder,gt_name)

        try:
            with open(gt_full_name,encoding="gb2312") as f:
                file = "".join(f.readlines())
        except UnicodeDecodeError:
            with open(gt_full_name,encoding="utf-8") as f:
                file = "".join(f.readlines())
        img = io.imread(img_full_name, as_grey=True)
        img_org = img.copy()
        img = util.invert(img)
        rows, cols = img.shape
        root = ET.fromstring(file)
        lines = []
        for i, textRegion in enumerate(root[1]):
            line = []
            for j,pnt in enumerate(textRegion[0][:-1]):
                x = int(pnt.attrib['x'])
                x = 0 if x < 0 else x
                x = cols if x > cols else x
                y = int(pnt.attrib['y'])
                y = 0 if y < 0 else y
                y = rows if y > rows else y
                if x > 0 and j == 0:
                    line.append([0,y])
                line.append([x, y])
                if x < cols-1 and j == len(textRegion[0][:-1])-1:
                    line.append([cols-1,y])
            lines.append(line)

        line2 = np.asanyarray(lines)

        gt_img = np.zeros(img.shape)

        for i in range(len(line2) - 1):
            line_top = np.asarray(line2[i])
            if i == 0:
                line_top = np.asarray([[0,0],[cols-1,0]])
            line_bottom = np.asarray(line2[i + 1])[::-1]
            if i == len(line2) - 2:
                line_bottom = np.asarray([[cols-1,rows-1],[0,rows-1]])
            line_polygon = np.vstack((line_top, line_bottom))
            r = line_polygon[:, 1]
            c = line_polygon[:, 0]
            img_s = np.zeros((rows, cols), np.bool)
            rr, cc = draw.polygon(r, c)
            img_s[rr, cc] = True
            gt_img[rr, cc] = i + 2
            img2 = np.where(img_s, img, 0)

        gt_file_full_path = os.path.join(gt_data_folder,file_base_name)
        print("总行数 %d " % len(lines))
        np.save(gt_file_full_path + ".npy", np.asarray([gt_img, len(line2)], dtype=object))
        # plt.imshow(gt_img,alpha=0.7)
        # plt.imshow(img_org,alpha=0.3)
        # plt.show()
    pass

def export_line_2_file(img_folder=IMG_FOLDER,gt_folder=GT_FOLDER,gt_data_folder=GT_DATA_FOLDER):
    img_file_names = os.listdir(img_folder)
    for img_file_name in img_file_names:
        file_base_name = os.path.splitext(img_file_name)[0]
        print(file_base_name)
        gt_name = "%s_anonymous@unknown.com.xml" % file_base_name
        img_full_name = os.path.join(img_folder, img_file_name)
        gt_full_name = os.path.join(gt_folder, gt_name)

        try:
            with open(gt_full_name, encoding="gb2312") as f:
                file = "".join(f.readlines())
        except UnicodeDecodeError:
            with open(gt_full_name, encoding="utf-8") as f:
                file = "".join(f.readlines())
        img = io.imread(img_full_name, as_grey=True)
        img_org = img.copy()
        img = util.invert(img)
        rows, cols = img.shape
        root = ET.fromstring(file)
        lines = []

        for i, textRegion in enumerate(root[1]):
            line = []
            for j,pnt in enumerate(textRegion[0][:-1]):
                x = int(pnt.attrib['x'])
                x = 0 if x < 0 else x
                x = cols if x > cols else x
                y = int(pnt.attrib['y'])
                y = 0 if y < 0 else y
                y = rows if y > rows else y
                if x > 0 and j == 0:
                    line.append([0,y])
                line.append([x, y])
                if x < cols-1 and j == len(textRegion[0][:-1])-1:
                    line.append([cols-1,y])
            lines.append(line)

        line2 = np.asanyarray(lines)

        for i in range(len(line2) - 1):
            line_top = np.asarray(line2[i])
            if i == 0:
                line_top = np.asarray([[0, 0], [cols - 1, 0]])
            line_bottom = np.asarray(line2[i + 1])[::-1]
            if i == len(line2) - 2:
                line_bottom = np.asarray([[cols - 1, rows - 1], [0, rows - 1]])
            line_polygon = np.vstack((line_top, line_bottom))
            r = line_polygon[:, 1]
            c = line_polygon[:, 0]
            img_s = np.zeros((rows, cols), np.bool)
            rr, cc = draw.polygon(r, c)
            img_s[rr, cc] = True
            img2 = np.where(img_s, img, 0)
            profile_h = np.sum(img2,axis=1)

            start_row,end_row = 0,0
            for j in range(len(profile_h)-1):
                if profile_h[j] == 0 and profile_h[j+1]>0:
                    start_row = j
                    break
            for j in range(len(profile_h)-1,1,-1):
                if profile_h[j] == 0 and profile_h[j-1]>0:
                    end_row = j

            print(start_row,end_row)
            imgo = img2[start_row:end_row,:]

            try:
                io.imsave(os.path.join(LINE_OUTPUT_FOLDER,"%s_%d.png"%(file_base_name,i)),np.bitwise_not(imgo))
            except Exception as es:
                print(os.path.join(LINE_OUTPUT_FOLDER,"%s_%d.png"%(file_base_name,i))+"~~~~~~~~~~~~~~~~~~")
    pass

if __name__ == '__main__':

    # export_line_2_file()
    make_ground_truth_from_folder()
    # img = io.imread("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0011_0.jpg",as_grey=True)
    # make_gt_from_file_2("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0011_0_anonymous@unknown.com.xml",img)


