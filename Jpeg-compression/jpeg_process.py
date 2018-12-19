import numpy as np
import cv2
from IPython import embed
import math
import pickle
import sys
class JpegProcess(object):
    def __init__(self,fname, adjust = 1):
        self.adjust = adjust
        self.image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE).astype(int)

    def getLuminenceQuantizationMatrix(self,block_size, adjust = 1, reverse = False):
        Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14,17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98,112, 100, 103, 99]])
        if block_size == 16:
            newQ = np.ones((16,16), dtype = int)
            for i in range(8):
                for j in range(8):
                    x1,y1 = 2*i, 2*j
                    x2,y2 = 2+i+1, 2*j
                    x3,y3 = 2*i, 2*j+1
                    x4,y4 = 2+i+1, 2*j+1
                    newQ[x1][y1] =newQ[x2][y2] = newQ[x3][y3] = newQ[x4][y4] = Q[i][j]
            
            Q = newQ
        
        return np.multiply(self.adjust,Q) if not reverse else np.multiply(adjust,Q)

    def dct_point(self, u, v, n):
        if u == 0:
            return math.sqrt(1 / n)
        else:
            return math.sqrt(2 / n) * math.cos(((2 * v + 1) * u * math.pi) / (2 * n))
    
    def dct_trans(self, n):
        self.dct = np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                self.dct[i,j] = self.dct_point(i, j, n)
        self.dctTran = self.dct.transpose()  


    def level_shift(self, block, block_size):
        sub = 128 * np.ones((block_size,block_size))
        return block - sub
    
    def reverse_level_shift(self, block, block_size):
        sub = 128 * np.ones((block_size,block_size))
        return block + sub

    
    def performDCT(self, block):  # get B
        n,n = block.shape
        self.dct_trans(n)
        dctMatrix = np.matmul(self.dct, block)
        dctMatrix = np.matmul(dctMatrix, self.dctTran)
        return dctMatrix.round(4)
    
    def reverseDCT(self, block):
        n,n = block.shape
        self.dct_trans(n)
        dctMatrix = np.matmul(self.dctTran, block)
        dctMatrix = np.matmul(dctMatrix, self.dct)
        return dctMatrix.round().astype(int)

    
    def getBQ(self, B, Q):
        return np.round(B/Q)
    
    def reverseBQ(self, Q, BQ):
        return Q*BQ
    
    # def dc_difference(self, blocks):
    #     for index in range(1,blocks.shape[0]):
    #         blocks[index,0,0] -= blocks[index-1,0,0]


    def reverse_dc_difference(self, blocks):
        for index in range(blocks.shape[0]-1,0,-1):
            blocks[index,0,0] += blocks[index-1,0,0]
    
    def zigzag(self, block):
        """
        ZigZag Algorithm
        index = –1
        for i=0 to 2(n–1) do
        if (i < n) then bound=0 else bound = i–n+1 for j=bound to i–bound do begin
        index = index+1
        if i is odd
        thenZ[index] = X[j,i–j] else Z[index] = X[i–j,j]
        end end
        """
        n,_ = block.shape
        index = -1
        z = [0]*(n*n)
        for i in range(2*n-1):
            bound = 0 if i<n else i-n+1
            for j in range(bound, i-bound+1):
                index += 1
                z[index] = block[j, i-j] if i%2 == 1 else block[i-j,j]
        return z
    
    def reverseZigzag(self, array, block_size = 8):
        block = np.zeros((block_size,block_size),dtype = int)
        index = -1
        for i in range(0,2*block_size-1):
            bound = 0
            if i >= block_size:
                bound = i - block_size + 1
            for j in range(bound,i - bound + 1):
                index += 1
                if i % 2 != 0:
                    block[j,i-j] = array[index]
                    # ret.append((j,i-j))
                else:
                    block[i-j,j] = array[index]
                    # ret.append((i-j,j))

        return block


    def saveImage(self, array, fname):
        print(fname)
        cv2.imwrite(fname, array)

    
    def encodeImage(self, block_size):
        m, n = self.image.shape
        area = block_size * block_size
        padding_num = area - (m*n) % (area) if (m*n) % (area) != 0 else 0
        flat = self.image.flatten().reshape((1,m*n))
        flat = np.append(flat, np.zeros((1,padding_num)))
        num = m*n + padding_num
        total_result = []
        prev = 0
        for i in range(0,num,area):
            array = flat[i:i+area]
            block = array.reshape((block_size, block_size))
            AS = self.level_shift(block, block_size)
            B = self.performDCT(AS)
            Q = self.getLuminenceQuantizationMatrix(block_size)
            BQ = self.getBQ(B, Q)
            BQ[0,0] -= prev
            prev = BQ[0,0]
            ## dc difference
            array = self.zigzag(BQ)
            total_result += array
        total_result.append(m)
        total_result.append(n)
        total_result.append(block_size)
        total_result.append(self.adjust)
        return total_result
    
    def reverseImage(self, fname):
        # with open(fname, 'rb') as f:
        #     result = pickle.load(f)
        result = np.load(fname)
        height, width, block_size, adjust = result[-4:]
        height = int(height)
        width = int(width)
        block_size = int(block_size)
        result = list(result[:-4].astype(int))
        area = block_size * block_size
        n = len(result)
        arrays = [result[i:i+area] for i in range(0,n,area)]
        blocks = np.array([self.reverseZigzag(array, block_size) for array in arrays])
        self.reverse_dc_difference(blocks)
        Q = self.getLuminenceQuantizationMatrix(block_size, adjust = adjust, reverse= True)
        flat = np.array(())
        for block in blocks:
            B = self.reverseBQ(Q, block)
            AS = self.reverseDCT(B)
            origin = self.reverse_level_shift(AS, block_size)
            origin_flat = origin.flatten().reshape((1, area))
            flat = np.append(flat, origin_flat)
        flat = flat[:height* width]
        image = flat.reshape((height, width))
        return image

    def psnr(self, modified_image):
        m = np.mean((self.image - modified_image) ** 2)
        if m == 0:
            return 100
        else:
            return 20 * math.log10(255.0/math.sqrt(m))
        

