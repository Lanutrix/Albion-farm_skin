import os
from PIL import ImageGrab
from datetime import datetime
from ultralytics import YOLO
from time import sleep
from time import sleep
import predict_img
import keyboard
from sys import exit as qx
    
def main():
    api.START()
    while 1:
        screenshot = ImageGrab.grab()
        screenshot.save('13yolo.jpg')
        sleep(0.01)
        results = model.predict('13yolo.jpg', show = False, save=True, imgsz=(640, 480), conf=0.65, line_thickness = 1)
        api.push_data(results)
        os.remove('13yolo.jpg') 
        sleep(0.1)
  
model = YOLO('pyst.pt') 
api = predict_img.Bot_API()
keyboard.add_hotkey("alt+s", lambda: api.vector_move())   
keyboard.add_hotkey("alt+p", lambda: main()) 
keyboard.add_hotkey("alt+c", lambda: api.clear_dviz())
keyboard.add_hotkey("alt+k", lambda: qx()) 
print(model.names)

 
while 1: 
    sleep(100)