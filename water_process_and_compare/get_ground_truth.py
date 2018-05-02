# coding:utf-8

import os
from xml.etree import ElementTree as ET

ground_truth_file = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\result\ground-truth\ground_truth_two.txt'
path_Xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine'

ground_truth_file = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\result\ground-truth\ground_truth_three.txt'
path_Xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total-three\total-addbaseline'

def get_part_image():
    ground_truth = open(ground_truth_file, 'w')
    for i in os.listdir(path_Xml):
        XmlFile = os.path.join(path_Xml, i)
        if XmlFile.endswith('.xml'):
            text = open(XmlFile, 'r', encoding='UTF-8').read()
            # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
            root = ET.fromstring(text)
            imageFilename = root[-1].attrib['ImageFileName']
            print('get file: ', imageFilename)
            total_x, total_y = [], []
            point_x, point_y = [], []
            for i, textRegion in enumerate(root[-1]):
                listx = []
                listy = []
                if (len(textRegion[0]) % 2 == 0):
                    index = len(textRegion[0])
                else:
                    index = -1
                for j, pnt in enumerate(textRegion[0][:index]):
                    x = int(pnt.attrib['x'])
                    y = int(pnt.attrib['y'])
                    listx.append(x)
                    listy.append(y)
                    point_x.append(x)
                    point_y.append(y)
                total_x.append(listx)
                total_y.append(listy)
            ground_truth.write(imageFilename + ',')
            for i in range(len(total_x)):
                for j in range(0, len(total_x[i]), 2):
                    ground_truth.write(
                        str(total_x[i][j]) + ' ' + str(total_y[i][j]) + ' ' + str(total_x[i][j + 1]) + ' ' +
                        str(total_y[i][j + 1]) + ',')
            ground_truth.write('\n')
    ground_truth.close()


get_part_image()
