# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time

import mumeikaneshige as mk
from detect_human import main_process as human_detect

class Terminator(mk.Mumeikaneshige):
    def __init__(self):
        super().__init__()

    rage_word = ['馬鹿', '無能', '死ね', '阿呆', 'ファック', 'マザーファッカー']
    is_rage = False

    def get_rotate_angle(image, rocs, gakaku = 60):
        roc = rocs[0]
        center = int(image.shape[1]/2)
        # 右を正とする
        return (roc - center) / gakaku

    def go_dest(dest):
        
        time.sleep(1)
    
    def angle_to_speed(angle):
        speed = angle
        time.sleep(1)

    def rage(self, rotate_rate = 60):
        hit = False
        self.controllers['JTalk'].cmd_queue.put('yes.wav')
        self.controllers['Motor'].cmd_queue.put(50)
        time.sleep(1)
        self.controllers['Motor'].cmd_queue.put(-20)
        for i in range(360 / rotate_rate):
            self.controllers['Motor'].cmd_queue.put((5000,-5000))
            time.sleep(1)
            self.controllers['Motor'].cmd_queue.put((0, 0))
            frame1, frame2 = self.senders['Webcamera'].msg_queue.get()
            roc1 = human_detect(frame1)
            roc2 = human_detect(frame2)
            if len(roc1) != 0 or len(roc2) = 0:
                self.controllers['JTalk'].cmd_queue.put('yes.wav')
                self.controllers['Arm'].msg_queue.put(50)
                time.sleep(1)
                self.controllers['Arm'].msg_queue.puy(-20)
                hit = True
                break
            else:
                self.controllers['JTalk'].cmd_queue.put('yes.wav')
        if hit:
            self.controllers['Motor'].cmd_queue.put((10000, 10000))
            time.sleep(1)
            self.controllers['Motor'].cmd_queue.put((0, 0))
            self.controllers['Arm'].cmd_queue.put(50)
            time.sleep(1)
            self.controllers['Arm'].cmd_queue.put(-20)
        else:
            self.controllers['JTalk'].cmd_queue.put('yes.wav')
        is_rage = False
            
    def run(self):
        while True:
            voice = self.senders['Julius'].msg_queue.get()
            if rage_word.exist(voice):
                is_rage = True
            if is_rage:
                rage()

def main():
    robot = BugDestroyer()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
