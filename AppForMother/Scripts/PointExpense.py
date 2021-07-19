import tkinter as tk
from tkinter import ttk
import numpy as np
#from tkinter import *
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date

class MainPoint(tk.Toplevel):
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
        self.btn_delete = tk.Button(self.toolbar, text = "Удалить", command = self.delete, bg = "white", bd =0, compound = tk.TOP, image = self.delete_img)
        self.btn_delete.pack(side = tk.LEFT)
        
        
        self.tree = ttk.Treeview(self, columns = ('ID','Year', 'Month','Point','Name','Sum'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Year', width = 60, anchor = tk.CENTER)
        self.tree.column('Month', width = 80, anchor = tk.CENTER)
        self.tree.column('Point', width = 80, anchor = tk.CENTER)
        self.tree.column('Name', width = 80, anchor = tk.CENTER)
        self.tree.column('Sum', width = 80, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = '№')
        self.tree.heading('Year',text = 'Год')
        self.tree.heading('Month',text = 'Месяц')
        self.tree.heading('Point',text = 'Отдел')
        self.tree.heading('Name',text = 'Название')
        self.tree.heading('Sum',text = 'Сумма')
        
        data = pd.read_csv('d://Apps/Data/PointExpense.csv')
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack(side=tk.TOP,fill=tk.X)
        
    def open_dialog(self):
        Child()
        
    def open_edit(self):
        if self.tree.selection() != ():
            n = int(self.tree.set(self.tree.selection()[0])["ID"])
            Child_edit(n,self)
    
    def delete(self):
        df = pd.read_csv('d://Apps/Data/PointExpense.csv')
        list = []
        for selection_item in self.tree.selection():
            list.append(int(self.tree.set(selection_item, '#1')))
        df = df.drop(list)
        df.to_csv ('d://Apps/Data/PointExpense.csv', encoding = 'utf-8',index=False)
        self.update()
        
        
    def update(self):
        data = pd.read_csv('d://Apps/Data/PointExpense.csv')
        text = data.columns.values
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        
        data.set_index(np.arange(len(data.index))) 
        data["ID"] = (np.arange(len(data.index)))
        data.to_csv ('d://Apps/Data/PointExpense.csv', encoding = 'utf-8',index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
            
    def chosen(self,n):
        df = pd.read_csv('d://Apps/Data/PointExpense.csv')
        Year = df.loc[n]["Year"]
        Month = df.loc[n]["Month"]
        Point = df.loc[n]["Point"]
        Name = df.loc[n]["Name"]
        Sum = df.loc[n]["Sum"]
        list = [Year,Month,Point,Name,Sum]
        return list

    
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        
        
    def init_child(self):
        self.title("Добавить расходы")
        self.geometry("400x220+550+150")
        self.resizable(False, False)
        self["bg"] = "white"       
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =110)
        
        label_point = tk.Label(self, text = 'Отдел:',bg = 'white')
        label_point.place(x = 50 , y =80)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =140)
        
        label_year = tk.Label(self, text = 'Год:',bg = 'white')
        label_year.place(x = 50 , y =20)

        label_month = tk.Label(self, text = 'Месяц:',bg = 'white')
        label_month.place(x = 50 , y =50)
        
        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        self.entery_year = ttk.Entry(self)
        d = datetime.date.today()
        self.entery_year.insert(0, d.strftime("%Y"))
        self.entery_year.place(x = 200, y = 20)

        self.entery_month = ttk.Combobox(self, values = month_list)
        d = datetime.date.today()
        self.entery_month.insert(0, d.strftime("%B"))
        self.entery_month.place(x = 200, y = 50)

        self.entery_point = ttk.Combobox(self, values = ['Сити1', 'Сити2','Сити3','Ман1','Ман2','Радуга','ТДЖ','Сити4','Вавилон','Искра','Магнит','Рынок7','Валентина'])
        self.entery_point.place(x = 200, y =80)
    
        self.entery_name = ttk.Combobox(self, values = ['Зарплата-База','Зарплата-%','Аренда'])
        self.entery_name.place(x = 200, y = 110)

        self.entery_money = ttk.Entry(self)
        self.entery_money.place(x = 200, y = 140)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 170)
        
        btn_add = tk.Button(self, text = 'Добавить',bg = 'white')
        btn_add.place(x = 220, y =170)
        btn_add.bind('<Button-1>', lambda event: self.insert(self.entery_year.get(),self.entery_month.get(),self.entery_point.get(),self.entery_name.get(),
                                                             self.entery_money.get()))
        
    def insert(self,year,month,point,name,money):
        data = pd.read_csv('d://Apps/Data/PointExpense.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,year,month,point,name,money]
        data.loc[len(data[text[0]])] = list
        data.to_csv ('d://Apps/Data/PointExpense.csv', encoding = 'utf-8',index=False)
        self.destroy()
        

class Child_edit(tk.Toplevel):
    
    def __init__(self,n, main):
        super().__init__()
        self.main = main
        self.n = n
        self.init_child()
        
        
    def init_child(self):
        self.title("Редактировтаь товар")
        self.geometry("400x250+550+150")
        self.resizable(False, False)
        self["bg"] = "white"
        self.grab_set()
        self.focus_set()
        

        input_list = self.main.chosen(self.n)

        label_point = tk.Label(self, text = 'Отдел:',bg = 'white')
        label_point.place(x = 50 , y =80)
        
        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =110)

        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =140)
        
        label_month = tk.Label(self, text = 'Месяц:',bg = 'white')
        label_month.place(x = 50 , y =50)

        label_year = tk.Label(self, text = 'Год:',bg = 'white')
        label_year.place(x = 50 , y =20)

        month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        self.entery_year = ttk.Entry(self)
        self.entery_year.insert(0, input_list[0])
        self.entery_year.place(x = 200, y = 20)

        self.entery_month = ttk.Combobox(self, values = month_list)
        self.entery_month.insert(0, input_list[1])
        self.entery_month.place(x = 200, y = 50)

        self.entery_point = ttk.Combobox(self, values = ['Сити1', 'Сити2','Сити3','Ман1','Ман2','Радуга','ТДЖ','Сити4','Вавилон','Искра','Магнит','Рынок7','Валентина'])
        self.entery_point.insert(0, input_list[2])
        self.entery_point.place(x = 200, y =80)
    
        self.entery_name = ttk.Combobox(self, values = ['Зарплата-База','Зарплата-%','Аренда'])
        self.entery_name.insert(0, input_list[3])
        self.entery_name.place(x = 200, y = 110)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.insert(0, input_list[4])
        self.entery_money.place(x = 200, y = 140)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 170)
        
        btn_edit = tk.Button(self, text = 'Редактировать',bg = 'white')
        btn_edit.place(x = 200, y =170)
        btn_edit.bind('<Button-1>', lambda event: self.edit(self.entery_year.get(),self.entery_month.get(),self.entery_point.get(),self.entery_name.get(),
                                                             self.entery_money.get()))
        
    def edit(self,year,month,point,name,money):
        data = pd.read_csv('d://Apps/Data/PointExpense.csv')
        list =[self.n,year,month,point,name,money]
        data.loc[self.n] = list
        data.to_csv ('d://Apps/Data/PointExpense.csv', encoding = 'utf-8',index=False)
        self.destroy()
        