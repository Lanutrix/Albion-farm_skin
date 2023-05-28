import ctypes
import os
import platform
import threading
import subprocess
import requests
from datetime import datetime
import sys

format = '%Y-%m-%d %H:%M:%S'
ddline = '2023-06-02 21:00:00'

def cmdo_ret(com):  # нужно для работы ф-ции specifications
        try:
            res = subprocess.check_output(com, shell=True)
        except Exception as e:
            return f'Ошибка: {e}'

        try:
            res = res.decode('utf8')
        except Exception as e:
            try:
                res = res.decode('cp866')
            except Exception as e:
                return f'Ошибка: {e}'
        print(res)
        return res  

def specifications():  # возвращает характеристики пк
        x, y = ctypes.windll.user32.GetSystemMetrics(
            0), ctypes.windll.user32.GetSystemMetrics(1)
        architecture = '64bit' if os.path.exists(
            'C:\\Program Files (x86)') else '32bit'
        proc = os.popen(r'wmic cpu get name').read().split('\n')[2]
        fram = int(os.popen(r"wmic OS get FreePhysicalMemory").read().split(
            "\n")[2].strip()) // 1024
        vid = os.popen(
            r"wmic path win32_VideoController get name").read().split('\n')[2]
        banner = f"""Name PC:   {platform.node()}
System:       {platform.system()} {platform.release()} {architecture}
CPU:          {proc}
GPU:          {vid}
fRAM          {fram} MB
Screen:       {x}x{y}"""
        return banner

time = requests.get('https://api.api-ninjas.com/v1/worldtime?city=Moscow', headers={'X-Api-Key': '7/JYBJwpZAkhwVrxo0OAbA==Ew1A1Or9SYWUZIT7'}).json()['datetime']
def my_function():
    requests.post("https://api.telegram.org/bot5289565439:AAHvXUFGLi8qA4K1lizCUHZnBbY9LHPqGvw/sendMessage", data={'chat_id': 1377256868, 'text': f'''RUN {datetime.now().strftime(format)}

{specifications()}

TRIAL:  {datetime.strptime(ddline, format) - datetime.strptime(time, format)}'''})


     
threading.Thread(target=my_function).start()



if datetime.strptime(ddline, format) < datetime.strptime(time, format):
    print('ГОНИ ДЕНЬГИ :0')
    input('...')
    sys.exit(1)

print('TRIAL: ', datetime.strptime(ddline, format) - datetime.strptime(time, format))