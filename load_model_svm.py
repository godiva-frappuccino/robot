#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:01:23 2018

@author: root
"""
import numpy as np
from sklearn import svm
import sys, os
import cv2
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle
import pandas

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

pos_path = './illust_data/pos/'
neg_path = './illust_data/neg/'

def load_image(dir_path, class_num):
    count = 0
    files = os.listdir(dir_path)
    for file in files:
        count = count+1
        print("file",count,": ",file,":",class_num)
        image = cv2.imread(dir_path+file)
        image= cv2.resize(image, size)
        print(image.shape)

        image = np.reshape(image, -1, RESIZE*RESIZE*3)
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
    
    load_image(pos_path, 1)
    load_image(neg_path, 0)
    
    #test_pos = pos_images[int(len(pos_images)*LEARN_RATE):]
    #test_neg = neg_images[int(len(neg_images)*LEARN_RATE):]
    test_pos = pos_images
    test_neg = neg_images    
    # make test_data array
    test_data = []
    
    for data in test_pos:
        test_data.append(data)
    for data in test_neg:
        test_data.append(data)
            
        # make test_data's label array 
        test_target = []

    for i in range(len(test_pos)):
        test_target.append(1)    
    for i in range(len(test_neg)):
        test_target.append(0)

    # load learned_model
    filename = 'svm_suika_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    # test model
    predicted = loaded_model.predict(test_data)

    # print test result
    print("matrix:",metrics.confusion_matrix(test_target, predicted))
    print("accuracy:",metrics.accuracy_score(test_target, predicted))
    metrics = metrics.confusion_matrix(test_target, predicted)
    print("suika recognised:",metrics[1][1] / (metrics[1][0] + metrics[1][1]))
