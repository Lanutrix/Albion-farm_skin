from time import sleep
import pyautogui as pag
from random import randint

while 1:
    pag.moveTo(randint(100,1400),randint(100,900),2, pag.easeOutQuad)
    sleep(randint(5,15)/10)
    pag.scroll(randint(800,1100) if randint(0,1) else -randint(800,1100))
    sleep(randint(5,15))