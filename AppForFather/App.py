import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
#from tkinter import *
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

        #import warnings
        #import numpy as np
        #warnings.simplefilter(action='ignore', category=FutureWarning)
        #print('x' in np.arange(5))  

        toolbar = tk.Frame(bg = "white", bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)
        
        buttonImage = Image.open('add1.png')
        self.add_img = ImageTk.PhotoImage(buttonImage) 

        btn_open_dialog = tk.Button(toolbar, text = "Добавить позицию", command = self.open_dialog, bg = "white", bd =0, compound = tk.TOP, image = self.add_img)
        btn_open_dialog.pack(side = tk.LEFT)
        
        buttonImage = Image.open('refresh1.png')
        self.refresh_img = ImageTk.PhotoImage(buttonImage) 
        btn_refresh = tk.Button(toolbar, text = "Обновить", command = self.update, bg = "white", bd =0, compound = tk.TOP, image = self.refresh_img)
        btn_refresh.pack(side = tk.LEFT)

        buttonImage = Image.open('update.png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage) 

        btn_update = tk.Button(toolbar, text = "Редактировать", command = self.open_edit, bg = "white",
                               bd =0, compound = tk.TOP, image = self.buttonPhoto)
        btn_update.pack(side = tk.LEFT)

        
        buttonImage = Image.open('delete.png')
        self.delete_img = ImageTk.PhotoImage(buttonImage) 
        btn_delete = tk.Button(toolbar, text = "Удалить", command = self.delete, bg = "white", bd =0, compound = tk.TOP, image = self.delete_img)
        btn_delete.pack(side = tk.LEFT)

        buttonImage = Image.open('search.png')
        self.search_img = ImageTk.PhotoImage(buttonImage) 
        btn_search = tk.Button(toolbar, text = "Поиск",command = self.open_search,  bg = "white", bd =0, compound = tk.TOP,image = self.search_img)
        btn_search.pack(side = tk.LEFT)

        buttonImage = Image.open('table.png')
        self.general_img = ImageTk.PhotoImage(buttonImage) 
        btn_general = tk.Button(toolbar, text = "Общая таблица",command = self.open_general,  bg = "white", bd =0, compound = tk.TOP,image = self.general_img)
        btn_general.pack(side = tk.LEFT)

        buttonImage = Image.open('all_table.png')
        self.details_img = ImageTk.PhotoImage(buttonImage) 
        btn_general = tk.Button(toolbar, text = "Подробнee",command = self.open_details,  bg = "white", bd =0, compound = tk.TOP,image = self.details_img)
        btn_general.pack(side = tk.LEFT)
        
        
        self.tree = ttk.Treeview(self, columns = ('ID', 'Date','Type','Name','SubType','Sum'), height = 15, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Date', width = 110, anchor = tk.CENTER)
        self.tree.column('Type', width = 120, anchor = tk.CENTER)
        self.tree.column('Name', width = 150, anchor = tk.CENTER)
        self.tree.column('SubType', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 115, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = 'ID')
        self.tree.heading('Date',text = 'Дата')
        self.tree.heading('Type',text = 'Доход / Расход')
        self.tree.heading('Name',text = 'Название')
        self.tree.heading('SubType',text = 'Тип')
        self.tree.heading('Sum',text = 'Сумма')
        
        data = pd.read_csv('DataBase.csv')
        data['Sum'] = np.round(data['Sum'], 2)
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack()
        
    def open_dialog(self):
        Child()

    def open_general(self):
        General()

    def open_details(self):
        Details()

    def open_search(self):
        Search()
        
        
    def open_edit(self):
        if self.tree.selection() != ():
            n = int(self.tree.set(self.tree.selection()[0])["ID"])
            Child_edit(n)
    
    def delete(self):
        df = pd.read_csv('DataBase.csv')
        list = []
        for selection_item in self.tree.selection():
            list.append(int(self.tree.set(selection_item, '#1')))
        df = df.drop(list)
        df.to_csv ('DataBase.csv', encoding = 'utf-8',index=False)
        self.update()
        
        
    def update(self):
        data = pd.read_csv('DataBase.csv')
        text = data.columns.values
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        
        data.set_index(np.arange(len(data.index))) 
        data["ID"] = (np.arange(len(data.index)))
        data.to_csv ('DataBase.csv', encoding = 'utf-8',index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
            
    def chosen(self,n):
        df = pd.read_csv('DataBase.csv')
        Date = df.loc[n]["Date"]
        Type = df.loc[n]["Type"]
        Name = df.loc[n]["Name"]
        Subtype = df.loc[n]["SubType"]
        Sum = df.loc[n]["Sum"]
        list = [Date,Type,Name,Subtype,Sum]
        return list

    
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        
        
    def init_child(self):
        self.title("Добавить доходы / расходы")
        self.geometry("400x220+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self["bg"] = "white"
        
        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =80)
        
        label_combobox = tk.Label(self, text = 'Доход/Расход:',bg = 'white')
        label_combobox.place(x = 50 , y =20)
        
        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y =50)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =110)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =140)
        
        def change_date():
            if self.check.get() == 1:
                self.entery_date.config(state=tk.NORMAL)
                self.entery_date.insert(0, '')
            elif self.check.get() == 0:
                self.entery_date.delete(0, tk.END)
                self.entery_date.insert(0, date.today())
                self.entery_date.config(state=tk.DISABLED)
        
        self.check = tk.BooleanVar()
        self.check.set(0)
        self.check_date = tk.Checkbutton(self,text="Не сегодня", variable=self.check, onvalue=1, offvalue=0,
                                         command = change_date,bg = 'white')
        self.check_date.place(x = 100, y = 140)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, datetime.date.today())
        self.entery_date.config(state=tk.DISABLED)
        self.entery_date.place(x = 200, y = 140)

        self.entery_name = ttk.Combobox(self, values = [''])
        self.entery_name.place(x = 200, y = 80)
    
        def change_name(event):
            df = pd.read_csv('d://AppForFather/DataBase.csv')
            df = df.groupby(by=["SubType","Name"], as_index = False).sum()
            mask = df['SubType'] == self.entery_type.get()
            df = df[mask]
            name_list = df["Name"].to_list()
            self.entery_name.delete(0, tk.END)
            self.entery_name = ttk.Combobox(self, values = name_list)
            self.entery_name.place(x = 200, y = 80)

        encome_list = ['Зарплата','Деньги с квартиры']
        buy_list = ['Еда','Напитки','Алкоголь','Быт.расх.','Кошки','ЖКХ-22','ЖКХ-23','Бензин','Прочее']
        
        self.entery_type = ttk.Combobox(self, values = buy_list)
        self.entery_type.bind("<<ComboboxSelected>>",change_name)
        self.entery_type.place(x = 200, y = 50)
        
    
        def change_type(event):
            if self.description.get() == 'Доход':
                list = encome_list
            elif self.description.get() == 'Расход':
                list = buy_list
            self.entery_type = ttk.Combobox(self, values = list)
            self.entery_type.bind("<<ComboboxSelected>>",change_name)
            self.entery_type.place(x = 200, y = 50)
        
        self.description = ttk.Combobox(self, values = ['Расход','Доход'])
        self.description.insert(0, 'Расход')
        self.description.bind("<<ComboboxSelected>>",change_type)
        self.description.place(x = 200, y =20)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.place(x = 200, y = 110)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy)
        btn_cancel['bg'] = 'white'
        btn_cancel.place(x = 300, y= 170)
        
        btn_add = tk.Button(self, text = 'Добавить')
        btn_add['bg'] = 'white'
        btn_add.place(x = 220, y =170)
        btn_add.bind('<Button-1>', lambda event: self.insert(self.entery_name.get(),self.entery_money.get(),
                                                             self.entery_type.get(),self.description.get(),
                                                             self.entery_date.get()))
        
        
    def insert(self,name, money, type, description,date):
        data = pd.read_csv('DataBase.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,date,description,name,type,money]
        data.loc[len(data[text[0]])] = list
        data.to_csv ('DataBase.csv', encoding = 'utf-8',index=False)
        self.destroy()
        

class Child_edit(tk.Toplevel):
    
    def __init__(self,n):
        super().__init__()
        self.main = Main(root)
        self.n = n
        self.init_child()
        
        
    def init_child(self):
        self.title("Редактировтаь товар")
        self.geometry("400x220+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self["bg"] = "white"
        

        input_list = self.main.chosen(self.n)
        
        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =80)
        
        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y =50)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =110)
        
        label_description = tk.Label(self, text = 'Расход/Доход:',bg = 'white')
        label_description.place(x = 50 , y =20)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =140)
        
        def change_date():
            if self.check.get() == 1:
                self.entery_date.config(state=tk.NORMAL)
                self.entery_date.insert(0, '')
            elif self.check.get() == 0:
                self.entery_date.delete(0, tk.END)
                self.entery_date.insert(0, input_list[0])
                self.entery_date.config(state=tk.DISABLED)
        
        self.check = tk.BooleanVar()
        self.check.set(0)
        self.check_date = tk.Checkbutton(self,text="Не этот день", variable=self.check, onvalue=1, offvalue=0,
                                         command = change_date,bg = 'white')
        self.check_date.place(x = 100, y = 140)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, input_list[0])
        self.entery_date.config(state=tk.DISABLED)
        self.entery_date.place(x = 200, y = 140)

        
        df = pd.read_csv('d://AppForFather/DataBase.csv')
        df = df.groupby(by=["SubType","Name"], as_index = False).sum()
        mask = df['SubType'] == input_list[3]
        df = df[mask]
        name_list = df["Name"].to_list()

        self.entery_name = ttk.Combobox(self, values = name_list)
        self.entery_name.insert(0, input_list[2])
        self.entery_name.place(x = 200, y = 80)
        
        encome_list = ['Зарплата','Деньги с квартиры','Акции']
        buy_list = ['Еда','Напитки','Алкоголь','Быт.расх.','Кошки','ЖКХ-22','ЖКХ-23','Бензин','Прочее']

        def change_name(event):
            df = pd.read_csv('d://AppForFather/DataBase.csv')
            df = df.groupby(by=["SubType","Name"], as_index = False).sum()
            mask = df['SubType'] == self.entery_type.get()
            df = df[mask]
            name_list = df["Name"].to_list()
            self.entery_name.delete(0, tk.END)
            self.entery_name = ttk.Combobox(self, values = name_list)
            self.entery_name.place(x = 200, y = 80)

        type_list = []
        if input_list[1] == 'Расход':
            type_list = buy_list
        else:
            type_list = encome_list
        self.entery_type = ttk.Combobox(self, values = type_list)
        self.entery_type.insert(0, input_list[3])
        self.entery_type.bind("<<ComboboxSelected>>",change_name)
        self.entery_type.place(x = 200, y = 50)

        def change_type(event):
            if self.entery_description.get() == 'Доход':
                list = encome_list
            elif self.entery_description.get() == 'Расход':
                list = buy_list
            self.entery_type = ttk.Combobox(self, values = list)
            self.entery_type.bind("<<ComboboxSelected>>",change_name)
            self.entery_type.place(x = 200, y = 50)
        
        self.entery_description = ttk.Combobox(self, values = ['Расход', 'Доход'])
        self.entery_description.insert(0, input_list[1])
        self.entery_description.bind("<<ComboboxSelected>>",change_type)
        self.entery_description.place(x = 200, y =20)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.insert(0, input_list[4])
        self.entery_money.place(x = 200, y = 110)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 170)
        
        btn_edit = tk.Button(self, text = 'Редактировать',bg = 'white')
        btn_edit.place(x = 200, y =170)
        btn_edit.bind('<Button-1>', lambda event: self.edit(self.entery_name.get(),self.entery_money.get(),
                                                             self.entery_type.get(),self.entery_description.get(),
                                                            self.entery_date.get()))
        
    def edit(self,name, money, type, description, date):
        data = pd.read_csv('DataBase.csv')
        #text = data.columns.values
        list =[self.n,date,description,name,type,money]
        data.loc[self.n] = list
        data.to_csv ('DataBase.csv', encoding = 'utf-8',index=False)
        self.destroy()
        
