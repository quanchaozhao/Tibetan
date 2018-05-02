#  **** coding:utf-8 ****

import xml.dom.minidom as mindom
import re
from xml.etree import ElementTree
from xml.etree import ElementTree as ET
import os

def mains():
    XmlName = "abc.xml"
    dom = mindom.parse(XmlName)
    root = dom.documentElement

    maxid = root.getElementsByTagName("maxid")
    print(maxid[0].nodeName,maxid[0].nodeValue)

    login = root .getElementsByTagName("login")
    item = login[0]

    un = item.getAttribute("username")
    print(un)

    xml = open(XmlName,encoding="utf-8").read()
    xmls = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", xml)
    root = ElementTree.fromstring(xmls)
    contents = root[2]
    p = contents.findall('./item')
    for oneper in p:
        for child in oneper.getchildren():
            print(child.tag,':',child.text)


def readXml(file):
    text = open(file).read()
    # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
    root = ET.fromstring(text)
    point_x , point_y = [],[]
    for i,textRegion in enumerate(root[1]):
        listx = []
        listy = []
        for j,pnt in enumerate(textRegion[0][:-1]):
            x = int(pnt.attrib['x'])
            y = int(pnt.attrib['y'])
            listx.append(x)
            listy.append(y)
            point_x.append(x)
            point_y.append(y)

    fileName = root[1].attrib['imageFilename']
    imageHeight = root[1].attrib['imageHeight']
    imageWidth = root[1].attrib['imageWidth']
    print(fileName, ' ',imageHeight, ' ',imageWidth)
    return fileName,[imageHeight,imageWidth]

def alterXml(fileName,info):

    imageHeight, imageWidth,pointx,pointy = info
    print(imageHeight, imageWidth)
    tt,ss = 12,3
    root = ET.Element('root',{'Author':'Quanchao Zhao','Email':'quanchaozhao@yeah.net'})
    pg = ET.SubElement(root,'Page',attrib = {'imageHeight':imageHeight,'imageWidth':imageWidth})
    for i in range(len(pointx)):
        textRegion = ET.SubElement(pg,'textRegion')
        ET.SubElement(textRegion,'Coords',attrib = {'pointx':('%d'%tt),'pointy':('%d'%ss)})
    tree = ET.ElementTree(root)
    tree.write(fileName.split('.')[0] + '.xml',encoding = 'utf-8',xml_declaration = True)
    pass
def alter_point(image,point):
    temx,temy = [],[]
    pointx,pointy = point
    if(image[pointx[0]][pointy[0]] == 1):
        temx.append(pointx[0])
        temy.append(pointy[0])
    for i in range(1,len(pointx) - 1,1):
        if(image[pointx[i - 1]][pointy[i - 1]] == 0 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][pointy[i + 1]] == 1) and \
                (image[pointx[i - 1]][pointy[i - 1]] == 1 and image[pointx[i]][pointy[i]] == 1 and image[pointx[i + 1]][ pointy[i + 1]] == 0):
            temx.append(pointx[i])
            temy.append(pointy[i])
    if (image[pointx[-1]][pointy[-1]] == 1):
        temx.append(pointx[-1])
        temy.append(pointy[-1])
    return temx,temy
if __name__ == "__main__":
    fileName,ss = readXml("chos lugs-pan chen blo chos kyi rgyal mtshan gsung 'bum-1-0003_1_426_anonymous@unknown.com.xml")
    alterXml(fileName,[ss[0],ss[1],[1,2],[2,3]])
