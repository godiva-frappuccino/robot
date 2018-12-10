#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:01:18 2018

@author: root
"""

# import the necessary packages
import numpy as np
import sys
from logging import getLogger, DEBUG, StreamHandler
import cv2
import os

argv = sys.argv
file_dir = 'data/human1/'
save_dir = 'data/'

def deep_learning_object_detection(image, prototxt, model, count):
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        handler = StreamHandler(sys.stderr)
        handler.setLevel(DEBUG)
        logger.addHandler(handler)

        CONFIDENCE = 0.2

        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    
        #logger.info("Loading model...")

        net = cv2.dnn.readNetFromCaffe(prototxt, model)
        image = cv2.imread(image)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    
        #logger.info("computing object detections...")

        net.setInput(blob)
        detections = net.forward()
        boxs = []
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > CONFIDENCE:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    print("x:",startX, " y:",startY, " x+w:",endX, " y+h:",endY)
                    print(CLASSES[idx])
                    image = cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 255))
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    logger.info(label)
                    boxs.append(((startX, startY), (endX, endY)))
                    cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
        return boxs

def main_process(file_path):
    prototxt="MobileNetSSD_deploy.prototxt.txt"
    model="MobileNetSSD_deploy.caffemodel"
    boxs = deep_learning_object_detection(file_path, prototxt, model, 0)
    print(boxs)
    return boxs
    
if __name__ == '__main__':
    if len(argv) == 2:
        boxs = main_process(argv[1])
    else:
        print("usage:python3 ssd_detection file_name")

        
