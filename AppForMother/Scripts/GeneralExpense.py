import tkinter as tk
from tkinter import ttk
import numpy as np
#from tkinter import *
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date


class MainGeneral(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):
        self.toolbar = tk.Frame(self,bg = "white", bd = 2)
        self.toolbar.pack(side = tk.TOP, fill = tk.X)
        
        buttonImage = Image.open('d://Apps/images/add.png')
        self.add_img = ImageTk.PhotoImage(buttonImage) 
        self.btn_open_dialog = tk.Button(self.toolbar, text = "Добавить позицию", command = self.open_dialog, bg = "white", bd =0, compound = tk.TOP, image = self.add_img)
        self.btn_open_dialog.pack(side = tk.LEFT)
        
        buttonImage = Image.open('d://Apps/images/refresh.png')
        self.refresh_img = ImageTk.PhotoImage(buttonImage) 
        self.btn_refresh = tk.Button(self.toolbar, text = "Обновить", command = self.update, bg = "white", bd =0, compound = tk.TOP, image = self.refresh_img)
        self.btn_refresh.pack(side = tk.LEFT)
        
        buttonImage = Image.open('d://Apps/images/update.png')
        self.update_img = ImageTk.PhotoImage(buttonImage) 
        self.btn_update = tk.Button(self.toolbar, text = "Редактировать", command = self.open_edit, bg = "white",
                               bd =0, compound = tk.TOP, image = self.update_img)
        self.btn_update.pack(side = tk.LEFT)
        
        buttonImage = Image.open('d://Apps/images/delete.png')
        self.delete_img = ImageTk.PhotoImage(buttonImage) 
        self.btn_delete = tk.Button(self.toolbar, text = "Удалить", command = self.delete_update, bg = "white", bd =0, compound = tk.TOP, image = self.delete_img)
        self.btn_delete.pack(side = tk.LEFT)
        
        
        self.tree = ttk.Treeview(self, columns = ('ID','Year','Month','Period','Name','Sum'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Year', width = 70, anchor = tk.CENTER)
        self.tree.column('Month', width = 80, anchor = tk.CENTER)
        self.tree.column('Period', width = 90, anchor = tk.CENTER)
        self.tree.column('Name', width = 120, anchor = tk.CENTER)
        self.tree.column('Sum', width = 100, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = '№')
        self.tree.heading('Year',text = 'Год')
        self.tree.heading('Month',text = 'Месяц')
        self.tree.heading('Period',text = 'Период')
        self.tree.heading('Name',text = 'Название')
        self.tree.heading('Sum',text = 'Сумма')
        
        data = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)
        
    def open_dialog(self):
        Child()
        
    def open_edit(self):
        if self.tree.selection() != ():
            n = int(self.tree.set(self.tree.selection()[0])["ID"])
            Child_edit(n, self)

    def delete_update(self):
        self.delete()
        self.update()

    def delete(self):
        df = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        list = []
        for selection_item in self.tree.selection():
            list.append(int(self.tree.set(selection_item, '#1')))
        del_list = []
        quarter_list = ['Q1','Q2','Q3','Q4']
        for i in list:
            if df.loc[i]['Period'] == 'Месячный':
                if i not in del_list:
                    del_list.append(i)
            elif df.loc[i]['Period'] in quarter_list:
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period'] and df.loc[j]['Year'] == df.loc[i]['Year']:
                        if j not in del_list:
                            del_list.append(j)
            elif df.loc[i]['Period'] == 'Годовой':
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period'] and df.loc[j]['Year'] == df.loc[i]['Year']:
                        if j not in del_list:
                            del_list.append(j)
            elif df.loc[i]['Period'] == '3-х годовой':
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period']:
                        if j not in del_list:
                            del_list.append(j)
        df = df.drop(del_list)
        df.to_csv ('d://Apps/Data/GeneralExpense.csv', encoding = 'utf-8',index=False)
        
        
    def update(self):
        data = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        text = data.columns.values
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        
        data.set_index(np.arange(len(data.index))) 
        data["ID"] = (np.arange(len(data.index)))
        data.to_csv ('d://Apps/Data/GeneralExpense.csv', encoding = 'utf-8',index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
            
    def chosen(self,n):
        df = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        year = df.loc[n]["Year"]
        month = df.loc[n]["Month"]
        period = df.loc[n]["Period"]
        name = df.loc[n]["Name"]
        sum = df.loc[n]["Sum"]
        quater_list = ['Q1', 'Q2','Q3', 'Q4']
        list = []
        if period == 'Месячный':
            list = [year, period, month, name, sum]
        elif period in quater_list:
            list = [year, "Квартальный", period, name, round(sum*3)]
        elif period == 'Годовой':
            list = [year, period, ' ', name, round(sum*12)]
        elif period == '3-х годовой':
            list = [year, period, int(year)+2, name, round(sum*36)]
        return list

    def edit_rows(self):
        df = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        list = []
        for selection_item in self.tree.selection():
            list.append(int(self.tree.set(selection_item, '#1')))
        del_list = []
        quarter_list = ['Q1','Q2','Q3','Q4']
        for i in list:
            if df.loc[i]['Period'] == 'Месячный':
                if i not in del_list:
                    del_list.append(i)
            elif df.loc[i]['Period'] in quarter_list:
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period'] and df.loc[j]['Year'] == df.loc[i]['Year']:
                        if j not in del_list:
                            del_list.append(j)
            elif df.loc[i]['Period'] == 'Годовой':
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period'] and df.loc[j]['Year'] == df.loc[i]['Year']:
                        if j not in del_list:
                            del_list.append(j)
            elif df.loc[i]['Period'] == '3-х годовой':
                text = df.columns.values
                for j in range(len(df[text[0]])):
                    if df.loc[j]['Period'] == df.loc[i]['Period']:
                        if j not in del_list:
                            del_list.append(j)
        return(del_list)

    
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        
        
    def init_child(self):
        self.title("Добавить общие расходы")
        self.geometry("400x220+550+150")
        self.resizable(False, False)
        self["bg"] = "white"
        self.grab_set()
        self.focus_set()
        

        label_year = tk.Label(self, text = 'Год:',bg = 'white')
        label_year.place(x = 50 , y = 20)

        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y = 50)

        label_period = tk.Label(self, text = 'Период:',bg = 'white')
        label_period.place(x = 50 , y = 80)

        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =110)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =140)

        self.month1_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        self.quarter1_list = ['Q1','Q2','Q3','Q4']
        self.year1_list = ['2018','2019','2020','2021','2022']

        self.month_list = ['Поездака в Москву','Пенсионный фонд','Бухгалтеры','Прочее']
        self.quater_list = ['Патент']
        self.year_list = ['ОФД кассы','1 % от дохода']
        self.year3_list = ['Замена фиск. касс']

        def change_name_period(event):
            if self.entery_type.get() == 'Месячный':
                list1 = self.month_list
                period_list  = self.month1_list
            elif self.entery_type.get() == 'Квартальный':
                list1 = self.quater_list
                period_list  = self.quarter1_list
            elif self.entery_type.get() == 'Годовой':
                list1 = self.year_list
                self.entery_period.delete(0, tk.END)
                self.entery_period.config(state=tk.DISABLED)
            elif self.entery_type.get() == '3-х годовой':
                list1 = self.year3_list
                self.entery_period.delete(0, tk.END)
                self.entery_period.insert(0, int(self.entery_year.get()) + 2)
                self.entery_year.config(state=tk.DISABLED)
                self.entery_period.config(state=tk.DISABLED)

            self.entery_name = ttk.Combobox(self, values=list1)
            self.entery_name.place(x = 200, y = 110)

            if self.entery_type.get() != 'Годовой' and self.entery_type.get() != '3-х годовой':
                self.entery_period.config(state=tk.NORMAL)
                self.entery_year.config(state=tk.NORMAL)
                self.entery_period = ttk.Combobox(self, values=period_list)
                self.entery_period.place(x = 200, y = 80)


        self.entery_year = ttk.Combobox(self,values = self.year1_list)
        d = datetime.date.today()
        self.entery_year.insert(0, d.strftime("%Y"))
        self.entery_year.place(x = 200, y = 20)

        self.entery_name = ttk.Combobox(self, values = [''])
        self.entery_name.place(x = 200, y = 110)

        self.entery_period = ttk.Combobox(self, values = [''])
        self.entery_period.place(x = 200, y = 80)

        self.entery_type = ttk.Combobox(self, values = ['Месячный','Квартальный','Годовой','3-х годовой'])
        self.entery_type.bind("<<ComboboxSelected>>", change_name_period)
        self.entery_type.place(x = 200, y = 50)

        self.entery_money = ttk.Entry(self)
        self.entery_money.place(x = 200, y = 140)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 170)
        
        btn_add = tk.Button(self, text = 'Добавить',bg = 'white')
        btn_add.place(x = 220, y =170)
        btn_add.bind('<Button-1>', lambda event: self.detect(self.entery_year.get(),self.entery_name.get(),self.entery_type.get(),
                                                             self.entery_period.get(),self.entery_money.get()))
    def detect(self,year,name,type,period,money):
        if type  == 'Месячный':
            self.insert(year, period,type, name, money)

        if type == 'Квартальный':
            if period == 'Q1':
                self.insert(year, self.month1_list[0], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[1], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[2], period, name, round(int(money) / 3, 2))
            if period == 'Q2':
                self.insert(year, self.month1_list[3], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[4], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[5], period, name, round(int(money) / 3, 2))
            if period == 'Q3':
                self.insert(year, self.month1_list[6], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[7], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[8], period, name, round(int(money) / 3, 2))
            if period == 'Q4':
                self.insert(year, self.month1_list[9], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[10], period, name, round(int(money) / 3, 2))
                self.insert(year, self.month1_list[11], period, name, round(int(money) / 3, 2))

        if type == 'Годовой':
            for i in self.month1_list:
                self.insert(year, i, type, name, round(int(money) / 12, 2))

        if type == '3-х годовой':
            for y in range(3):
                for m in self.month1_list:
                    self.insert(int(year) + int(y), m, type, name, round(int(money) / 36, 2))


    def insert(self, year, month, period, name, sum):
        data = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,year, month, period, name, sum]
        data.loc[len(data[text[0]])] = list
        data.to_csv ('d://Apps/Data/GeneralExpense.csv', encoding = 'utf-8',index=False)
        self.destroy()
        

