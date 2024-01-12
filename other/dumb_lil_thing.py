from math import sqrt
from math import e
from math import pow

v1_coefficient1 = -9/11
v2_coefficient1 = 20/11
v1_coefficient2 = 2/11
v2_coefficient2 = 9/11

v1 = 1
v2 = 0

for i in range(3):
    print("After collision " + str(i + 1))
    v1temp = v1_coefficient1 * v1 + v2_coefficient1 * v2
    v2 = v1_coefficient2 * v1 + v2_coefficient2 * v2
    v1 = abs(v1temp)
    print("v1: " + str(v1))
    print("v2: " + str(v2))
    print()
