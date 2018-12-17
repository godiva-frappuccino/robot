#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import sys, os
import numpy as np

# 入力画像、テンプレート画像を読み込む。
image = cv2.imread('data/bug3.jpg')  # 入力画像
template = cv2.imread('data/bug_template.jpg')  # テンプレート画像
 
def co(image):
    image = image.astype(np.float32)
    image3 = image[:,:,2]
    #image_mean = ((image1 + image2 + image3)/3)
    #s = np.sqrt((image1-image_mean)**2 + (image2-image_mean)**2 + (image3-image_mean)**2)
    #print(s)
    #cv2.imwrite('./data/result' + str(count) + '.jpg', image3)
    image3 /= 255
    return image3
    
def template_match(image, template, count):
    # テンプレートマッチングを行う。
    result = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
    # 検索窓の範囲を描画する。
    def draw_window(image, x, y, w, h):
        tl = x, y  # 左上の頂点座標
        br = x + w, y + h  # 右下の頂点座標
        cv2.rectangle(image, tl, br, (0, 255, 0), 3)

    # 最も類似度が高い位置を取得する。
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    print('max value: {}, position: {}'.format(maxVal, maxLoc))

    # 描画する。
    drawn = image.copy()
    h, w = template.shape[:2]
    # maxLoc[0], maxLoc[1] = 左上の頂点座標(x, y) 
    draw_window(drawn, maxLoc[0], maxLoc[1], w, h)
    cv2.imwrite('./data/result' + str(count) + '.jpg', drawn)

def calcCircleLevel (contour, area):
    perimeter = cv2.arcLength(contour, True)
    circle_level = 4.0 * np.pi * area / (perimeter * perimeter); # perimeter = 0 のとき気をつける
    return circle_level

def template_match_mono(image, template, count):
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    copy = image.copy()
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = image[:,:,1]
    image = image*co(copy)
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
                print(int(x), int(y))
            
    cv2.imwrite('./data/result' + str(count) + '.jpg', image)

file_dir = './data/'
    
for i, file in enumerate(os.listdir(file_dir)):
    print(file)
    image = cv2.imread(file_dir+file)  # 入力画像
    #co(image, i)
    template_match_mono(image, template, i)
    
