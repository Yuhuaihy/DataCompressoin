import numpy as np
import cv2
from IPython import embed
class JpegEncode(object):
    def __init__(self,fname, block_size=8):
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
``
    def getLuminenceQuantizationMatrix(self,block_size, adjust = None):
        Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14,17, 22, 29, 51, 87, 80, 6],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98,112, 100, 103, 99]])
        if block_size == 16:
            newQ = np.ones((16,16))
            for i in range(8):
                for j in range(8):
                    x1,y1 = 2*i, 2*j
                    x2,y2 = 2+i+1, 2*j
                    x3,y3 = 2*i, 2*j+1
                    x4,y4 = 2+i+1, 2*j+1
                    newQ[x1][y1] =newQ[x2][y2] = newQ[x3][y3] = newQ[x4][y4] = Q[i][j]
            
            Q = newQ
        if not adjust:
            return Q
        else:
            pass


    def level_shift(self, block, block_size):
        sub = 128 * np.ones((block_size,block_size))
        return block - sub
    
    def performDCT(self, block):  # get B
        pass
    
    def getBQ(self, B, Q):
        return np.round(B/Q)
        
if __name__ == '__main__':
    encoder = JpegEncode('test_images/Kodak08gray.bmp')

    