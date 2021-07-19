import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date


class MainTable(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):
        self.grab_set()
        self.focus_set()
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        tree = ttk.Treeview(self,style="mystyle.Treeview", columns = ('Year', 'Point','January','February','March','April','May','June','July','August','September','October','November','December'), height = 15, show = 'headings') 
        vsb = tk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        tree.column('Year', width = 60, anchor = tk.CENTER)
        tree.column('Point', width = 100, anchor = tk.CENTER)
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        month_list_rus = ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
        for i in month_list:
            tree.column(i, width = 110, anchor = tk.CENTER)
            

        tree.heading('Year',text = 'Год')
        tree.heading('Point',text = 'Отдел')
        for i in month_list:
            m = month_list_rus[month_list.index(i)]
            tree.heading(i, text = m)



            
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

        
        new_sells = sells
        new_sells['Point'] = new_sells['Point']

        table = pd.DataFrame(columns = ['Year', 'Point','January','February','March','April','May','June','July','August','September','October','November','December'])
        text = table.columns.values

        years = sells.groupby(by=['Year'], as_index = False).sum()["Year"].to_list()


        for i in years:
            list1 = [i, '','','','','','','','','','','','','']
            table.loc[i] = list1
            
        sells = sells.groupby(by=['Year',"Month"], as_index = False).sum()  
        text = sells.columns.values
        for i in range(len(sells[text[0]])):
            table.loc[int(sells.iloc[i]['Year']), sells.iloc[i]['Month']] = round(sells.iloc[i]['Sum'],1)   
        data = table
        df11 = data.set_index(np.arange(len(data.index))) 
        text = df11.columns.values
        for i in range(len(df11[text[0]])):
            tree.insert('', 'end',df11[text[0]][i],tags = "ttk", text=df11[text[0]][i], values = list(map(lambda x: df11[x][i], text[0:])))
            
        tree.tag_configure('ttk', background='yellow')

        #for i in range(len(data[text[0]])):
            #tree.item(data[text[0]][i], tags = "oddrow")

        text = data.columns.values
        for i in data[text[0]].to_list():
            sells = new_df
            y = int(data.loc[i]['Year'])
            sells.groupby(by=["Year","Point"], as_index = False).sum()
            mask = sells['Year'].values == int(y)
            df = sells[mask]
            points = df.groupby(by=["Point"], as_index = False).sum()["Point"].to_list()
            points_table = pd.DataFrame(columns = ['Year','Point','January','February','March','April','May','June','July','August','September','October','November','December'])
            for i in points:
                list1 = ['', i,0,0,0,0,0,0,0,0,0,0,0,0]
                points_table.loc[i] = list1
            
            sells = new_df
            sells = sells.groupby(by=['Year',"Month","Point"], as_index = False).sum()
            mask = sells['Year'].values == int(y)
            sells = sells[mask]
            text = sells.columns.values
            for i in range(len(sells[text[0]])):
                points_table.loc[sells.iloc[i]["Point"], sells.iloc[i]["Month"]] = round(sells.iloc[i]["Sum"],1)
                
            text = points_table.columns.values
            for i in range(len(points_table[text[0]])):
                tree.insert(y, 'end', text=points_table[text[0]][i], values = list(map(lambda x: points_table[x][i], text[0:])))

        tree.pack(side=tk.TOP,fill=tk.X)

