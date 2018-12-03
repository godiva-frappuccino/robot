#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
argv = sys.argv

template = cv2.imread('data/bug_template.jpg')  # テンプレート画像
 
def red_filter(image):
    image = image.astype(np.float32)
    image3 = image[:,:,2]
    image3 /= 255
    return image3
    
def calcCircleLevel (contour, area):
    perimeter = cv2.arcLength(contour, True)
    circle_level = 4.0 * np.pi * area / (perimeter * perimeter); # perimeter = 0 のとき気をつける
    return circle_level

def detect_coc(image, template):
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    centers = []
    copy = image.copy()    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = image[:,:,1]
    image = image*red_filter(copy)
    image = image.astype(np.uint8)
    
    ret,image = cv2.threshold(image,50,255,cv2.THRESH_TOZERO)
    kernel_gauss = np.ones((3,3), np.float32)/9
    kernel = np.array([[1,1,1],[1,-8,1],[1,1,1]], np.float32)
    image = cv2.filter2D(image, -1, kernel)
    image = cv2.filter2D(image, -1, kernel_gauss)
    image = cv2.dilate(image, kernel, iterations = 3)
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) >= 1:
        for cont in contours:
            (x,y),radius = cv2.minEnclosingCircle(cont)
            center = (int(x),int(y))
            radius = int(radius)
            if radius >= 20 and radius <= 70:
                image = cv2.circle(image,center,radius,(255,255,255),2)
                centers.append([int(x), int(y)])
   
    return centers
    
file_dir = './data/'

def main_process(path):
    image = cv2.imread(path)
    return detect_coc(image, template)

if __name__ == '__main__':
    if len(argv) != 2:
        print("usage:python3 detect_coc.py file_name")
    else:
        print(main_process(argv[1]))  
