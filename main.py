import json
# import pd
from math import sqrt
import os
from PIL import ImageGrab
from datetime import datetime, timedelta
import keyboard
import numpy as np
from ultralytics import YOLO
import psutil
import pyautogui as pag
import tkinter as tk
from tkinter import messagebox
import cv2
from sys import exit as qx
from time import sleep

pag.FAILSAFE = False
os.system('setting.exe')

root = tk.Tk()
root.withdraw()

config          = json.loads(open('config.json').read())
model           = YOLO('pyst.pt')
scrn            = list(pag.size())
timeout_looting = config["timeout_looting"]
timeout_move    = config["timeout_move"]

person  = [scrn[0]//2, scrn[1]//2-30]
system_drive = f"{os.getenv('APPDATA')}\\Skinner"
print(system_drive)
try:
    os.mkdir(system_drive)
except:
    pass
path_screen = '13yolo.jpg'


img_atack       = cv2.imread('atack.png')
img_atack       = img_atack[68:71, 283:295]

img_looting     = cv2.imread('looting.png')
img_looting     = img_looting[447:472, 520:546]

img_dange       = cv2.imread('dange.png')
img_dange       = img_dange[578:635, 1118:1165]
img_move_zone   = cv2.imread('move_zone.png')
img_move_zone   = img_move_zone[146:150,400:535]

dviz            = [ [scrn[0]//2+400, scrn[1]//2],
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
            self.dviz = config["movement"][0]
        except:
            self.dviz = []
        self.fight = 0

    def atack_press_skills(self):
        for i in range(len(self.use[0])):
            if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                pag.press(self.use[0][i])
                self.timer[self.use[0][i]] = datetime.now()

    def vector_move(self):
        xy = pag.position()
        self.dviz += [[xy[0], xy[1]]]
        print(self.dviz)

    def clear_dviz(self):
        print('CLEAR')
        self.dviz = []

    def save_dviz(self):
        global config
        print('SAVE CONFIG')
        config['movement'] = self.dviz
        open('config.json', 'w').write(json.dumps(config))

    def skaning(self):
        if self.fight:
            sleep(2.3)
            self.fight = 0
            return False
        screenshot = ImageGrab.grab()
        screenshot.save(path_screen)
        sleep(0.05)
        results = model.predict(path_screen, show = False, save=False, imgsz=(1280, 736), conf=config['cnn'], line_thickness = 1)
        sleep(0.05)
        os.remove(path_screen)
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
            pixel2 = img2[68:71, 283:295]
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
        pixel2 = self.img2[68:71, 283:295]
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
        pixel2 = self.img2[447:472, 520:546]
        diff = cv2.absdiff(img_looting, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 1:
            self.fight = 0
            sleep(timeout_looting)
            return False
        return True
    
    def exit_dange(self):
        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        self.img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = self.img2[578:635, 1118:1165]
        diff = cv2.absdiff(img_dange, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 2.2:
            print('dange')
            sleep(2)
            keyboard.press_and_release('a')
            sleep(10)
            self.scrolling()
            sleep(1)
            return False
        return True
    
    def check_map(self):
        if datetime.now() - self.last_scan > timedelta(0,3):
            maper = self.img2[554:660, 1086:1191]
            diff = cv2.absdiff(maper, self.map)
            similarity = cv2.mean(diff)[0]
            print(similarity)
            if int(similarity) == 0:
                self.map = maper
                self.reverse_dviz()
                self.last_scan = datetime.now()
                return False
            else:
                self.map = maper
                self.last_scan = datetime.now()
                
        diff = cv2.absdiff(img_move_zone, self.img2[146:150,400:535])
        similarity = cv2.mean(diff)[0]
        if similarity<0.1:
            pag.click(740, 560)
            self.reverse_dviz()
            self.reverse_dviz()   
            pag.click(self.dviz[0], self.dviz[1])
            pag.press('f')
            sleep(timeout_move) 
            return False
        return True

    def reverse_dviz(self):
        if self.dviz[0]>640 and self.dviz[1]>360:
            self.dviz[0] = 1280 - self.dviz[0]
        elif self.dviz[0]<640 and self.dviz[1]>360:
            self.dviz[1] = 720 - self.dviz[1]
        elif self.dviz[0]<640 and self.dviz[1]<360:
            self.dviz[0] = 1280 - self.dviz[0]
        else:
            self.dviz[1] = 720 - self.dviz[1]
        
    def scrolling(self):
        for i in range(20):
                pag.scroll(1000)
                sleep(0.03)


    def RUN(self):
        os.chdir(system_drive)
        print('START')            
        self.scrolling()

        pag.moveTo(1150,600)
        self.scrolling()

        pag.moveTo(640,360)

        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()

        self.map = img2[554:660, 1086:1191]
        self.last_scan = datetime.now()

        while 1:
            if self.exit_dange():
                if self.check_map():
                    if self.atack_or_looting():
                        if self.skaning():
                            pag.click(self.dviz[0], self.dviz[1])
                            pag.press('f')
                            sleep(timeout_move)
        




bot = Bot_API()


print('APP WAS LOADED')
sleep(3)
scrn    = list(pag.size())
processes = psutil.process_iter()
flag = 1

dtnt = [0, 0]

for i in processes:
    if i.name() == 'Albion-Online.exe':
        flag = 0
        dtnt[0] = 1

if scrn!=[1280, 720]:
    messagebox.showerror("Неправильное разрешение экрана",
                                            "Установите разрешение 1280х720")
else:
    dtnt[1] = 1

if flag:
    messagebox.showerror("Запустите игру",
                                            "На данный момент Albion-Online не запущен")
    
if dtnt[0] and dtnt[1]:
    bot.RUN()
else:
    print(bot.dviz)
    bot.reverse_dviz()
    print(bot.dviz)
    bot.reverse_dviz()
    bot.reverse_dviz()
    print(bot.dviz)
    bot.reverse_dviz()