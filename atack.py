from datetime import datetime, timedelta
from time import sleep
import pyautogui as pag
import threading

class Atackment:
    def __init__(self) -> None:
        self.use = [    ['r','e','q'],
                        [timedelta(0,30), timedelta(0,15), timedelta(0,3)]
                   ]
        self.timer = {i : datetime.now() for i in self.use[0]}


    def hendler(self):
        for i in range(30):
            for i in range(len(self.use[0])):
                print(datetime.now(), self.timer[self.use[0][i]], self.use[1][i])
                if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                    pag.press(self.use[0][i])
                    self.timer[self.use[0][i]] = datetime.now()
            sleep(1.3)
    
    def atack_run(self):
        thread = threading.Thread(target=self.hendler, args=())
        thread.start()
a = Atackment().atack_run()