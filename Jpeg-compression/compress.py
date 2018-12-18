import numpy as np 
import cv2
from IPython import embed

fname = 'test_images/Kodak08gray.bmp'
image = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
