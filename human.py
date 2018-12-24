# coding:utf-8

import numpy as np
import cv2

import sys
sys.path.append('..')
import movidius

def main_process(frame, detector):
    x_center = 0
    try:
        if frame is None:
            print('Failed to take a picture')
            pass
        frame = cv2.resize(frame, (300, 300))
        result = detector.detect(frame)
        
        for item in result:
            if item['category'] != 'person':
                continue
            print('human detect!')
            #print('x1 = ', item['x1'], 'x2 = ', item['x2'])
            x_center = int((item['x1'] + item['x2'])/2)
            break

    finally:
        return x_center
        

if __name__ == '__main__':
    main_process()
