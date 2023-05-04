import cv2
import math
import threading
import pyautogui as pag
from time import sleep
from datetime import datetime
from datetime import timedelta


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

class Bot_API:
    def __init__(self) -> None:
        self.names = {0: 'antilop', 1: 'birdt3', 2: 'dantilop',
                      3: 'dbirdt3', 4: 'dbirdt5', 5: 'ddeer',
                      6: 'deer', 7: 'dpuma'}
        self.mode = 0
        """
        mode = 0 (бегать),
        mode = 1 (убивать),
        mode = 2 (лутать),
        mode = 3 (телепорт)
        """
        self.skills = [3, 30, 15]
        self.dviz = []
        self.starting = 0

        print(scrn)
    
    def START(self):
        self.starting = 1
        print('START')
        thread = threading.Thread(target=self.movement, args=())
        thread.start()
    
    def vector_move(self):
        self.dviz += [pag.position()]
        print(self.dviz)

    def clear_dviz(self):
        print('CLEAR')
        self.dviz = []

    def push_data(self, results):
        mobs = [[], []]
        for r in results: #вывод всех распознанных классов
            for c in r.boxes:
                x=(int(c.xyxy[0][0])+int(c.xyxy[0][2]))//2
                y=(int(c.xyxy[0][1])+int(c.xyxy[0][3]))//2
                mobs[0].append([x ,y])
            for c in r.boxes.cls:
                mobs[1].append(int(c))
        print(mobs)
        if mobs[0]:

            x1, y1 = person
            min_distance = 10_000
            nearest_point = None

            for point in range(len(mobs[1])):
                print(point)

                x2, y2 = mobs[0][point][0], mobs[0][point][1]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = mobs[0][point]
            self.mode = 1   
            pag.click(nearest_point)
            
            sleep(10)
            self.mode = 0        
            
    def movement(self):
        while 1:
            if self.dviz:
                for i in self.dviz:
                    if self.mode == 0:
                        pag.click(i[0], i[1])
                        sleep(1.6)
                    else:
                        sleep(2)
                else:
                    sleep(1)

    def scan(self):
        while 1:
            # atack
            img2 = cv2.imread(path_screen)
            pixel2 = img2[33:37, 298:400]
            diff = cv2.absdiff(img_atack, pixel2)
            similarity = cv2.mean(diff)[0]
            if similarity < 5:
                self.mode = 1
                self.fight()
                continue
            
            #looting
            pixel2 = img2[447:472, 520:546]
            diff = cv2.absdiff(img_atack, pixel2)
            similarity = cv2.mean(diff)[0]
            if similarity < 1:
                self.mode = 2
                self.looting()
                continue

    def fight(self):
        sleep(1)
        pag.press('r')
        sleep(0.2)
        pag.press('r')
        sleep(0.2)

    def looting(self):
        pass

# bot = Bot_API().START()
