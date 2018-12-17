# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 20:57:33 2018

@author: godiva
"""

import cv2
import numpy as np

read = 'data/coc5.jpg'
save = 'data/result.jpg'

def cf(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imwrite('data/hsv_h.jpg', image[:,:,0])
    cv2.imwrite('data/hsv_s.jpg', image[:,:,1])
    cv2.imwrite('data/hsv_v.jpg', image[:,:,2])
    lower = np.array([50, 200, 0])
    upper = np.array([100, 255, 250])
    mask = cv2.inRange(image, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)
    return image

def cl(image):
    b = image[:,:,0]
    g = image[:,:,1]
    r = image[:,:,2]
    m = (b+g+r)/3
    s = (b-m)**2 + (g-m)**2 + (r-m)**2
    s = np.sqrt(s)
    print(s)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.where(s > 150, image, 0)
    image = np.where(s < 200, image, 0)
    return image

def edge(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.where(image > 100, image, 0)
    image = np.where(image < 150, image, 0)
    image = image.astype(np.float32)
    ed = np.array([[1, 1, 1],[1, -8, 1], [1, 1, 1]], np.float32)
    #image = cv2.filter2D(image, -1, ed)
    return image

kernel = np.ones((3, 3), np.float32)/9

if __name__ == '__main__':
    image = cv2.imread(read)
    #image = cl(image)
    #image = edge(image)
    image = cf(image)
    #image = cv2.erode(image, kernel, iterations = 1)
    #image = cv2.dilate(image, kernel, iterations = 3)
    cv2.imwrite(save, image)