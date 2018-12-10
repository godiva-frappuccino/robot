# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time

import mumeikaneshige as mk
from detect_coc import detect_coc

class BugDestroyer(mk.Mumeikaneshige):
    def __init__(self):
        super().__init__()

    def run(self):
         
        print('START')
        self.controllers['Arm'].cmd_queue.put(-25)
        while True:

            stall_msg = self.senders['DetectStall'].msg_queue.get()
            print(stall_msg)
            
            if stall_msg:
                self.controllers['JTalk'].cmd_queue.put('../voice-sample/yes.wav')
            time.sleep(0.5)

def main():
    robot = BugDestroyer()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
