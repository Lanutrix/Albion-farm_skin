import json
import pd
from math import sqrt
import os
from PIL import ImageGrab
from datetime import datetime, timedelta
import keyboard
import numpy as np
from ultralytics import YOLO
import pyautogui as pag
import cv2
from sys import exit as qx
from time import sleep


config = json.loads(open('config.json').read())
model = YOLO('pyst.pt')
scrn    = list(pag.size())



person  = [scrn[0]//2, scrn[1]//2-30]
path_screen = '13yolo.jpg'


img_atack = cv2.imread('atack.png')
img_atack = img_atack[36:40, 298:400]

img_looting = cv2.imread('looting.png')
img_looting = img_looting[447:472, 520:546]

img_dange = cv2.imread('dange.png')
img_dange = img_dange[578:635, 1118:1165]

dviz = [[scrn[0]//2+400, scrn[1]//2],
    [scrn[0]//2-400, scrn[1]//2],
    [scrn[0]//2, scrn[1]//2+300],
    [scrn[0]//2, scrn[1]//2-300]]
 
class Bot_API:
    def __init__(self) -> None:
        self.start = 1
        self.skan = 1
        self.use = [    config['skills'][0],
                        [timedelta(0, i) for i in config['skills'][1]]
                   ]
        self.timer = {i : datetime.now() for i in self.use[0]}
        try:
            self.dviz = config["movement"]
        except:
            self.dviz = []
        self.fight = 0

    def atack_press_skills(self):
        for i in range(len(self.use[0])):
            if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                pag.press(self.use[0][i])
                self.timer[self.use[0][i]] = datetime.now()

    def vector_move(self):
        self.dviz += [pag.position()]
        print(self.dviz)

    def clear_dviz(self):
        print('CLEAR')
        self.dviz = []


    def skaning(self):
        if self.fight:
            sleep(2)
            self.fight = 0
            return False
        screenshot = ImageGrab.grab()
        screenshot.save('13yolo.jpg')
        sleep(0.01)
        results = model.predict('13yolo.jpg', show = False, save=False, imgsz=(1280, 736), conf=config['cnn'], line_thickness = 1)
        os.remove('13yolo.jpg')
        mobs = [[], []]
        for r in results:
            for c in r.boxes:
                x=(int(c.xyxy[0][0])+int(c.xyxy[0][2]))//2
                y=(int(c.xyxy[0][1])+int(c.xyxy[0][3]))//2
                mobs[0].append([x ,y])
            for c in r.boxes.cls:
                mobs[1].append(int(c))
        if mobs[0]:
            x1, y1 = person
            min_distance = 10_000
            nearest_point = None
            for point in range(len(mobs[1])):
                x2, y2 = mobs[0][point][0], mobs[0][point][1]
                distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = mobs[0][point]
            pag.click(nearest_point)
            sleep(2)

            screenshot = ImageGrab.grab()
            open_cv_image = np.array(screenshot)
            img2 = open_cv_image[:, :, ::-1].copy()
            pixel2 = img2[36:40, 298:400]
            diff = cv2.absdiff(img_atack, pixel2)
            similarity = cv2.mean(diff)[0]
            if similarity < 2.4:
                pag.press('space')
                for i in range(len(self.use[0])):
                    if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                        pag.press(self.use[0][i])
                        self.timer[self.use[0][i]] = datetime.now()
                return False
            pixel2 = img2[447:472, 520:546]
            diff = cv2.absdiff(img_looting, pixel2)
            similarity = cv2.mean(diff)[0]
            if similarity < 1:
                return False
            
        return True
        

    def atack_or_looting(self):
        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = img2[36:40, 298:400]
        diff = cv2.absdiff(img_atack, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 1:
            pag.press('space')
            for i in range(len(self.use[0])):
                if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                    pag.press(self.use[0][i])
                    self.timer[self.use[0][i]] = datetime.now()
            self.fight = 1
            sleep(1.6)
            return False
        pixel2 = img2[447:472, 520:546]
        diff = cv2.absdiff(img_looting, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 1:
            self.fight = 0
            sleep(5)
            return False
        return True
    
    def exit_dange(self):

        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = img2[578:635, 1118:1165]
        diff = cv2.absdiff(img_dange, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 2.2:
            print('dange')
            keyboard.press_and_release('a')
            sleep(10)
            return False
        return True

    def looting(self):
        sleep(5)
        self.move = 1

    def RUN(self):
        print('START')
        while 1:
            if self.exit_dange():
                if self.atack_or_looting():
                    if self.skaning():
                        pag.click(self.dviz[0][0], self.dviz[0][1])
                        self.dviz = self.dviz[1:] + [self.dviz[0]]
                        sleep(1.7)

running = 1
def qexit():
    global running
    running = 0
    print('EXIT')
    qx()

bot = Bot_API()


keyboard.add_hotkey("alt+s", lambda: bot.vector_move())
keyboard.add_hotkey("alt+c", lambda: bot.clear_dviz())   
keyboard.add_hotkey("alt+p", lambda: bot.RUN())
keyboard.add_hotkey("alt+k", lambda: qexit())
print('APP WAS LOADED')

while running:
    sleep(3)