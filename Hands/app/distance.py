import numpy as np

a = np.array([-0.0069, -0.0022])
#b = np.array([-0.0176, 0.0020])
c = np.array([-0.0287, 0.0181])

#dist = ((a[0] - c[0])*(a[0] - c[0]) + (a[1] - c[1])*(a[1] - c[1]))
dist = np.linalg.norm(a - c)
print(dist)