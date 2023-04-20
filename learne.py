from ultralytics import YOLO

model = YOLO()

model.train(model = 'yolov8l.pt', imgsz = 1282,  data = 'data_custom.yaml', dropout = 0.5, epochs = 100, lr0 = 0.05, verbose = True, optimizer = 'Adam')

model.export()
