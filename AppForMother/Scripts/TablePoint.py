import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date


class Table(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):
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
        df = pd.DataFrame(columns = ['Year'])

        years = sells.groupby(by=['Year'], as_index = False).sum()["Year"].to_list()
        point = sells.groupby(by=['Point'], as_index = False).sum()["Point"].to_list()
        indexer = ['Year']
        for_columns = ['Год']
        for i in point:
            indexer.append(i)
            for_columns.append(i)
        for i in years:
            list1 = [i]
            df.loc[i] = list1
            
        sells = sells.groupby(by=['Year',"Point"], as_index = False).sum()  
        text = sells.columns.values
        for i in range(len(sells[text[0]])):
            df.loc[int(sells.iloc[i]['Year']), str(sells.iloc[i]['Point'])] = round(sells.iloc[i]['Sum'],1)
        df = df[indexer]


        self.tree = ttk.Treeview(self, columns = for_columns, height = 15, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("Год", width = 100, anchor = tk.CENTER)
        for i in point:
            self.tree.column(i, width = 100, anchor = tk.CENTER)
        
        self.tree.heading("Год", text = "Год")
        for i in point:
            self.tree.heading(i, text = i)
        
        data = df
        text = data.columns.values
            
        #for i in range(len(data[text[0]])):
            #self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))

        for i in df['Year'].to_list():
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)