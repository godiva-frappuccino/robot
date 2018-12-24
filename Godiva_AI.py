# coding: utf-8

import sys
sys.path.append('../')
import numpy as np
import cv2
import time
import random
import mumeikaneshige as mk
from detect_human import main_process as human_detect
from human import main_process as h_detect
import movidius

rage_word = ['馬鹿', 'マヌケ', 'アホ']
stop_word = ['ごめん', 'すみません']
apolo_word = ['ゆるして']
# laugh word
laugh = "uhuhu.wav"
hai = "hai.wav"
yobu = "yobu.wav"
laugh_word = [laugh, hai, yobu]
# rage word
okotta = "rage.wav"
mukka = "mukka.wav"
atack = "atack.wav"
naniyo = "naniyo.wav"
kakugo = "kakugo.wav"
aa = "find.wav"
# apologize word
hansei = "hansei.wav"
gomen = "gomen.wav"
# finish word
mouii = "mouii.wav"
# other word
start = "start.wav"
end = "end.wav"


class Terminator(mk.Mumeikaneshige):
    def __init__(self):
        super().__init__()
        graph = '../movidius/graph'
        categories = ('background','aeroplane', 'bicycle', 'bird', 'boat',
                  'bottle', 'bus', 'car', 'cat', 'chair','cow',
                  'diningtable', 'dog', 'horse','motorbike', 'person',
                  'pottedplant', 'sheep','sofa', 'train', 'tvmonitor')
    
        self.detector = movidius.MobileSSD(graph, categories)


    def say(self, voice):
        self.controllers['JTalk'].cmd_queue.put(voice)

    def set_go(self, speed_right, speed_left, acc):
        self.controllers['Motor'].cmd_queue.put((speed_right, speed_left, acc))        

    def set_arm(self, angle):
        self.controllers['Arm'].cmd_queue.put(angle)
        
    def get_voice(self):
        return self.senders['Julius'].msg_queue.get()

    def get_sensor(self):
        return self.senders['SRF02'].msg_queue.get()

    def get_image(self):
        return self.senders['Webcamera'].msg_queue.get()

    def apologize(self):
        self.say(kakugo)
        time.sleep(2)
        voice = self.get_voice()
        print("Apologize word", voice)
        if voice in stop_word:
            self.say(gomen)
            return True
        elif voice in apolo_word:
            self.say(naniyo)
            return False
        else:
            self.say(naniyo)
            return False

    def get_angle(self, image, roc, gakaku = 60):
        center = 150
        # 右を正とする
        return (roc - center) / gakaku * 640 / 300

    def go_straight(self):
        speed = 30000
        self.set_go(speed, speed, speed)
        while True:
            dst_msg = self.get_sensor()
            print(dst_msg)
            if dst_msg[0] < 20 or dst_msg[1] < 20:
                self.set_go(0, 0, 30000)
                return True
   
    def rotate_by_angle(self, angle):
        speed = 10000
        print("angle = ", angle)
        t = float(angle) / 15
        print("rotate time = ", t)
        self.set_go(-speed, speed, speed)
        time.sleep(t)
        self.set_go(0, 0, speed)
        
    def smash(self):
        self.set_arm(60)
        time.sleep(1)
        self.say(atack)
        time.sleep(0.5)
        self.set_arm(-30)
        time.sleep(1)
        self.set_arm(60)
       
        
    def rotate_six(self, right = True):
        speed =20000 if right else -20000
        self.set_go(speed, -speed, abs(speed))
        time.sleep(2)
        self.set_go(0, 0, abs(speed))
          
    def rage(self, rotate_rate = 60):
        find = False
        
        # start rage_mode
        print("Rage Mode...")
        self.say(okotta)
        self.smash()
        
        # search human to smash
        for i in range(int(360 / rotate_rate)):
            frame1, frame2 = self.get_image()
            roc1 = h_detect(frame1, self.detector)
            roc2 = h_detect(frame2, self.detector)
            # if apologized finish
            if self.apologize():
                break
            
            # if found human
            if roc2 != 0:
                print("I found human!")
                self.say(aa)
                print("adjust angle to smash")
                self.rotate_by_angle(self.get_angle(frame2, roc2))
                find = True
                time.sleep(1)
                break
            elif roc1 != 0:
                print("I found human!!!")
                self.say(aa)
                print("adjust angle to smash")
                self.rotate_by_angle(self.get_angle(frame1, roc1))
                find = True
                time.sleep(1)
                break
            
            # if not found
            else:
                print("I couldn't find human...")
                self.say(mukka)

                if i == 5:
                    pass
                print("rotate to find human", i)
                self.rotate_six(right = True)
                print("stop and find human")
                time.sleep(2)
           
        # found! let's smash human!
        print("let's smash human")
        if find:
            if self.apologize():
                pass
            if self.go_straight():
                self.smash()
                
                # everything is over, apologize
                time.sleep(2)
                self.say(gomen)
            find = False
        
        # couldn't find, give up...
        else:
            self.say(hansei)
        print("Rage mode finished...")
            
    def run(self): 
        print("Godiva_AI start running!!!")
        while True:
            voice = self.get_voice()
            if voice in rage_word:
                self.rage()
                break
            else:
                self.say(laugh_word[random.randint(0, 2)])
        print("Godiva AI normally finished...")
        
def main():
    robot = Terminator()
    robot.start()
    del robot
if __name__ == '__main__':
    main()