class Child_edit(tk.Toplevel):
    
    def __init__(self,n, main):
        super().__init__()
        self.main = main
        self.n = n
        self.init_child()
        
        
    def init_child(self):
        self.title("Редактировать общие расходы")
        self.geometry("400x250+550+150")
        self.resizable(False, False)
        self["bg"] = "white"
        self.grab_set()
        self.focus_set()
        

        input_list = self.main.chosen(self.n)

        self.edit_list = self.main.edit_rows()

        self.month1_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

        label_year = tk.Label(self, text = 'Год:',bg = 'white')
        label_year.place(x = 50 , y = 20)

        label_type = tk.Label(self, text = 'Тип:',bg = 'white')
        label_type.place(x = 50 , y = 50)

        label_period = tk.Label(self, text = 'Период:',bg = 'white')
        label_period.place(x = 50 , y = 80)

        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =110)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =140)

        month_list = ['Поездака в Москву','Пенсионный фонд','Бухгалтеры','Прочее']
        quater_list = ['Патент']
        year_list = ['ОФД кассы','1 % от дохода']
        year3_list = ['Замена фиск. касс']

        month1_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        quarter1_list = ['Q1','Q2','Q3','Q4']
        year1_list = ['2018','2019','2020','2021','2022']


        self.entery_year = ttk.Combobox(self,values = year1_list)
        self.entery_year.insert(0, input_list[0])
        self.entery_year.place(x = 200, y = 20)


        month_list = ['Поездка в Москву','Пенсионный фонд','Бухгалтеры','Прочее']
        quater_list = ['Патент']
        year_list = ['ОФД кассы','1 % от дохода']
        year3_list = ['Замена фиск. касс']

        def change_name_period(event):
            if self.entery_type.get() == 'Месячный':
                list1 = month_list
                period_list  = month1_list
            elif self.entery_type.get() == 'Квартальный':
                list1 = quater_list
                period_list  = quarter1_list
            elif self.entery_type.get() == 'Годовой':
                list1 = year_list
                self.entery_period.delete(0, tk.END)
                self.entery_period.config(state=tk.DISABLED)
            elif self.entery_type.get() == '3-х годовой':
                list1 = year3_list
                self.entery_period.delete(0, tk.END)
                self.entery_period.insert(0, int(self.entery_year.get()) + 2)
                self.entery_year.config(state=tk.DISABLED)
                self.entery_period.config(state=tk.DISABLED)

            self.entery_name = ttk.Combobox(self, values=list1)
            self.entery_name.place(x = 200, y = 110)

            if self.entery_type.get() != 'Годовой' and self.entery_type.get() != '3-х годовой':
                self.entery_period.config(state=tk.NORMAL)
                self.entery_year.config(state=tk.NORMAL)
                self.entery_period = ttk.Combobox(self, values=period_list)
                self.entery_period.place(x = 200, y = 80)

        self.entery_type = ttk.Combobox(self, values = ['Месячный','Квартальный','Годовой','3-х годовой'])
        self.entery_type.insert(0, input_list[1])
        self.entery_type.bind("<<ComboboxSelected>>", change_name_period)
        self.entery_type.place(x = 200, y = 50)

        self.entery_name = ttk.Combobox(self, values = [''])
        self.entery_name.insert(0, input_list[3])
        self.entery_name.place(x = 200, y = 110)

        self.entery_period = ttk.Combobox(self, values = [''])
        self.entery_period.insert(0, input_list[2])
        if input_list[1] == '3-х годовой':
            self.entery_period.config(state=tk.DISABLED)
        if input_list[1] == 'Годовой':
            self.entery_period.config(state=tk.DISABLED)
        self.entery_period.place(x = 200, y = 80)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.insert(0, input_list[4])
        self.entery_money.place(x = 200, y = 140)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 170)
        
        btn_edit = tk.Button(self, text = 'Редактировать',bg = 'white')
        btn_edit.place(x = 200, y =170)
        btn_edit.bind('<Button-1>', lambda event: self.edit(self.entery_year.get(),self.entery_type.get(),self.entery_period.get(),
                                                            self.entery_name.get(),self.entery_money.get()))
    
    def edit(self,year, type, period, name, money):
        self.main.delete()
        Child.detect(self,year,name,type,period,money)

    def insert(self, year, month, period, name, sum):
        data = pd.read_csv('d://Apps/Data/GeneralExpense.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,year, month, period, name, sum]
        data.loc[len(data[text[0]])] = list
        data.to_csv ('d://Apps/Data/GeneralExpense.csv', encoding = 'utf-8',index=False)
        self.destroy()
                

   
        