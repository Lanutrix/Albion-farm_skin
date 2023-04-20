class c:
    xyxy = [[448.4319, 231.9960, 614.9921, 320.8406]]

x=(int(c.xyxy[0][0])+int(c.xyxy[0][2]))//2
y=(int(c.xyxy[0][1])+int(c.xyxy[0][3]))//2
print(x, y)