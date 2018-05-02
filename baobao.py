# coding:utf-8

import matplotlib.pylab as plt
import numpy as np

np.seterr(divide='ignore', invalid='ignore')


def ssqut(nums):
    for i in range(len(nums)):
        flag = False
        if (nums[i] < 0):
            nums[i] = np.sqrt(-nums[i])
            flag = True
            print('ddddddddd')
        else:
            nums[i] = np.sqrt(nums[i])
        # if (flag):
        #     nums[i] = - nums[i]
    return nums


fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111)
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

h1 = np.arange(0, 1e-06, 0.00000000001)
h2 = h1 / (16 + h1 * h1)
# f = -ssqut((h2 * h2 * h2 - 2 * ssqut(h1) * h2 * h2 * ssqut(h2) +
#             h1 * h2 * h2 + h1 * h1 * h2 * ssqut(h2))) / h2
# f = -ssqut(((256 * h1 * h1 * h1 * (16 * h1 * h1 + 1)) + 128 * ssqut(h1 * h1 * h1
#                                                                     * h1 * h1 * h1 * h1 * h1 * h1) + 16 * h1 * h1 * h1 * h1 * h1 * h1) / (
#                        (16 * h1 * h1 + 1) * (16 * h1 * h1 + 1) * (16 * h1 * h1 + 1)))
# f = ssqut(162 * h1 * h1 * h1 + h1)
f = ssqut((-h1) / (4 * h1 * h1 * h1 - 1))
# f = ssqut(1 + 4 * h1 * h1)
plt.plot(h1, f)
t = (256 * h1 * h1 * h1 * (16 * h1 * h1 + 1))
# f = ssqut(((256 * h1 * h1 * h1 * (16 * h1 * h1 + 1)) + 128 * ssqut(h1 * h1 * h1
#                                                                    * h1 * h1 * h1 * h1 * h1 * h1) + 16 * h1 * h1 * h1 * h1 * h1 * h1) / (
#                       (16 * h1 * h1 + 1) * (16 * h1 * h1 + 1) * (16 * h1 * h1 + 1)))
# f = -ssqut(162 * h1 * h1 * h1 + h1)
# f = -ssqut(1 + 4 * h1 * h1)
f = -ssqut((-h1) / (4 * h1 * h1 * h1 - 1))
plt.plot(h1, f)
plt.ylabel('fT')
plt.xlabel('h2')

x = [0, 1, 0.000001]
for i in x:
    if (i * i * i - 0.25 < 0.00001):
        print('i = : ', i)
plt.show()
