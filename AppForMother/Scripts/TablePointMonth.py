import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date

class MainPointMonthTable(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):

        self.grab_set()
        self.focus_set()

        label1 = tk.Label(self, text = 'Выберите отдел:',bg = 'white', font = ("Helvetica", 9, "bold"))
        label1.place(x = 100 , y = 20)

        label2 = tk.Label(self, text = 'Отдел:',bg = 'white')
        label2.place(x = 100 , y = 60)

        self.entery_point = ttk.Combobox(self, values = ['Сити1', 'Сити2','Сити3','Ман1','Ман2','Радуга','ТДЖ','Сити4','Вавилон','Искра','Магнит','Рынок7','Валентина'])
        self.entery_point.insert(0, 'Сити1')
        self.entery_point.place(x = 160, y = 60)

        btn_show = tk.Button(self, text = 'Показать',bg = 'white')
        btn_show.bind('<Button-1>', lambda event: self.open_table(self.entery_point.get()))
        btn_show.place(x = 100, y = 100)

    def open_table(self, point):
        Table(point)
    
class Table(tk.Toplevel):
    def __init__(self, point):
        super().__init__()
        self.point = point
        self.init_main()
    
    def init_main(self):
        self.title(self.point + " за месяцы лет")
        self["bg"] = "white"
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        
        sells = pd.read_csv('d://Apps/Data/Sells.csv')
        general_expense = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        point_expense = pd.read_csv('d://Apps/Data/PointExpense.csv')
        text = sells.columns.values
        for i in range(len(sells[text[0]])):
            m = datetime.datetime.strptime(sells['Date'].loc[i],"%Y-%m-%d").date()
            sells.loc[i, 'Date'] = str(m.strftime("%B"))
            sells.loc[i, 'ID'] = int(m.strftime("%Y"))
        sells.rename(columns={ 'Date': 'Month', 'ID':'Year','Price':'Sum'}, inplace=True)
        sells = sells.groupby(by=['Year','Month','Point'], as_index = False).sum()

        general_expense = general_expense.groupby(by=['Year','Month'], as_index = False).sum()

        point_expense = point_expense.groupby(by=['Year','Month', 'Point'], as_index = False).sum()
        text1 = sells.columns.values
        text2 = point_expense.columns.values
        for i in range(len(sells[text1[0]])):
            for j in range(len(point_expense[text2[0]])):
                if sells.loc[i]['Year'] == point_expense.loc[j]['Year']:
                    if sells.loc[i]['Month'] == point_expense.loc[j]['Month']:
                        if sells.loc[i]['Point'] == point_expense.loc[j]['Point']:
                            sells.loc[i,'Sum'] =  sells.loc[i]['Sum'] - point_expense.loc[j]['Sum']
        new_df = sells

        general_expense = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        general_expense = general_expense.groupby(by=['Year','Month'], as_index = False).sum()
        numbers_points = pd.read_csv('d://Apps/Data/NumbersOfPoints.csv')
        text = general_expense.columns.values
        for i in range(len(general_expense[text[0]])):
            y = int(general_expense.loc[i]['Year'])
            m = str(general_expense.loc[i]['Month'])
            s = int(general_expense.loc[i]['Sum'])
            
            mask = numbers_points['Year'].values == y
            df = numbers_points[mask]
            n = int(df[m])
            general_expense.loc[i,'Sum'] = round(s / n, 2)
        minus_general = general_expense

        text1 = new_df.columns.values
        text2 = minus_general.columns.values
        for i in range(len(new_df[text1[0]])):
            for j in range(len(minus_general[text2[0]])):
                if new_df.loc[i]['Year'] == minus_general.loc[j]['Year']:
                    if new_df.loc[i]['Month'] == minus_general.loc[j]['Month']:
                            new_df.loc[i,'Sum'] =  new_df.loc[i]['Sum'] - minus_general.loc[j]['Sum']


        sells = new_df
    #конец вычитания ---------------------------------------------------------------------------------------------------
        
        mask = sells['Point'].values == self.point
        sells = sells[mask]
        df = pd.DataFrame(columns = ['Year','January','February','March','April','May','June','July','August','September','October','November','December','Total','Mean'])
        years = sells.groupby(by=['Year'], as_index = False).sum()["Year"].to_list()
        for i in years:
            n = np.nan
            list1 = list1 = [i,n,n,n,n,n,n,n,n,n,n,n,n,n,n]
            df.loc[i] = list1
        text = sells.columns.values
        for i in range(len(sells[text[0]])):
            df.loc[int(sells.iloc[i]['Year']), str(sells.iloc[i]['Month'])] = round(sells.iloc[i]['Sum'],1)
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']  
        df_sum = df[month_list]
        df['Total'] = df_sum.sum(axis=1)
        df['Mean'] = round(df_sum.mean(axis = 1,skipna = 1),2)

        columns = ['Year','January','February','March','April','May','June','July','August','September','October','November','December','Total', 'Mean']
        columns_rus = ['Год','Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь','Итого','Средние']
        self.tree = ttk.Treeview(self, columns = columns, height = 15, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        for i in columns:
            self.tree.column(i, width = 100, anchor = tk.CENTER)
        
        for i in columns:
            m = columns_rus[columns.index(i)]
            self.tree.heading(i, text = m)
        
        data = df
        data = data.set_index(np.arange(len(data.index))) 
        text = data.columns.values
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)