import os
from PIL import ImageGrab
from datetime import datetime
from ultralytics import YOLO
from time import sleep
import pyautogui

model = YOLO('best1.pt') 

n = 0
while 1:
    screenshot = ImageGrab.grab()
    screenshot.save('13yolo.jpg')
    sleep(0.01)
    results = model.predict('D:\\sserver-part\\13yolo.jpg', show = False, save=True, imgsz=(1282,759), conf=0.51, line_thickness = 1)
    pri = []
    for r in results: #вывод всех распознанных классов
        for c in r.boxes:
            print(c.xyxy[0])

            pyautogui.click(x=(int(c.xyxy[0][0])+int(c.xyxy[0][2]))//2, y=(int(c.xyxy[0][1])+int(c.xyxy[0][3]))//2)
            break
            
    os.remove('13yolo.jpg')
    sleep(0.1)
