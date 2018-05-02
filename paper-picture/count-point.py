# coding:utf-8

import os
from xml.etree import ElementTree as ET

from skimage import io

path_two_xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\AddBaseLine'
path_three_xml = r'C:\Users\Zqc\Desktop\mark\第二次数据-寒假\total-three\total-addbaseline'


def get_part_image(path):
    count_file = 0
    count_above_baseline = 0
    count_on_baseline = 0
    count_below_baseline = 0
    count_path = 0
    for i in os.listdir(path):
        XmlFile = os.path.join(path, i)
        if XmlFile.endswith('.xml'):
            count_file = count_file + 1
            text = open(XmlFile, 'r', encoding='UTF-8').read()
            # text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
            root = ET.fromstring(text)
            imageFilename = root[-1].attrib['ImageFileName']
            baseline = int(root[-1].attrib['BaseLine'])
            # print('get file: ', imageFilename)
            textRegion = root[-1][0]
            for i in range(len(root[-1])):
                textRegion = root[-1][i]
                if (len(textRegion[0]) > 2):
                    count_path = count_path + 1
                for j in range(0, len(textRegion[0]), 2):
                    y = int(textRegion[0][j].attrib['y']) / 2
                    y = y + int(textRegion[0][j + 1].attrib['y']) / 2
                    if (abs(y - baseline) <= 5):
                        count_on_baseline = count_on_baseline + 1
                    elif (y - baseline > 5):
                        count_below_baseline = count_below_baseline + 1
                    elif (baseline - y > 5):
                        count_above_baseline = count_above_baseline + 1

    return count_file, count_path, count_above_baseline, count_on_baseline, count_below_baseline


count_file, count_path, count_above_baseline, count_on_baseline, count_below_baseline = get_part_image(path_two_xml)

total = count_above_baseline + count_on_baseline + count_below_baseline
print('two total file: ', count_file)
print('two total path: ', count_path, 'ratio: ', '%.2f' % (count_path / count_file))
print('two total point: ', total, 'ratio: ', '%.2f' % (total / count_file))

# print('two above baseline: ', count_above_baseline, 'ratio: ', '%.2f' % (count_above_baseline / total * 100), '%')
# print('two on baseline: ', count_on_baseline, 'ratio: ', '%.2f' % (count_on_baseline / total * 100), '%')
# print('two below baseline: ', count_below_baseline, 'ratio: ', '%.2f' % (count_below_baseline / total * 100), '%')

count_file2, count_path2, count_above_baseline2, count_on_baseline2, count_below_baseline2 = get_part_image(
    path_three_xml)
total2 = count_above_baseline2 + count_on_baseline2 + count_below_baseline2

print('three total file: ', count_file2)
print('three total path: ', count_path2, 'ratio: ', '%.2f' % (count_path2 / count_file2))
print('three total point: ', total2, 'ratio: ', '%.2f' % (total2 / count_file2))
# print('three above baseline: ', count_above_baseline2, 'ratio: ', '%.2f' % (count_above_baseline2 / total2 * 100), '%')
# print('three on baseline: ', count_on_baseline2, 'ratio: ', '%.2f' % (count_on_baseline2 / total2 * 100), '%')
# print('three below baseline: ', count_below_baseline2, 'ratio: ', '%.2f' % (count_below_baseline2 / total2 * 100), '%')

total2 = count_above_baseline + count_on_baseline + count_below_baseline + count_above_baseline2 + count_on_baseline2 + count_below_baseline2
count_above_baseline = count_above_baseline + count_above_baseline2
count_on_baseline = count_on_baseline + count_on_baseline2
count_below_baseline = count_below_baseline + count_below_baseline2
count_file = count_file + count_file2
count_path = count_path + count_path2

print('total file: ', count_file)
print('total path: ', count_path, 'ratio: ', '%.2f' % (count_path2 / count_file2))
print('total point: ', total2, 'ratio: ', '%.2f' % (total2 / count_file))
# print('above baseline: ', count_above_baseline, 'ratio: ', '%.2f' % (count_above_baseline / total2 * 100), '%')
# print('on baseline: ', count_on_baseline, 'ratio: ', '%.2f' % (count_on_baseline / total2 * 100), '%')
# print('below baseline: ', count_below_baseline, 'ratio: ', '%.2f' % (count_below_baseline / total2 * 100), '%')
