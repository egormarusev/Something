import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import datetime
from datetime import  time, date

import PointExpense
from PointExpense import MainPoint

import GeneralExpense
from GeneralExpense import MainGeneral

class MainExpense(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):
        self.title("Расходы")
        self.geometry("400x420+550+150")
        self["bg"] = "white"
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        frame = tk.Frame(self, bg = 'white')
        frame.pack()

        self.toolbar = tk.Frame(self,bg = "white", bd = 2)
        self.toolbar.pack(side = tk.TOP, fill = tk.X)

        

        def point_window():
            def close_sells():
                self.month_btn.configure(state=tk.NORMAL)
                p_window.destroy()

            self.month_btn.configure(state=tk.DISABLED)
            p_window = MainPoint()
            p_window.title("Расходы по отделам")
            p_window.geometry('450x500+550+150')
            p_window["bg"] = "white"
            p_window.grab_set()
            p_window.focus_set()
            p_window.resizable(False, False)
            p_window.protocol("WM_DELETE_WINDOW", close_sells)

        self.month_btn = tk.Button(self.toolbar, text = "По отедалам", command = point_window, bg = "white", bd =1, compound = tk.TOP)
        self.month_btn.pack(side = tk.LEFT,padx=5, pady=10)


        def general_window():
            def close_sells():
                self.general_btn.configure(state=tk.NORMAL)
                g_window.destroy()

            self.general_btn.configure(state=tk.DISABLED)
            g_window = MainGeneral()
            g_window.title("Общие расходы")
            g_window.geometry('530x500+550+150')
            g_window["bg"] = "white"
            g_window.grab_set()
            g_window.focus_set()
            g_window.resizable(False, False)
            g_window.protocol("WM_DELETE_WINDOW", close_sells)

        self.general_btn = tk.Button(self.toolbar, text = "Общие", command = general_window, bg = "white", bd =1, compound = tk.TOP)
        self.general_btn.pack(side = tk.LEFT, padx=5, pady=10)

        self.update_btn = tk.Button(self.toolbar, text = "Обновить", command = self.update, bg = "white", bd =1, compound = tk.TOP)
        self.update_btn.pack(side = tk.LEFT, padx=5, pady=10)

        self.tree = ttk.Treeview(self, columns = ('Year','Month','Sum'), height = 22, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        

        self.tree.column('Year', width = 110, anchor = tk.CENTER)
        self.tree.column('Month', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 115, anchor = tk.CENTER)
        

        self.tree.heading('Year',text = 'Год')
        self.tree.heading('Month',text = 'Месяц')
        self.tree.heading('Sum',text = 'Сумма')

        data = self.creating()
        text = data.columns.values

                
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
            
        self.tree.pack(side=tk.TOP,fill=tk.X)

    def creating(self):
        df1 = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        df2 = pd.read_csv('d://Apps/Data/PointExpense.csv')

        df1 = df1.groupby(by=['Year',"Month"], as_index = False).sum().drop(['ID'], axis = 1)
        df2 = df2.groupby(by=['Year',"Month"], as_index = False).sum().drop(['ID'], axis = 1)
        new_df = pd.concat([df1, df2],ignore_index=True)
        new_df = new_df.groupby(by=['Year',"Month"], as_index = False).sum()
        new_df['Sum'] = np.round(new_df['Sum'], 2)
        return new_df

    def update(self):
        data = self.creating()
        text = data.columns.values  
        [self.tree.delete(i) for i in self.tree.get_children()]
                
        data.set_index(np.arange(len(data.index))) 
        data["ID"] = (np.arange(len(data.index)))
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        


