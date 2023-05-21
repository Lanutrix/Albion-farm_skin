import psutil
import pyautogui as pag
import tkinter as tk
from tkinter import messagebox
root = tk.Tk()
root.withdraw()

scrn    = list(pag.size())
processes = psutil.process_iter()
flag = 1

dtnt = [0, 0]

for i in processes:
    if i.name() == 'Albion-Online.exe':
        flag = 0
        dtnt[0] = 1

if scrn!=[1280, 720]:
    messagebox.showerror("Неправильное разрешение экрана",
                                             "Установите разрешение 1280х720")
else:
    dtnt[1] = 1

if flag:
    messagebox.showerror("Запустите игру",
                                             "На данный момент Albion-Online не запущен")
    
if dtnt[0] and dtnt[1]:
    print(';lbfd;kmlfd')