class General(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self.init_child()
        self["bg"] = "white"
        
        
    def init_child(self):
        self.title("Общая таблица")
        self.geometry("665x420+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        
        self.toolbar = tk.Frame(self,bg = "white", bd = 4)
        self.toolbar.pack(side = tk.TOP, fill = tk.X)

        buttonImage = Image.open('graph.png')
        self.graph = ImageTk.PhotoImage(buttonImage) 
        self.btn1 = tk.Button(self.toolbar, text = "График", bg = "white", bd =0, compound = tk.TOP,command = self.open_graph, image = self.graph)
        self.btn1.pack(side = tk.LEFT)

        self.tree = ttk.Treeview(self, columns = ('Year','Month','SubType','Sum'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("Year", width = 50, anchor = tk.CENTER)
        self.tree.column('Month', width = 110, anchor = tk.CENTER)
        self.tree.column('SubType', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 115, anchor = tk.CENTER)
        
        self.tree.heading('Year',text = 'Год')
        self.tree.heading('Month',text = 'Месяц')
        self.tree.heading('SubType',text = 'Тип')
        self.tree.heading('Sum',text = 'Сумма')
        
        df = pd.read_csv('d://AppForFather/DataBase.csv')
        text = df.columns.values
        for i in range(len(df[text[0]])):
            m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
            df.loc[i, 'Date'] = m.strftime("%B")
            df.loc[i, 'ID'] = m.strftime("%Y")
        df.rename(columns={'ID': 'Year'}, inplace=True)

        data = df.groupby(by=['Year',"Date", "SubType"], as_index = False).sum()
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)

    def open_graph(self):
        GeneralGraph()

class Details(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self.init_child()
        self["bg"] = "white"
        
        
    def init_child(self):
        self.title("Подробная таблица")
        self.geometry("665x420+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        
        self.toolbar = tk.Frame(self,bg = "white", bd = 4)
        self.toolbar.pack(side = tk.TOP, fill = tk.X)

        buttonImage = Image.open('graph.png')
        self.graph = ImageTk.PhotoImage(buttonImage) 
        self.btn1 = tk.Button(self.toolbar, text = "График", bg = "white", bd =0, compound = tk.TOP,command = self.open_graph, image = self.graph)
        self.btn1.pack(side = tk.LEFT)

        self.tree = ttk.Treeview(self, columns = ('Year','Month','SubType','Name','Sum'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("Year", width = 50, anchor = tk.CENTER)
        self.tree.column('Month', width = 110, anchor = tk.CENTER)
        self.tree.column('SubType', width = 120, anchor = tk.CENTER)
        self.tree.column('Name', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 115, anchor = tk.CENTER)
        
        self.tree.heading('Year',text = 'Год')
        self.tree.heading('Month',text = 'Месяц')
        self.tree.heading('SubType',text = 'Тип')
        self.tree.heading('Name',text = 'Название')
        self.tree.heading('Sum',text = 'Сумма')
        
        df = pd.read_csv('d://AppForFather/DataBase.csv')
        text = df.columns.values
        for i in range(len(df[text[0]])):
            m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
            df.loc[i, 'Date'] = m.strftime("%B")
            df.loc[i, 'ID'] = m.strftime("%Y")
        df.rename(columns={'ID': 'Year'}, inplace=True)

        data = df.groupby(by=['Year',"Date", "SubType","Name"], as_index = False).sum()
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)

    def open_graph(self):
        DetailsGraph()

class Search(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self.init_child()
        self["bg"] = "white"
        
        
    def init_child(self):
        self.title("Поиск")
        self.geometry("500x210+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_period = tk.Label(self, text = 'Год:',bg = 'white')
        label_period.place(x = 50 , y =20)

        self.entery_year = ttk.Combobox(self,values = ['2018', '2019','2020', '2021','2022'])
        d = datetime.date.today()
        self.entery_year.insert(0, d.strftime("%Y"))
        self.entery_year.place(x = 150, y = 20)

        label_period = tk.Label(self, text = 'Период:', bg = 'white')
        label_period.place(x = 50 , y =50)

        label_ot = tk.Label(self, text = 'От:', bg = 'white')
        label_ot.place(x = 120 , y =50)

        label_do = tk.Label(self, text = 'До:', bg = 'white')
        label_do.place(x = 300 , y =50)

        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

        self.entery_month1 = ttk.Combobox(self,values = month_list)
        d = datetime.date.today()
        self.entery_month1.insert(0, d.strftime("%B"))
        self.entery_month1.place(x = 150, y = 50)

        self.entery_month2 = ttk.Combobox(self,values = month_list)
        d = datetime.date.today()
        self.entery_month2.insert(0, d.strftime("%B"))
        self.entery_month2.place(x = 330, y = 50)

        label_description = tk.Label(self, text = 'Расход/Доход:',bg = 'white')
        label_description.place(x = 50 , y =80)

        self.entery_description = ttk.Combobox(self,values = ['Расход', 'Доход'])
        self.entery_description.insert(0, 'Расход')
        self.entery_description.place(x = 150, y = 80)
        
        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y =110)

        def change_name(event):
            df = pd.read_csv('d://AppForFather/DataBase.csv')
            df = df.groupby(by=["SubType","Name"], as_index = False).sum()
            mask = df['SubType'] == self.entery_type.get()
            df = df[mask]
            name_list = df["Name"].to_list()
            name_list.append("Без названия")
            self.entery_name.delete(0, tk.END)
            self.entery_name = ttk.Combobox(self, values = name_list)
            self.entery_name.insert(0, 'Без названия')
            self.entery_name.place(x = 150, y = 140)

        self.entery_type = ttk.Combobox(self,values = ['Без типа','Еда','Напитки','Алкоголь','Быт.расх.','Кошки','ЖКХ-22','ЖКХ-23','Бензин','Прочее'])
        self.entery_type.insert(0, 'Без типа')
        self.entery_type.bind("<<ComboboxSelected>>",change_name)
        self.entery_type.place(x = 150, y = 110)
        
        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =140)

        self.entery_name = ttk.Combobox(self)
        self.entery_name.insert(0, 'Без названия')
        self.entery_name.place(x = 150, y = 140)

        btn_show = tk.Button(self, text = 'Показать')
        btn_show['bg'] = 'white'
        btn_show.bind('<Button-1>', lambda event: self.filter(self.entery_year.get(), self.entery_month1.get(), self.entery_month2.get(),
                                                                                 self.entery_description.get(), self.entery_type.get(), self.entery_name.get()))
        btn_show.place(x = 50, y= 170)

    def filter(self,y, m1, m2, description, type, name):
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        date1 = date(int(y) ,month_list.index(m1) + 1, 1)
        date2 = date(int(y) ,month_list.index(m2) + 1, monthrange(int(y), month_list.index(m2) + 1)[1])

        if type == 'Без типа':
            type = ''

        if name == 'Без названия':
            name = ''

        df = pd.read_csv('d://AppForFather/DataBase.csv')
        text = df.columns.values
        for i in range(len(df[text[0]])):
            df.loc[i, 'Date'] = datetime.datetime.strptime(df.loc[i, 'Date'], '%Y-%m-%d').date()

        full_list = df.loc[(df['Date'] >= date1) & (df['Date'] <= date2)]
        
        f_dict = {}
        headers = ["Type","Name","SubType"]
        s_list = [description, name, type]
        k = -1
        for i in s_list:
            k += 1
            f_dict[headers[k]] = i
        for i in f_dict:
            if f_dict[i] != '':
                full_list = full_list[lambda full_list: (full_list[i] == f_dict[i])]
        filtered_list = full_list
        filtered_list.to_csv ('Filtered.csv', encoding = 'utf-8',index=False)
        Filtered()

        
class Filtered(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self["bg"] = "white"
        self.init_child()
        
        
    def init_child(self):
        self.title("Отфильтрованная таблица")
        self.geometry("665x420+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        self.tree = ttk.Treeview(self, columns = ('ID', 'Date','Type','Name','SubType','Sum'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Date', width = 110, anchor = tk.CENTER)
        self.tree.column('Type', width = 120, anchor = tk.CENTER)
        self.tree.column('Name', width = 150, anchor = tk.CENTER)
        self.tree.column('SubType', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 115, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = 'ID')
        self.tree.heading('Date',text = 'Дата')
        self.tree.heading('Type',text = 'Доход / Расход')
        self.tree.heading('Name',text = 'Название')
        self.tree.heading('SubType',text = 'Тип')
        self.tree.heading('Sum',text = 'Сумма')
        
        data = pd.read_csv('Filtered.csv')
        os.remove('Filtered.csv')
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack()

class GeneralGraph(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self["bg"] = "white"
        self.init_child()
        
        
    def init_child(self):
        self.title("График")
        self.geometry("350x150+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_period = tk.Label(self, text = 'Год:',bg = 'white')
        label_period.place(x = 50 , y =20)

        self.entery_year = ttk.Combobox(self,values = ['2018', '2019','2020', '2021','2022'])
        d = datetime.date.today()
        self.entery_year.insert(0, d.strftime("%Y"))
        self.entery_year.place(x = 150, y = 20)

        label_month = tk.Label(self, text = 'Месяц:', bg = 'white')
        label_month.place(x = 50 , y =50)

        month_list = ["Не выбрано",'January','February','March','April','May','June','July','August','September','October','November','December']

        self.entery_month1 = ttk.Combobox(self,values = month_list)
        d = datetime.date.today()
        self.entery_month1.insert(0, "Не выбрано")
        self.entery_month1.place(x = 150, y = 50)

        label_description = tk.Label(self, text = 'Расход/Доход:',bg = 'white')
        label_description.place(x = 50 , y =80)

        self.entery_description = ttk.Combobox(self,values = ['Расход', 'Доход'])
        self.entery_description.insert(0, 'Расход')
        self.entery_description.place(x = 150, y = 80)
        
        btn_show = tk.Button(self, text = 'Показать')
        btn_show['bg'] = 'white'
        btn_show.bind('<Button-1>', lambda event: self.pre_graph(self.entery_year.get(),self.entery_month1.get(),self.entery_description.get()  ))
        btn_show.place(x = 50, y= 110)
    
    def pre_graph(self, year, month, description):
        df = pd.read_csv('d://AppForFather/DataBase.csv')

        if month == "Не выбрано":

            text = df.columns.values
            for i in range(len(df[text[0]])):
                m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
                df.loc[i, 'Date'] = int(m.strftime("%Y"))
                df.loc[i, 'Type'] = str(df.loc[i, 'Type'])
                df.loc[i, 'SubType'] = str(df.loc[i, 'SubType'])

            df = df.groupby(by=['Date','SubType','Type'], as_index = False).sum().drop(["ID"], axis = 1)
            mask = df['Type'] == description
            df = df[mask]
            mask = df['Date'] == int(year)
            df = df[mask]
            df = df.drop(['Type'], axis = 1)
            df['Sum'] = np.round(df['Sum'], 2)

            x = df['SubType'].tolist()
            sum = df['Sum'].tolist()
            x_pos = [i for i, _ in enumerate(x)]
            plt.bar(x_pos, sum, color='blue')
            plt.xlabel("Типы")
            plt.ylabel("Сумма")
            if month == "Не выбрано":
                plt.title("Траты за " + str(year))
            else:
                plt.title("Траты за " + str(month) +" "+  str(year))
            plt.xticks(x_pos, x, fontsize= 9)
            plt.tick_params(axis='x', rotation=30)
            plt.show()

        else:
            df = pd.read_csv('d://AppForFather/DataBase.csv')
            text = df.columns.values
            for i in range(len(df[text[0]])):
                m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
                df.loc[i, 'Date'] = str(m.strftime("%B"))
                df.loc[i, 'ID'] = int(m.strftime("%Y"))
                df.loc[i, 'SubType'] = str(df.loc[i, 'SubType'])

            df.rename(columns={'ID': 'Year', 'Date': 'Month'}, inplace=True)

            df = df.groupby(by=['Year',"Month","SubType",'Type'], as_index = False).sum()

            mask = df['Type'] == description
            df = df[mask]
            mask = df['Year'] == int(year)
            df = df[mask]
            mask = df['Month'] == str(month)
            df = df[mask]
            df = df.drop(['Type'], axis = 1)
            df['Sum'] = np.round(df['Sum'], 2)


            x = df['SubType'].tolist()
            sum = df['Sum'].tolist()
            x_pos = [i for i, _ in enumerate(x)]
            plt.bar(x_pos, sum, color='blue')
            plt.xlabel("Типы")
            plt.ylabel("Сумма")
            if month == "Не выбрано":
                plt.title("Траты за " + str(year))
            else:
                plt.title("Траты за " + str(month) +" "+  str(year))
            plt.xticks(x_pos, x, fontsize= 9)
            plt.tick_params(axis='x', rotation=30)
            plt.show()




    

class DetailsGraph(tk.Toplevel):
    
    def __init__(self):
        super().__init__()
        self.main = Main(root)
        self.init_child()
        self["bg"] = "white"
        
        
    def init_child(self):
        self.title("График")
        self.geometry("400x210+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_period = tk.Label(self, text = 'Год:',bg = 'white')
        label_period.place(x = 50 , y =20)

        self.entery_year = ttk.Combobox(self,values = ['2018', '2019','2020', '2021','2022'])
        d = datetime.date.today()
        self.entery_year.insert(0, d.strftime("%Y"))
        self.entery_year.place(x = 150, y = 20)

        label_month = tk.Label(self, text = 'Месяц:', bg = 'white')
        label_month.place(x = 50 , y =50)

        month_list = ["Не выбрано",'January','February','March','April','May','June','July','August','September','October','November','December']

        self.entery_month1 = ttk.Combobox(self,values = month_list)
        d = datetime.date.today()
        self.entery_month1.insert(0, 'Не выбрано')
        self.entery_month1.place(x = 150, y = 50)

        label_description = tk.Label(self, text = 'Расход/Доход:',bg = 'white')
        label_description.place(x = 50 , y =80)

        self.entery_description = ttk.Combobox(self,values = ['Расход', 'Доход'])
        self.entery_description.insert(0, 'Расход')
        self.entery_description.place(x = 150, y = 80)
        
        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y =110)

        self.entery_type = ttk.Combobox(self,values = ['Еда','Напитки','Алкоголь','Быт.расх.','Кошки','ЖКХ-22','ЖКХ-23','Бензин','Прочее'])
        self.entery_type.insert(0, 'Еда')
        self.entery_type.place(x = 150, y = 110)
        
        btn_show = tk.Button(self, text = 'Показать')
        btn_show['bg'] = 'white'
        btn_show.bind('<Button-1>', lambda event: self.pre_graph(self.entery_year.get(),self.entery_month1.get(),self.entery_description.get(),self.entery_type.get()  ))
        btn_show.place(x = 50, y= 140)

    def pre_graph(self, year, month, description, type):
        df = pd.read_csv('d://AppForFather/DataBase.csv')
        #print(df)
        if month == "Не выбрано":

            text = df.columns.values
            for i in range(len(df[text[0]])):
                m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
                df.loc[i, 'Date'] = int(m.strftime("%Y"))
                df.loc[i, 'Type'] = str(df.loc[i, 'Type'])
                df.loc[i, 'SubType'] = str(df.loc[i, 'SubType'])

            df = df.groupby(by=['Date','SubType','Name','Type'], as_index = False).sum().drop(["ID"], axis = 1)
            mask = df['Type'] == description
            df = df[mask]
            mask = df['Date'] == int(year)
            df = df[mask]
            mask = df['SubType'] == type
            df = df[mask]
            df = df.drop(['Type'], axis = 1)
            df = df.drop(['SubType'], axis = 1)
            df['Sum'] = np.round(df['Sum'], 2)


            x = df['Name'].tolist()
            sum = df['Sum'].tolist()
            x_pos = [i for i, _ in enumerate(x)]
            plt.bar(x_pos, sum, color='blue')
            plt.xlabel("Названия")
            plt.ylabel("Сумма")
            plt.title("Траты за " + str(year) + ". "+ type)  
            plt.xticks(x_pos, x, fontsize= 9)
            plt.tick_params(axis='x', rotation=30)
            plt.show()

        else:
            df = pd.read_csv('d://AppForFather/DataBase.csv')
            text = df.columns.values
            for i in range(len(df[text[0]])):
                m = datetime.datetime.strptime(df['Date'].loc[i],"%Y-%m-%d").date()
                df.loc[i, 'Date'] = str(m.strftime("%B"))
                df.loc[i, 'ID'] = int(m.strftime("%Y"))
                df.loc[i, 'SubType'] = str(df.loc[i, 'SubType'])

            df.rename(columns={'ID': 'Year', 'Date': 'Month'}, inplace=True)

            df = df.groupby(by=['Year',"Month","SubType",'Name','Type'], as_index = False).sum()

            mask = df['Type'] == description
            df = df[mask]
            mask = df['Year'] == int(year)
            df = df[mask]
            mask = df['Month'] == str(month)
            df = df[mask]
            mask = df['SubType'] == type
            df = df[mask]
            df = df.drop(['Type'], axis = 1)
            df = df.drop(['SubType'], axis = 1)
            df['Sum'] = np.round(df['Sum'], 2)

            x = df['Name'].tolist()
            sum = df['Sum'].tolist()
            x_pos = [i for i, _ in enumerate(x)]
            plt.bar(x_pos, sum, color='blue')
            plt.xlabel("Названия")
            plt.ylabel("Сумма")
            plt.title("Траты за " + str(month) +" "+  str(year) + ". " + type)
            plt.xticks(x_pos, x, fontsize= 9)
            plt.tick_params(axis='x', rotation = 30)
            plt.show()
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Доходы и расходы")
    root.geometry("665x420+430+180")
    root.resizable(False, False)
    root.mainloop()
