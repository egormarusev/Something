import tkinter as tk
from tkinter import ttk
import numpy as np
#from tkinter import *
import pandas as pd
import datetime
from datetime import  time, date
import os
#import matplotlib
#import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
#plt.style.use('ggplot')


class MainAnalysis(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):

        os.remove('d://Apps/Data/period_file.csv')
        df = pd.DataFrame(columns = ['y1','m1','d1','y2','m2','d2',])
        df.to_csv ('d://Apps/Data/period_file.csv', encoding = 'utf-8',index=False)

        label_period = tk.Label(self, text = 'Период:',bg = 'white')
        label_period.place(x = 30 , y = 20)

        label_graphics = tk.Label(self, text = 'Вид графика:',bg = 'white')
        label_graphics.place(x = 30 , y = 60)

        label_type = tk.Label(self, text = 'Тип анализа:',bg = 'white')
        label_type.place(x = 30 , y = 100)
        
        self.entery_period = ttk.Entry(self)
        #self.entery_period.configure(state=tk.DISABLED)
        self.entery_period.place(x = 120, y = 20)


        self.insert_period()
            

        self.btn_period = tk.Button(self,text = 'Выбрать период',bg = 'white',command = self.open_period)
        self.btn_period.place(x = 270, y= 17)

        self.entery_graphics = ttk.Combobox(self, values = ['Столбчатый', 'Круговой', 'Линейный'])
        self.entery_graphics.place(x = 120, y = 60)

        self.entery_type = ttk.Combobox(self, values = ['Доходы - Расходы', 'Доходы', 'Расходы', 'Лучший месяц', 'Лучшая неделя', 'Лучший день недели'])
        self.entery_type.place(x = 120, y = 100)

        #btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        #btn_cancel.place(x = 110, y= 140)

        btn_show = tk.Button(self, text = 'Показать',bg = 'white', command = self.open_graphics)
        btn_show.place(x = 30, y =140)
    
    def open_graphics(self):
        Graphics(self.entery_graphics.get(), self.entery_type.get())

    def open_period(self):
        Child(self)

    def insert_period(self):
            data = pd.read_csv('d://Apps/Data/period_file.csv')
            if not data.empty:
                y1 = data.loc[0]['y1']
                m1 = data.loc[0]['m1']
                d1 = data.loc[0]['d1']
                y2 = data.loc[0]['y2']
                m2 = data.loc[0]['m2']
                d2 = data.loc[0]['d2']
                s = str(d1) + '.'+ str(m1) + '.' + str(y1) + '-' + str(d2) + '.'+ str(m2) + '.' + str(y2)
                self.entery_period.delete(0, tk.END)
                self.entery_period.insert(0, s)
            else:
                self.entery_period.delete(0, tk.END)
                self.entery_period.insert(0, 'Период не выбран')
                #self.entery_period.configure(state=tk.DISABLED)



