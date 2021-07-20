import tkinter as tk
from tkinter import ttk
import PIL
from PIL import ImageTk, Image, ImageDraw
import numpy as np
from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
plt.style.use('ggplot')
import pandas as pd
import datetime
from datetime import  time, date
from calendar import monthrange
import os
os.environ['MATPLOTLIBDATA'] = 'location of mpl-data folder'


class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
    
    def init_main(self):

        root.geometry('300x300+600+250')

        self.lang = IntVar()
    
        r1 = Radiobutton(text='Dekstop',
                        variable=self.lang, value=0)
        r2 = Radiobutton(text='Mobile  ',
                        variable=self.lang, value=1)
        space1 = Label(width=20, height=4)
        space2 = Label(width=20, height=1)
        label = Label(width=20, height=2, text = 'Choose your version')
        btn = Button(root, text = "OK",width = 4,bd =2,font="Arial 11", command = self.choose_window)
        space1.pack()
        label.pack()
        r1.pack()
        r2.pack()
        space2.pack()
        btn.pack()

    def choose_window(self):
        k = self.lang.get()
        if k == 0:
            Dekstop()
        else:
            print('mobile')


class Dekstop(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_dekstop()
        
        
    def init_dekstop(self):
        self.title("Dekstop")
        self.geometry("550x560+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self["bg"] = "white"

        def paint(event):
            x1, y1 = (event.x - 3), (event.y - 3)
            x2, y2 = (event.x + 3), (event.y + 3)
            cv.create_oval(x1, y1, x2, y2, fill="black",width=18)
            draw.line([x1, y1, x2, y2],fill="black",width=18)
    
        def clear():
            cv.delete('all')
            draw.rectangle((0, 0, 520, 520), fill=(255, 255, 255, 0))




        width =  520
        height = 520
        center = height//2
        white = (255, 255, 255)
        #создаем поле для рисования(холст)
        cv = Canvas(root, width=width, height=height, bg='white')
        # PIL создает пустое изображение и русет на нем
        image1 = PIL.Image.new("RGB", (width, height), white)
        draw = ImageDraw.Draw(image1)
        #само рисование на холсте
        cv.bind("<B1-Motion>", paint)
        #Параметры текста вывод

        #Привязка функций кнопкам
        btnClear = Button(root, text = "Clear",width = 6,bd =3,font="Arial 11", command = lambda:clear())
        cv.place(x= 10, y =30)
        btnClear.place(x = 465, y = 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Draw A Penis")
    root.geometry('300x300+600+250')
    root.resizable(False, False)
    root.mainloop()