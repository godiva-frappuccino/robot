#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 17:52:00 2018

@author: root
"""

import numpy as np
from sklearn import svm
import sys, os
import cv2
import pickle

argv = sys.argv

IMAGE_SIZE = 40
COLOR_BYTE = 3
CATEGORY_NUM = 3
LEARN_RATE = 0.3
RESIZE = 100
size = (RESIZE, RESIZE)

labels = []
pos_images = []
neg_images = []

# data`s directory
pos_path = './pos/'
neg_path = './neg/'


def load_image(dir_path, class_num): # class1 = True data, else = False data
    count = 0
    files = os.listdir(dir_path)
    for file in files:
        count = count + 1
        print("file",count,": ",file)
        
        # read and preprosess image
        image = cv2.imread(dir_path+file)
        image= cv2.resize(image, size)
        print(image.shape)
        image = np.reshape(image, -1, RESIZE*RESIZE*3)
        
        # into pos or neg directory
        if class_num == 1:
            labels.append(1)
            pos_images.append(image)
        else:
            labels.append(0)
            neg_images.append(image)

if __name__ == '__main__':
    if len(argv) == 3:
        pos_path = argv[1]
        neg_path = argv[2]

    # load_images from path
    load_image(pos_path, 1)
    load_image(neg_path, 0)

    # divide datas into train or test(now only train)
    train_pos = pos_images[:int(len(pos_images)*LEARN_RATE)]
    train_neg = neg_images[:int(len(neg_images)*LEARN_RATE)]

    # make train_data array
    train_data = []

    for data in train_pos:
        train_data.append(data)
    for data in train_neg:
        train_data.append(data)

    #make traindata's label arra
    train_target = []

    for i in range(len(train_pos)):
        train_target.append(1)    
    for i in range(len(train_neg)):
        train_target.append(0)

    # make model and train by using SVM
    print("learning start:")
    classifier = svm.LinearSVC()
    classifier.fit(train_data, train_target)
    print("learning finished")

    # save model
    print("save model:")
    filename = 'svm_suika_model.sav'
    pickle.dump(classifier, open(filename, 'wb'))

