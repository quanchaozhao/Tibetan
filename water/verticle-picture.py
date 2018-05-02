import matplotlib.pyplot as plt
from skimage import io, morphology, measure
import numpy as np
from pylab import figure,mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
NOISE_SIZE_THRESHOLD = 40
def delete_close_area(image):
    row , col = image.shape
    image = image.astype(int)
    image = np.where(image > 244, 0, 1)
    lb_img = measure.label(image,neighbors=4)
    regions = measure.regionprops(lb_img)

    max = np.max(lb_img)
    print("max = ",max )
    flag = np.zeros(max + 1)
    for i in range(1,row - 1,):
        flag[lb_img[i][0]] = flag[lb_img[i][0]] + 1
        flag[lb_img[i][col - 1]] = flag[lb_img[i][col - 1]] + 1

    for i in range(0,col):
        flag[lb_img[0][i]] = flag[lb_img[0][i]] + 1

    for i in range(0,col):
        flag[lb_img[row - 1][i]] = flag[lb_img[row - 1][i]] + 1
    lb = np.where(lb_img > 0, 0, 1)

    for i in range(row):
        for j in range(col):
            if flag[lb_img[i][j]] != 0:
                lb_img[i][j] = 0
    lb_img = np.where(lb_img > 0, 1, 0)
    print(flag)
    return lb_img + lb
#生成二值测试图像
img = io.imread("D:\藏文识别\相关文献\data\Sticky_text\ chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0007_1_015.png")
# img = io.imread("C:\\Users\\Zqc\Desktop\\ttt.bmp",as_grey=True)
import matplotlib.pyplot as plt
from skimage import data,color,morphology,feature
#生成二值测试图像
#检测canny边缘,得到二值图片
# edgs=feature.canny(img, sigma=2, low_threshold=10, high_threshold=10)
# chull = morphology.convex_hull_object(edgs,neighbors=8)
# p1 = plt.subplot(211)
# p1.imshow(img,cmap = "gray")
# p1 = plt.subplot(212)
# p1.imshow(delete_close_area(img),cmap = "gray")

image1 = io.imread("D:\藏文识别\相关文献\data\Sticky_text\ chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0013_0_015.png")
image2 = io.imread("D:\藏文识别\相关文献\data\Sticky_text\ chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0014_0_260.png")
#
# image1 = np.where(image1 > 0, 0, 1)
# image2 = np.where(image2 > 0, 0, 1)

p1 = plt.subplot(121)
p1.imshow(image1, cmap = "gray")
p1.set_title("中部垂直粘连")

p2 = plt.subplot(122)
p2.imshow(image2, cmap = "gray")
p2.set_title("起笔倾斜粘连")

def remove_noise(img):
    # 噪声分为两类，一类是小的像素点，一类是和边框连在一起的
    rows, cols = img.shape
    img_bin = np.where(img >= 0.9, 0, 1)
    img_labeled = measure.label(img_bin)

    regions = measure.regionprops(img_labeled)

    for region in regions:
        region_label = region.label
        minr, minc, maxr, maxc = region.bbox
        # 和边框连接在一起的噪声去除
        if minr == 0 or minc == 0 or maxr >= rows or maxc == cols or region.area < NOISE_SIZE_THRESHOLD or (maxr - minr) < 8:
            # print("****************************************************************************" + str(region.area))
            for point in region.coords:
                row,col = point
                img[row,col] = 1
    return img

# image2 = io.imread("D:\\database\\mark_lines\\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0002_1_1.png")
# image1 = io.imread("D:\藏文识别\相关文献\data\gt_text_lines\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0002_1_1.png",as_grey=True)


# p1 = plt.subplot(211)
#
# image1 = image1[:,0:700]
# image1 = remove_noise(image1)
# image1 = np.where(image1 > 5,1,0)
#
# image2 = image2[:,0:700]
#
#
# p1.imshow(image1, cmap = "gray")
# p1.set_title("原始藏文历史文献行图像")
# p2 = plt.subplot(212)
# p2.imshow(image2, cmap = "gray")
# p2.set_title("预处理提取粘连后的行图像")

p1 = plt.subplot(221)
p2 = plt.subplot(222)
p1.imshow(image1,cmap = "gray")
col,row = image1.shape
h_profile = np.sum(np.where(image1==255,1,0),axis = 0)
# print(image1)

x = range(0,len(h_profile),1)
y1 = np.zeros(row)
y1[:] = col - 1

p1.fill_between(x, (col - h_profile / 2) , y1,color="#2ec3e7")
p1.set_title("藏文历史文献粘连字丁串垂直投影")
print(h_profile)
min_x = np.min(h_profile[int(row / 5): int(row / 5 * 4)])
k = list(h_profile).index(np.min(h_profile[int(row / 5): int(row / 5 * 4)]),int(row / 5), int(row / 5 * 4))
pointx = [k,k]
pointy = [0,col - 1]
p2.imshow(image1,cmap = "gray")
p2.plot(pointx,pointy,"r.-")
p2.set_title("藏文历史文献粘连字丁串切分路径")


p3 = plt.subplot(223)
p4 = plt.subplot(224)
p3.imshow(image2,cmap = "gray")
col,row = image2.shape
h_profile = np.sum(np.where(image2==255,1,0),axis = 0)
# print(image1)

x = range(0,len(h_profile),1)

y2 = np.zeros(row)

y2[:] = col - 1

p3.fill_between(x, (col - (h_profile / 2)), y2,color="#2ec3e7")

print(h_profile)
min_x = np.min(h_profile[int(row / 5): int(row / 5 * 4)])
k = list(h_profile).index(np.min(h_profile[int(row / 5): int(row / 5 * 4)]),int(row / 5), int(row / 5 * 4))
pointx = [k,k]
pointy = [0,col - 1]
p4.imshow(image2,cmap = "gray")
p4.plot(pointx,pointy,"r.-")

plt.show()
