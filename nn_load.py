#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 00:02:19 2018

@author: root
"""

import tensorflow as tf
import keras
from keras.utils import np_utils
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import cv2
import sys, os
from keras.datasets import mnist
from keras.models import model_from_json
from keras.utils import np_utils

RESIZE = 64
size = (RESIZE, RESIZE)


def load_image(dir_path, class_num, data, label): # class1 = True data, else = False data
    count = 0
    files = os.listdir(dir_path)
    for file in files:
        count = count + 1
        #print("file",count,": ",file)
        sys.stdout.write(str(count) + " ")
        
        # read and preprosess image
        image = cv2.imread(dir_path+file)
        image= cv2.resize(image, size)
        #image = np.reshape(image, -1, RESIZE * RESIZE * 3)
        label.append(class_num)
        data.append(image)
    print("")

# data`s directory
pos_path = './data/pos/'
neg_path = './data/neg/'

def main():
    X = []
    Y = []
    load_image(pos_path, 1, X, Y)
    load_image(neg_path, 0, X, Y)
    # NumPy配列に変換
    X = np.asarray(X)
    Y = np.asarray(Y)

    # float32型に変換
    X = X.astype('float32')

    # 正規化(0～1)
    X_train = X / 255.0
    X_test = X / 255.0

    # クラスの形式を変換
    Y = np_utils.to_categorical(Y, 2)
    y_train = Y
    y_test = Y
    # 学習用データとテストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.5, random_state=111)
 
    print("load model:")
    # load model
    model = load_model('model_.h5')
    
    print("check model:")
    # モデルの検証・性能評価
    score = model.evaluate(X_train, y_train, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    print('what:', score)

if __name__ == '__main__':
    main()
