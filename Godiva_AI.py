# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time

import mumeikaneshige as mk
from detect_human import main_process as human_detect

rage_word = ['馬鹿', 'マヌケ', 'アホ']
stop_word = ['ごめんなさい', 'すみません']
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

    def go_straight(speed=30000):
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        while True:
            if self.apolo():
                return False
            dst_msg = self.senders['SRF02'].msg_queue.get()
            if dst_msg[0] < 15 or dst_msg[1] < 15:
                self.controllers['Motor'].cmd_queue.put((e, e))
                return True

    def go_fast(speed=30000, d):
        t = 5/3*d + 3/2
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        time.sleep(t)    
        self.controllers['Motor'].cmd_queue.put((0, 0))
        
    
    def go_slow(speed=10000, d=2):
        t = 5*d + 1/2
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        time.sleep(t)    
        self.controllers['Motor'].cmd_queue.put((0, 0))
    
    def rotate_by_angle(angle):
        speed = angle
        self.controllers['Motor'].cmd_queue.put((5000,-5000))
        time.sleep(1)
        self.controllers['Motor'].cmd_queue.put((0, 0))

    def smash():
        self.controllers['Arm'].cmd_queue.put(60)
        time.sleep(1)
        self.controllers['Arm'].cmd_queue.put(-30)
        time.sleep(1)
        self.controllers['Arm'].cmd_queue.put(60)
       
        
    def rotate_nine(right = True):
        speed =30000 if right else -30000
        self.controllers['Moror'].cmd_queue.put((speed, -speed))
        time.sleep(5)
        self.controllers['Moror'].cmd_queue.put((speed, -speed))

    def apolo():
      voice = self.senders['Julius'].msg_queue.get()
      if voice in stop_word:
          return True
      else:
          return False
          
    def rage(self, rotate_rate = 90):
        find = False
        print("Rage Mode...")
        self.controllers['JTalk'].cmd_queue.put('yes.wav') # rage
        self.smash()
        for i in range(int(360 / rotate_rate)):
            if self.apolo():
                break
            print("rotate to find human")
            self.rotate_nine(right = False)
            print("stop and find human")
            frame1, frame2 = self.senders['Webcamera'].msg_queue.get()
            #roc1 = human_detect(frame1)
            #roc2 = human_detect(frame2)
            roc1 = [1, 2]
            roc2 = [2, 3]
            if len(roc2) != 0:
                print("I found human!")
                self.controllers['JTalk'].cmd_queue.put('yes.wav') # find
                self.rotate_by_angle(self.get_rotate_angle(frame2, roc2))
                find = True
                break
            elif len(roc1) != 0:
                print("I found human!")
                self.controllers['JTalk'].cmd_queue.put('yes.wav') # find
                self.rotate_by_angle(self.get_rotate_angle(frame1, roc1))
                find = True
                break
            else:
                print("I couldn't find human...")
                self.controllers['JTalk'].cmd_queue.put('yes.wav') # gakkari
        if find:
            self.controllers['JTalk'].cmd_queue.put('yes.wav') # ikuyo
            if self.go_straight():
                self.smash()
        else:
            self.controllers['JTalk'].cmd_queue.put('yes.wav') # sikatanai
        print("Rage mode finished...")
            
    def run(self): 
        print("Godiva_AI start running!!!")
        while True:
            voice = self.senders['Julius'].msg_queue.get()
            if voice in rage_word:
                self.rage()
        
def main():
    robot = Terminator()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