def save_model(path, result):
    result = np.array(result)
    np.save(path,result)
    print('Successfully save the file !!')


def load_model(path):
    print('Successfully load the file !!')
    matrix = np.load(path)
    return matrix, matrix[-2]
        
if __name__ == '__main__':
    args = sys.argv
    pic = args[1]
    adjust = float(args[2])
    block_size = int(args[3])
    np_name = args[4]
    decompress_path = args[5]
    # pic = 'test_images/Kodak12gray.bmp'
    # pic_name = pic.split('/')[-1].split('.')[0]
    # adjust = 10
    process = JpegProcess(pic, adjust)
    # block_size = 16
    result = process.encodeImage(block_size)
    # np_name = pic_name + '_encode_result_{}_{}.npy'.format(block_size, adjust)
    # with open(pkl_name, 'wb') as f:
    #     pickle.dump(result, f, 2)
    save_model(np_name, result)
    print('encoded image saved as {}!'.format(np_name))
    image = process.reverseImage(np_name)
    # save_name = 'result/'+pic_name + '_{}_{}.bmp'.format(block_size, adjust)
    save_name = decompress_path
    process.saveImage(image, save_name)
    print('decoded image saved in {}'.format(save_name))
    print('PSNR: ', process.psnr(image))

    # list = [50, 50, 50, 50, 200, 200, 200, 200]
    # listRev = list[::-1]
    # checkboard = []
    
    # for i in range(0,4):
    #     checkboard.append(list)
    
    # for i in range(0,4):
    #     checkboard.append(listRev)
    
    # img = np.array(checkboard)
    # # img = np.repeat(img, 2, axis=0)
    # # img = np.repeat(img, 2, axis=1)
    # AS = encoder.level_shift(img, 8)
    # B = encoder.performDCT(AS)
    # Q = encoder.getLuminenceQuantizationMatrix(8)
    # BQ = encoder.getBQ(B,Q)
    # embed()
    # new_B = encoder.reverseBQ(Q, BQ)
    # embed()
    # new_B[0][0] = -16
    # new_AS = encoder.reverseDCT(new_B)
    # embed()
