# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time

import mumeikaneshige as mk
from detect_human import main_process as human_detect

rage_word = ['馬鹿', 'マヌケ', '死ね', 'アホ', 'ファック', 'マザーファッカー']
class Terminator(mk.Mumeikaneshige):
    def __init__(self):
        super().__init__()

    def get_rotate_angle(image, rocs, gakaku = 60):
        roc = rocs[0]
        center = int(image.shape[1]/2)
        # 右を正とする
        return (roc - center) / gakaku

    def go_time(speed=10000, t=1):
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        time.sleep(t)    
        self.controllers['Motor'].cmd_queue.put((0, 0))

    def go_dist(speed=10000, d=2):
        t = d / 2
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        time.sleep(t)    
        self.controllers['Motor'].cmd_queue.put((0, 0))
        
    def rotate_by_angle(angle):
        speed = angle
        self.controllers['Motor'].cmd_queue.put((5000,-5000))
        time.sleep(1)
        self.controllers['Motor'].cmd_queue.put((0, 0))

    def rage(self, rotate_rate = 60):
        hit = False
        print("Rage Mode...")
        self.controllers['JTalk'].cmd_queue.put('yes.wav')
        self.controllers['Arm'].cmd_queue.put(50)
        time.sleep(1)
        self.controllers['Arm'].cmd_queue.put(-30)
        time.sleep(1)
        self.controllers['Arm'].cmd_queue.put(50)
        for i in range(int(360 / rotate_rate)):
            #self.rotate_by_angle(rotat_rate)
            print("moter left")
            self.controllers['Motor'].cmd_queue.put((5000, -5000))
            time.sleep(3)
            print("Motor stop")
            self.controllers['Motor'].cmd_queue.put((0,0))
            frame1, frame2 = self.senders['Webcamera'].msg_queue.get()
            #roc1 = human_detect(frame1)
            #roc2 = human_detect(frame2)
            roc1 = [1, 2]
            roc2 = [2, 3]
            if len(roc2) != 0:
                print("Human detect")
                # rotate
                #rotate_by_angle(get_rotate_angle(frame2, roc2))
                self.controllers['JTalk'].cmd_queue.put('yes.wav')
                self.controllers['Motor'].cmd_queue.put((5000, -5000))
                time.sleep(1)
                self.controllers['Motor'].cmd_queue.put((0,0))
                # go
                self.controllers['JTalk'].cmd_queue.put('yes.wav')
                self.controllers['Motor'].cmd_queue.put((5000, 5000))
                time.sleep(1)
                self.controllers['Motor'].cmd_queue.put((0,0))
                self.controllers['Arm'].cmd_queue.put(50)
                time.sleep(1)
                self.controllers['Arm'].cmd_queue.put(-30)
                time.sleep(1)
                self.controllers['Arm'].cmd_queue.put(50)
                hit = True
                break
            elif len(roc1) != 0:
                print("Human detect")
                self.controllers['Jtalk'].cmd_queue.puy('yes.wav')
                self.controllers['Motor'].cmd_queue.put((5000, -5000))
                time.sleep(1)
                self.controllers['Motor'].cmd_queue.put((0,0))
                #rotate_by_angle(get_rotate_angle(frame1, roc1))
                self.controllers['Arm'].msg_queue.put(50)
                time.sleep(1)
                self.controllers['Arm'].msg_queue.put(-30)
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
        print("Rage mode finished...")
            
    def run(self):
        self.controllers['Motor'].cmd_queue.put((10000, -10000))
        time.sleep(2)
        self.controllers['Motor'].cmd_queue.put((0,0))
        #self.rage()
        
def main():
    robot = Terminator()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
