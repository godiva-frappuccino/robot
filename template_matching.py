#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np
argv = sys.argv

image = cv2.imread('data/bug3.jpg')
template = cv2.imread('data/bug_template.jpg')

def calcCircleLevel (contour, area):
    perimeter = cv2.arcLength(contour, True)
    circle_level = 4.0 * np.pi * area / (perimeter * perimeter); # perimeter = 0 のとき気をつける
    return circle_level

def template_match_mono(image, template, count):
    kernel =np.array([[1, 1, 1],[1, -8, 1],[1, 1, 1]], np.float32)
    center_list = []
    #copy = np.zeros([image.shape[0], image.shape[1]])
    image = image[:,:,2] - image[:,:,0]
    ret,image = cv2.threshold(image,30,255,cv2.THRESH_TOZERO)
    ret,image = cv2.threshold(image,50,255,cv2.THRESH_TOZERO_INV)
    ret,image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)    
    image = cv2.dilate(image, kernel, iterations = 1)
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) >= 1:
        for cont in contours:
            (x,y),radius = cv2.minEnclosingCircle(cont)
            #center = (int(x),int(y))
            radius = int(radius)
            if radius >= 30 and radius <= 120:
                #image = cv2.circle(copy,center,radius,(255,255,255),2)
                center_list.append([int(x), int(y)])
                            
    cv2.imwrite('./data/result' + str(count) + '.jpg', image)
    return center_list

def main_process(file_path):
    image = cv2.imread(file_path)
    center = template_match_mono(image, template, 0)
    print(center)
    return center
    
if __name__ == '__main__':
    if len(argv) == 2:
        center = main_process(argv[1])
    else:
        print("usage: pthon3 template_matching.py file_name")
