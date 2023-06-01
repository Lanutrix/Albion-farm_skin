print('STARTING APP...')
from time import sleep
from datetime import datetime
import json
import os
import keyboard
from ctypes import windll, Structure, c_long, byref
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
def get_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x, pt.y]



config = json.loads(open('config.json').read())

system_drive = f"{os.getenv('APPDATA')}\\Skinner"
print(system_drive)
try:
    os.mkdir(system_drive)
except:
    pass


class Bot_APIii:
    def __init__(self) -> None:
        try:
            self.dviz = config["movement"]
        except:
            self.dviz = []

    def vector_move(self):
        xy = get_mouse_position()
        self.dviz += [[xy[0], xy[1]]]
        print(self.dviz)

    def clear_dviz(self):
        self.dviz = []

    def save_dviz(self):
        global config
        config['movement'] = self.dviz
        open('config.json', 'w').write(json.dumps(config))

    def qexit(self):
        self.clear_dviz()
        self.vector_move()
        self.save_dviz()
        global running
        running = 0
    
    def qexitss(self):
        global running
        running = 0
 
running = 1


print('''
Текущая конфигурация:''')
print(f'''[+] Точность для определяемого объекта: {config['cnn']}''')
print(f'''[+] Прожимаемые скилы: {config['skills']}''')
try:
    print(f'''[+] Траектория движения: {config['movement']}
''' if config['movement'] else "[-] Траектория движения: \n")
except:
    print("[-] Траектория движения: \n")

bot = Bot_APIii()

keyboard.add_hotkey("alt+s", lambda: bot.qexitss())
keyboard.add_hotkey("alt+p", lambda: bot.qexit())

while running:
    sleep(1)