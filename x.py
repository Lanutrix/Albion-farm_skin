# import cv2
# from datetime import datetime
# img = cv2.imread('move_zone.png')[146:150,400:535]
# dt = datetime.now
# ts = dt()
# for i in range(46,84):
    
#     img2 = cv2.imread(f'map\Screenshot_{i}.png')[146:150,400:535]
#     t1 = dt()
#     diff = cv2.absdiff(img, img2)
#     similarity = cv2.mean(diff)[0]
#     print(similarity, dt()-t1)
# print(dt()-ts)

import pyautogui as pag
from time import sleep
sleep(2)
pag.click(740, 560)