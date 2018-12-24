# coding:utf-8

import numpy as np
import cv2

import sys
sys.path.append('..')

import movidius

def main_process():
    path_to_graph = '../movidius/graph'
    categories = ('background','aeroplane', 'bicycle', 'bird', 'boat',
                  'bottle', 'bus', 'car', 'cat', 'chair','cow',
                  'diningtable', 'dog', 'horse','motorbike', 'person',
                  'pottedplant', 'sheep','sofa', 'train', 'tvmonitor')
    
    detector = movidius.MobileSSD(path_to_graph, categories)
    
    cam = cv2.VideoCapture(1)
    x_center = 0
    try:
        _, frame = cam.read()
        if frame is None:
            print('Failed to take a picture')
            pass
        frame = cv2.resize(frame, (300, 300))
        result = detector.detect(frame)
        
        for item in result:
            if item['category'] != 'person':
                continue
            x_center = int((item['x1'] + item['x2'])/2)
            break

        cv2.waitKey(0)
        return x_center

    finally:
        cam.release()
        return x_center
        

if __name__ == '__main__':
    main_process()
