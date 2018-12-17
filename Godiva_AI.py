# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time
import mumeikaneshige as mk
from detect_human import main_process as human_detect

rage_word = ['馬鹿', 'マヌケ', 'アホ']
stop_word = ['ごめん', 'すみません']
apolo_word = ['ゆるして']
words = ['', '', '', '', '']
laugh = "uhuhu.wav"
okotta = "rage.wav"
mukka = "mukka.wav"
atack = "atack.wav"
hansei = "hansei.wav"
apolo = "gomen.wav"

class Terminator(mk.Mumeikaneshige):
    def __init__(self):
        super().__init__()

    def say(voice):
        self.controllers['JTalk'].cmd_queue.put(voice)

    def apologize():
      voice = self.senders['Julius'].msg_queue.get()
      if voice in stop_word:
          self.say(gomen)
          return True
      elif voice in apolo_word:
          self.say(mukka)
          return False
      else:
          self.say(mukka)
          return False

    def get_rotate_angle(image, rocs, gakaku = 60):
        roc = rocs[0]
        center = int(image.shape[1]/2)
        # 右を正とする
        return (roc - center) / gakaku

    def go_straight(speed=30000):
        self.controllers['Motor'].cmd_queue.put((speed, speed))
        while True:
            if self.apologize():
                return False
            else:
                self.say(okotta)
            dst_msg = self.senders['SRF02'].msg_queue.get()
            if dst_msg[0] < 15 or dst_msg[1] < 15:
                self.controllers['Motor'].cmd_queue.put((e, e))
                return True

   
    def rotate_by_angle(speed=10000, angle):
        t = angle/40*3 + 1/2
        self.controllers['Motor'].cmd_queue.put((speed, -speed))
        time.sleep(t)
        self.controllers['Motor'].cmd_queue.put((0, 0))
    
    def smash():
        self.controllers['Arm'].cmd_queue.put(60)
        time.sleep(1)
        self.say(atack)
        self.controllers['Arm'].cmd_queue.put(-30)
        time.sleep(1)
        self.controllers['Arm'].cmd_queue.put(60)
       
        
    def rotate_nine(right = True):
        speed =30000 if right else -30000
        self.controllers['Moror'].cmd_queue.put((speed, -speed))
        time.sleep(5)
        self.controllers['Moror'].cmd_queue.put((speed, -speed))
          
    def rage(self, rotate_rate = 90):
        find = False
        
        # start rage_mode
        print("Rage Mode...")
        self.say(okotta)
        self.smash()
        
        # search human to smash
        for i in range(int(360 / rotate_rate)):
            # if apologized finish
            if self.apologize():
                break
            print("rotate to find human")
            self.rotate_nine(right = False)
            print("stop and find human")
            frame1, frame2 = self.senders['Webcamera'].msg_queue.get()
            roc1 = human_detect(frame1)
            roc2 = human_detect(frame2)
            
            # if found human
            if len(roc2) != 0:
                print("I found human!")
                x_center = (roc2[0][0] + roc2[0][2]) / 2
                self.say(okotta)
                self.rotate_by_angle(self.get_rotate_angle(frame2, x_center))
                find = True
                break
            elif len(roc1) != 0:
                print("I found human!!!")
                x_center = (roc1[0][0] + roc1[0][2]) / 2
                self.say(okotta)
                self.rotate_by_angle(self.get_rotate_angle(frame1, x_center))
                find = True
                break
            
            # if not found
            else:
                print("I couldn't find human...")
                self.say(mukka)
        
        # found! let's smash human!
        if find:
            self.say(mukka)
            if self.go_straight():
                self.smash()
                
                # everything is over, apologize
                time.sleep(2)
                self.say(gomen)
        
        # couldn't find, akirame...        
        else:
            self.say(mukka)
        print("Rage mode finished...")
            
    def run(self): 
        print("Godiva_AI start running!!!")
        while True:
            voice = self.senders['Julius'].msg_queue.get()
            if voice in rage_word:
                self.rage()
            else:
                self.say(laugh)
                
def main():
    robot = Terminator()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
