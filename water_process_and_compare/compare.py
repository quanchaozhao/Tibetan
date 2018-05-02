# coding:utf-8
import numpy as np

ground_truth = r'ground_truth_two.txt'
result = r'result-water.txt'
result = r'result_outline_423_two.txt'
#
# ground_truth = r'ground_truth_three.txt'
# result = r'result-water.txt'
# result = r'result_outline_423_three.txt'

# result = r'result.txt'
ratio = 1.5
stroke = 8


# def judge_point(point_result,point_ground_truth):
#     x = point_result[0] - point_ground_truth[0]
#     y = point_result[1] - point_result[1]
#     np.power(x,x) + np.power(y,y) < np.power(stroke * 1.5, stroke * 1.5)
def pre(x):
    str = ''
    for i in range(x):
        str = str + '▆'
    return str


def remove(points, point):
    new_point = []
    for i in range(len(points)):
        # print(points[i][0],',',points[i][1])
        if not (points[i][0] == point[0] and points[i][1] == point[1]):
            new_point.append(points[i])
    return new_point


ground_truth_read = open(ground_truth, 'r')
record_truth = ground_truth_read.readline()
dir_truth = {}
dir_result = {}
count_truth = 0
count_result = 0
count = 0
tt = 0
# 读取ground truth中数据
print('reading ground_truth...')
while (record_truth):
    record_truth = record_truth[:-2].split(',')
    if (len(record_truth) > 2):
        tt = tt + 1
    # print(record_truth)
    value = []
    for i in range(len(record_truth) - 1):
        point = record_truth[i + 1].split(' ')
        value.append([int((int(point[0]) + int(point[2])) / 2), int((int(point[1]) + int(point[3])) / 2)])
        count_truth = count_truth + 1
    dir_truth[record_truth[0]] = value
    record_truth = ground_truth_read.readline()
ground_truth_read.close()

print("reading outline...")
# 读取切分结果中的数据
result_read = open(result, 'r')
result_file = result_read.readline()
while (result_file):
    result_file = (result_file[:-2]).split(',')
    # print(result_file)
    value = []
    for i in range(len(result_file) - 1):
        point = result_file[i + 1].split(' ')
        value.append([int((int(point[0]) + int(point[2])) / 2), int((int(point[1]) + int(point[3])) / 2)])
        count_result = count_result + 1
    dir_result[result_file[0]] = value
    result_file = result_read.readline()
result_read.close()

# print(dir_truth)
# print(dir_result)
print('Total points of ground truth: ', count_truth, 'tt: ', tt)
print('Total points of outline-algorithm: ', count_result)
for (k, v) in dir_result.items():
    for point_result in v:
        val = dir_truth.get(k, 'default_value')
        if val == 'default_value':
            continue
        for point_ground_truth in dir_truth[k]:
            x = point_result[0] - point_ground_truth[0]
            y = point_result[1] - point_ground_truth[1]
            # print(point_result, point_ground_truth, ':', np.sqrt(x * x + y * y), '--', stroke * 2)
            if (np.sqrt(x * x + y * y) < stroke * 1.4):
                count = count + 1
                tem = remove(dir_truth[k], point_ground_truth)
                dir_truth[k] = tem
                break

print('Correct points: ', count)
print('Precision rate: [', pre(int(count / count_truth * 20)), count / count_truth * 100, '%]')
