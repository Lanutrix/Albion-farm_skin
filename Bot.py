from math import sqrt
import os
from PIL import ImageGrab
from datetime import datetime, timedelta
import keyboard
import numpy as np
from ultralytics import YOLO
import pyautogui as pag
import cv2
import threading
from sys import exit as qx
from time import sleep


model = YOLO('pyst.pt')
scrn    = list(pag.size())

left    = [scrn[0]//2+400, scrn[1]//2]
right   = [scrn[0]//2-400, scrn[1]//2]
up      = [scrn[0]//2, scrn[1]//2+300]
down    = [scrn[0]//2, scrn[1]//2-300]


person  = [scrn[0]//2, scrn[1]//2-50]
path_screen = '13yolo.jpg'


img_atack = cv2.imread('atack.png')
img_atack = img_atack[33:37, 298:400]

img_looting = cv2.imread('looting.png')
img_looting = img_looting[447:472, 520:546]

dviz = [[scrn[0]//2+400, scrn[1]//2],
    [scrn[0]//2-400, scrn[1]//2],
    [scrn[0]//2, scrn[1]//2+300],
    [scrn[0]//2, scrn[1]//2-300]]
 
class Bot_API:
    def __init__(self) -> None:
        self.start = 1
        self.skan = 1 # 0, 1, 2 (run,kill,loot)
        self.use = [    ['r','e','q'],
                        [timedelta(0,30), timedelta(0,15), timedelta(0,3)]
                   ]
        self.timer = {i : datetime.now() for i in self.use[0]}
        self.dviz = []

    def atack_press_skills(self):
        while 1:
            for i in range(len(self.use[0])):
                if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                    pag.press(self.use[0][i])
                    self.timer[self.use[0][i]] = datetime.now()
            sleep(1.3)
        sleep(1)

    def vector_move(self):
        self.dviz += [pag.position()]
        print(self.dviz)

    def clear_dviz(self):
        print('CLEAR')
        self.dviz = []

    def movement(self):
        for i in self.dviz:
            pag.click(i[0], i[1])
            sleep(1.6)

    def skaning(self):
        while 1:
            if self.skan == 0:
                screenshot = ImageGrab.grab()
                screenshot.save('13yolo.jpg')
                sleep(0.01)
                results = model.predict('13yolo.jpg', show = False, save=False, imgsz=(1280, 736), conf=0.65, line_thickness = 1)
                self.push_data(results)
                os.remove('13yolo.jpg')
                sleep(0.3)
            else:
                sleep(1)

    def push_data(self, results):
        mobs = [[], []]
        for r in results: #вывод всех распознанных классов
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
            sleep(1)

    def atack_or_looting(self):
        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = img2[33:37, 298:400]
        diff = cv2.absdiff(img_atack, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 2.4:
            self.skan = 1
            print('atack')
            pag.press('space')
            sleep(1)
            pag.press('r')
            sleep(1)
            pag.press('e')
            sleep(10)
        pixel2 = img2[447:472, 520:546]
        diff = cv2.absdiff(img_looting, pixel2)
        similarity = cv2.mean(diff)[0]
        if similarity < 1:
            print('looting')
            self.skan = 2
            sleep(10)

            sleep(1)
            self.skan = 0
            

    def looting(self):
        sleep(5)
        self.move = 1

    def RUN(self):
        self.start = 0
        print('START')
        skaning_thread = threading.Thread(target=self.skaning, args=())
        skaning_thread.start()

        movement_thread = threading.Thread(target=self.movement, args=())
        movement_thread.start()

        atack_or_looting = threading.Thread(target=self.atack_or_looting, args=())
        atack_or_looting.start()

        atack_press_skills_thread = threading.Thread(target=self.atack_press_skills, args=())
        atack_press_skills_thread.start()

        looting_thread = threading.Thread(target=self.looting, args=())
        looting_thread.start()
    

bot = Bot_API()


keyboard.add_hotkey("alt+s", lambda: bot.vector_move())
keyboard.add_hotkey("alt+c", lambda: bot.clear_dviz())   
keyboard.add_hotkey("alt+p", lambda: bot.RUN())

while 1:
    sleep(100)