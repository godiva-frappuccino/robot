#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import sys, os
import numpy as np

# 入力画像、テンプレート画像を読み込む。
image = cv2.imread('data/bug3.jpg')  # 入力画像
template = cv2.imread('data/bug_template.jpg')  # テンプレート画像

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

def template_match_mono(image, template, count):
    image = image[:,:,2] - image[:,:,0]
    print(image.shape)
    ret,image = cv2.threshold(image,30,255,cv2.THRESH_TOZERO)
    ret,image = cv2.threshold(image,50,255,cv2.THRESH_TOZERO_INV)
    ret,image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
    
    cv2.imwrite('./data/result' + str(count) + '.jpg', image)

file_dir = './data/'
    
    
for i, file in enumerate(os.listdir(file_dir)):
    print(file)
    img = cv2.imread(file_dir+file)  # 入力画像
    template_match_mono(img, template, i)
    