class Child(tk.Toplevel):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.init_child()
        
        
    def init_child(self):
        self.title("Период анализа")
        self.geometry("400x300+550+150")
        self.resizable(False, False)
        self.grab_set()
        self["bg"] = "white"
        self.focus_set()
          
        label_ask1 = tk.Label(self, text = 'Введите дату начала',bg = 'white',font=("Helvetica", 9, "bold"))
        label_ask1.place(x = 50 , y =20)
        
        label_year1 = tk.Label(self, text = 'Год:',bg = 'white')
        label_year1.place(x = 50 , y =50)
        
        label_month1 = tk.Label(self, text = 'Месяц:',bg = 'white')
        label_month1.place(x = 50 , y =80)

        label_day1 = tk.Label(self, text = 'День:',bg = 'white')
        label_day1.place(x = 50 , y =110)

        label_ask2 = tk.Label(self, text = 'Введите дату конца',bg = 'white',font=("Helvetica", 9, "bold"))
        label_ask2.place(x = 50 , y =140)
        
        label_year2 = tk.Label(self, text = 'Год:',bg = 'white')
        label_year2.place(x = 50 , y =170)
        
        label_month2 = tk.Label(self, text = 'Месяц:',bg = 'white')
        label_month2.place(x = 50 , y =200)

        label_day2 = tk.Label(self, text = 'День:',bg = 'white')
        label_day2.place(x = 50 , y =230)

        year_list = ['2018','2019','2020','2021','2022']
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

        self.entery_year1 = ttk.Combobox(self, values = year_list)
        self.entery_year1.insert(0, datetime.date.today().strftime("%Y"))
        self.entery_year1.place(x = 120, y = 50)

        self.entery_month1 = ttk.Combobox(self, values = month_list)
        self.entery_month1.insert(0, datetime.date.today().strftime("%B"))
        self.entery_month1.place(x = 120, y = 80)

        self.entery_day1 = ttk.Entry(self)
        self.entery_day1.insert(0, datetime.date.today().strftime("%d"))
        self.entery_day1.place(x = 120, y = 110)


        self.entery_year2 = ttk.Combobox(self, values = year_list)
        self.entery_year2.insert(0, datetime.date.today().strftime("%Y"))
        self.entery_year2.place(x = 120, y = 170)

        self.entery_month2 = ttk.Combobox(self, values = month_list)
        self.entery_month2.insert(0, datetime.date.today().strftime("%B"))
        self.entery_month2.place(x = 120, y = 200)

        self.entery_day2 = ttk.Entry(self)
        self.entery_day2.insert(0, datetime.date.today().strftime("%d"))
        self.entery_day2.place(x = 120, y = 230)


        self.btn_period = tk.Button(self,text = 'Выбрать',bg = 'white')
        #month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        self.btn_period.place(x = 50, y= 260)
        self.btn_period.bind('<Button-1>', lambda event:  self.chose_period())


    def chose_period(self):
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        year1 = self.entery_year1.get()
        month1 = month_list.index(self.entery_month1.get()) + 1
        day1 = self.entery_day1.get()
        year2 = self.entery_year2.get()
        month2 = month_list.index(self.entery_month2.get()) + 1
        day2 = self.entery_day2.get()

        list1 = [str(year1),str(month1),str(day1),str(year2),str(month2),str(day2)]
        data = pd.read_csv('d://Apps/Data/period_file.csv')
        data.loc[0] = list1
        data.to_csv ('d://Apps/Data/period_file.csv', encoding = 'utf-8',index=False)
        self.main.insert_period()
        self.destroy()
"""
class Graphics():
    def __init__(self, graphic, type):
        super().__init__()
        self.graphic  = graphic
        self.type = type
        self.init_main()
    def init_main(self):
        df = pd.read_csv('d://Apps/Data/period_file.csv')
        self.date1 = date(df.loc[0]['y1'], df.loc[0]['m1'], df.loc[0]['d1'])
        self.date2 = date(df.loc[0]['y2'], df.loc[0]['m2'], df.loc[0]['d2'])

        if self.graphic == 'Столбчатый':
            if self.type  == 'Доходы':
                df = pd.read_csv('d://Apps/Data/Sells.csv')
                text = df.columns.values
                for i in range(len(df[text[0]])):
                    df.loc[i,'Date'] = datetime.datetime.strptime(df.loc[i]['Date'], '%Y-%m-%d').date()
                df = df.loc[(df['Date'] >= self.date1) & (df['Date'] <= self.date2)]
                self.bar_chart(df)

    def pie_chart(self):
        full_list = pd.read_csv('./data/db_full_list.csv')
        fig = plt.figure()
        axs = fig.add_axes([0, 0, 1, 1])
        axs.axis('equal')
        arg = ['Лето', 'Зима']
        val = [(full_list["Сезон"] == "Лето").sum(),
                (full_list["Сезон"] == "Зима").sum()]
        axs.pie(val, labels=arg, autopct='%1.2f%%')
        plt.show()

    def bar_chart(self, df):

        x = df['Date'].tolist()
        sum = df['Price'].tolist()

        x_pos = [i for i, _ in enumerate(x)]

        plt.bar(x_pos, sum, color='blue')
        plt.xlabel("Дата")
        plt.ylabel("Сумма")
        plt.title("Доход")

        plt.xticks(x_pos, x)

        plt.show()

    def box_chart(self):
        full_list = pd.read_csv('./data/db_full_list.csv')
        def boxplot(x_data, y_data, base_color="#539caf",
                    median_color="#297083", title=""):
            _, axs = plt.subplots()
            axs.boxplot(y_data, patch_artist=True,
                        medianprops={'color': median_color},
                        boxprops={'color': base_color,
                                    'facecolor': base_color},
                                    whiskerprops={'color': base_color},
                                    capprops={'color': base_color})
            axs.set_xticklabels(x_data)
            axs.set_ylabel('Кол-во')
            axs.set_title(title)
        boxplot(['Зима / Лето'],
                [(full_list["Сезон"] == "Зима").sum(),
                    (full_list["Сезон"] == "Лето").sum()])
"""

        
        




        