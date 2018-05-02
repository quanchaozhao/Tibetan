from skimage import io
import matplotlib.pyplot as plt
img = io.imread(r"C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total_alter\chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0002_1_01.png",as_grey=True) / 255
plt.subplot(111).imshow(img,cmap='gray')
plt.show()
