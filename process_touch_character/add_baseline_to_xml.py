# 8_8 coding:utf-8 8_8

import os
from xml.etree import ElementTree as ET

updateTree = ET.parse('123.xml')
root = updateTree.getroot()
page = root[-1]
page.set('BaseLine', str(12))
updateTree.write('234.xml', encoding='utf-8', xml_declaration=True)

baselinefile = r'base_line.txt'
file = open(baselinefile, 'r')
line = file.readline()[:-1]
Path = r"C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine"
AlterPath = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine1'
while (line != None):
    xmlname, base_line = line.split(',')
    print(xmlname, base_line)
    xmlname = xmlname.replace('png', 'xml')

    XML = os.path.join(Path, xmlname)
    updateTree = ET.parse(XML)
    root = updateTree.getroot()
    page = root[-1]
    # page.set('BaseLine', base_line

    Class = page.attrib['class']
    ImageFileName = page.attrib['imageFilename']
    ImageHeight = page.attrib['imageHeight']
    ImageWidth = page.attrib['imageWidth']
    ImageStrokeWidth = page.attrib['strokeWidth']
    BaseLine = int(page.attrib['BaseLine'])
    if((BaseLine) > 2):
        BaseLine = BaseLine + 1
    # del page.attrib['BaseLine']
    # del page.attrib['class']
    # del page.attrib['imageFilename']
    # del page.attrib['imageHeight']
    # del page.attrib['imageWidth']
    # del page.attrib['strokeWidth']

    page.set("ImageFileName", ImageFileName)
    page.set("Class", Class)
    page.set("ImageHeight", ImageHeight)
    page.set("ImageWidth", ImageWidth)
    page.set("ImageStrokeWidth", ImageStrokeWidth)
    page.set("BaseLine", str(BaseLine))

    root1 = ET.Element('root', {'Author': 'Quanchao Zhao', 'Email': 'quanchaozhao@yeah.net'})
    pg = ET.SubElement(root1, 'Page',
                       attrib={'ImageFileName': ImageFileName, 'ImageHeight': ImageHeight, 'ImageWidth': ImageWidth,
                               'Class': Class, 'ImageStrokeWidth': '8', "BaseLine": str(BaseLine)})

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

    for i in range(len(total_x)):
        textRegion = ET.SubElement(pg, 'TextRegion')
        coods = ET.SubElement(textRegion, 'Coords')
        for j in range(len(total_x[i])):
            ET.SubElement(coods, 'Point', attrib={'x': str(total_x[i][j]), 'y': str(total_y[i][j])})
    tree = ET.ElementTree(root1)
    tree.write(os.path.join(AlterPath, xmlname), encoding='utf-8', xml_declaration=True)

    # updateTree.write(os.path.join(AlterPath, xmlname), encoding='utf-8', xml_declaration=True)
    line = file.readline()[:-1]
