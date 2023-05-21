from PIL import ImageGrab
from datetime import datetime
import numpy as np
import pyautogui as pag
import cv2
from time import sleep


path = r'C:\Users\Dmitry\Documents\Lightshot'
img_atack = cv2.imread('atack.png')
img_atack = img_atack[68:71, 283:295]

img_looting = cv2.imread('looting.png')
img_looting = img_looting[447:472, 520:546]

img_dange = cv2.imread('dange.png')
img_dange = img_dange[578:635, 1118:1165]
for i in range(1, 46):
        img2 = cv2.imread(path+f'\\Screenshot_{i}.png')
        pixel2 = img2[68:71, 283:295]
        diff = cv2.absdiff(img_atack, pixel2)
        similarity = cv2.mean(diff)[0]
        
        print(path+f'\\Screenshot_{i}.png'
              , similarity)
