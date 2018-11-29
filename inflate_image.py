#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:18:56 2018

@author: root
"""

import cv2
import numpy as np
import os
import random
import matplotlib.pyplot as plt


FILE_PATH = 'svm/neg/'

def inflate_image(FILE_PATH):
    count = 0
    files = os.listdir(FILE_PATH)
    for file in files:
        count = count + 1
        print("file",count,": ",file)        
        # read and preprosess image
        image = cv2.imread(FILE_PATH+file)
        # bure
        for i in range(10):
            shift_x = random.randint(-20,20)
            shift_y = random.randint(-10,10)
            rows, cols = image.shape[:2]
            pts1 = np.float32([[50,50],[60,50],[50,60]])
            pts2 = np.float32([[50 + shift_x, 50 + shift_y],[60 + shift_x, 50 + shift_y],[50 + shift_x, 60 + shift_y]])
            M = cv2.getAffineTransform(pts1,pts2)
            image_affine = cv2.warpAffine(image,M,(cols,rows))
            cv2.imwrite(FILE_PATH + 'inflated_image_affine' + str(count) + '_' + str(i) + '.jpg', image_affine)
        # dark (gamma is also good)
        for i in range(10):
            image_dark = (image / (1 + i*0.02))
            cv2.imwrite(FILE_PATH + 'inflated_image_dark' + str(count) + '_' + str(i) + '.jpg', image_dark)
        # light
        for i in range(10):
            image_light = (image * (1 + i*0.02))
            cv2.imwrite(FILE_PATH + 'inflated_image_light' + str(count) + '_' + str(i) + '.jpg', image_light)
        # blur
        for i in range(5):
            average_square = (i + 1, i + 1)
            image_blur = cv2.blur(image, average_square)
            cv2.imwrite(FILE_PATH + 'inflated_image_blur' + str(count) + '_' + str(i) + '.jpg', image_blur)
        # mix
        
if __name__ == '__main__':
    inflate_image(FILE_PATH)
