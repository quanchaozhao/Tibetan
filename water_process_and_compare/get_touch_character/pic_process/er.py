import numpy as np

s = [(1,3),(2,4),(4,6)]

l = np.array(s)

st = l[np.where(l > 4,True,False)]


ss = np.where([[True, False], [False, True]],
              [[1, 2], [3, 4]],
              [[9, 8], [7, 6]])

print(ss)