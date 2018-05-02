import numpy as np
probability = [1,2,3,43,25]
p1 = np.where(probability == np.max(probability))
print(p1[0][0])