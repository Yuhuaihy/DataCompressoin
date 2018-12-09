import numpy as np
from numpy import pi
from numpy import cos
import math

class DCTManipulation:
    def dct_point(self, u, v, n):
        if u == 0:
            return math.sqrt(1 / n)
        else:
            return math.sqrt(2 / n) * cos(((2 * v + 1) * u * pi) / (2 * n))

    def __init__(self, n):
        self.dct = np.zeros((n,n))

        for i in range(0, 8):
            for j in range(0, 8):
                self.dct[i, j] = self.dct_point(i, j, 8)

        self.dctTran = self.dct.transpose()

    def dct2(self, matrix):
        dctMatrix = np.matmul(self.dct, matrix)
        dctMatrix = np.matmul(dctMatrix, self.dctTran)
        return dctMatrix


    def i_dct2(self, matrix):
        dctMatrix = np.matmul(self.dctTran, matrix)
        dctMatrix = np.matmul(dctMatrix, self.dct)
        return dctMatrix


