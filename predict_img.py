from ultralytics import YOLO

model = YOLO('yolov8n.pt') 
model = YOLO('D:\\server-part\\best.pt') 


results = model.predict('D:\\server-part\\dataset\\train\images\\16.png', save=True, imgsz=(1282,759), conf=0.001, show = True, line_thickness = 1)
pri = []
for r in results: #вывод всех распознанных классов
    for c in r.boxes.cls:
        print(model.names[int(c)])
        

print(pri)