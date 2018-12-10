#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:01:23 2018

@author: root
"""
import numpy as np
import sys
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

def load_image(file_path, class_num):
    image = cv2.imread(file_path)
    image= cv2.resize(image, size)

    image = np.reshape(image, -1, RESIZE*RESIZE*3)
    labels.append(1)
    pos_images.append(image)
    
def suika(path):
    print("load image...")
    load_image(path, 1)
    
    test_pos = pos_images
    # make test_data array
    test_data = []
    
    for data in test_pos:
        test_data.append(data)
            
        # make test_data's label array 
        test_target = []

    for i in range(len(test_pos)):
        test_target.append(1)    
        
    print("load svm_model...")
    # load learned_model
    suika_model = 'svm_suika_model.sav'
    loaded_model = pickle.load(open(suika_model, 'rb'))

    print("judge if smashed...")
    # test model
    predicted = loaded_model.predict(test_data)
    if predicted[0] == 1:
        print("suika is successfully destroyed!")
        return True
    else:
        print("failed...")
        return False

def main_process(path):
    print("judge if suika smashed!!")
    return suika(path)
    
if __name__ == '__main__':
    if len(argv) == 2:
        file_name = argv[1]
        main_process(file_name)
    else:
        print("usage:python3 suika_svm.py file_name")
    
            