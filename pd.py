import pyautogui as pag
from time import sleep
from random import randint

n = 0
while 1:
    for i in range(randint(2,8)):
        pag.moveTo(randint(100,1300), randint(100,800), 1)
    delta = randint(10,20)
    n+=1
    print(n)
    sleep(delta)