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

class Bot_API:
    def __init__(self) -> None:
        self.names = {0: 'bird', 1: 'dbird', 2: 'ddeer',
                      3: 'deer', 4: 'dolen', 5: 'dpuma',
                      6: 'olen', 7: 'puma'}
        self.mode = 0
        """
        mode = 0, это бег
        mode = 1, это убийца
        mode = 2, это лутальня
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
                    flag = mobs[1][point] in [1, 2, 4, 5]
            
            if flag:
                self.looting(nearest_point)
            else:
                self.fight(nearest_point)
        else:
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

    def looting(self, xy):
        self.mode = 2
        pag.click(xy[0], xy[1])
        sleep(5)

    def fight(self, xy):
        self.mode = 1
        pag.click(xy[0], xy[1])
        sleep(1)
        pag.press('space')
        pag.press('r')
        pag.press('space')
        sleep(1.5)
        pag.press('space')
        pag.press('e')
        pag.press('space')
        sleep(1.5)
        pag.press('space')
        pag.press('q')
        pag.press('space')
        sleep(1)
        pag.press('space')


# bot = Bot_API().START()
