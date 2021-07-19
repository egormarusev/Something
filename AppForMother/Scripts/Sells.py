import tkinter as tk
from tkinter import ttk
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import datetime
from PIL import ImageTk, Image
from datetime import  time, date

class MainSells(tk.Toplevel):
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
        
        
        self.tree = ttk.Treeview(self, columns = ('ID', 'Date','Point','Price'), height = 20, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Date', width = 110, anchor = tk.CENTER)
        self.tree.column('Point', width = 120, anchor = tk.CENTER)
        self.tree.column('Price', width = 115, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = '№')
        self.tree.heading('Date',text = 'Дата')
        self.tree.heading('Point',text = 'Отдел')
        self.tree.heading('Price',text = 'Сумма')
        
        data = pd.read_csv('d://Apps/Data/Sells.csv')
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
        df = pd.read_csv('d://Apps/Data/Sells.csv')
        list = []
        for selection_item in self.tree.selection():
            list.append(int(self.tree.set(selection_item, '#1')))
        df = df.drop(list)
        df.to_csv ('d://Apps/Data/Sells.csv', encoding = 'utf-8',index=False)
        self.update()
        
        
    def update(self):
        data = pd.read_csv('d://Apps/Data/Sells.csv')
        text = data.columns.values
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        
        data.set_index(np.arange(len(data.index))) 
        data["ID"] = (np.arange(len(data.index)))
        data.to_csv ('d://Apps/Data/Sells.csv', encoding = 'utf-8',index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
            
    def chosen(self,n):
        df = pd.read_csv('d://Apps/Data/Sells.csv')
        Date = df.loc[n]["Date"]
        Point = df.loc[n]["Point"]
        Sum = df.loc[n]["Price"]
        list = [Date,Point,Sum]
        return list

    
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        
        
    def init_child(self):
        self.title("Добавить доходы / расходы")
        self.geometry("400x180+550+150")
        self.resizable(False, False)
        self.grab_set()
        self["bg"] = "white"
        self.focus_set()
          
        label_point = tk.Label(self, text = 'Отдел:',bg = 'white')
        label_point.place(x = 50 , y =50)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =80)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =20)
        
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
        self.check_date.place(x = 100, y = 20)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, datetime.date.today())
        self.entery_date.config(state=tk.DISABLED)
        self.entery_date.place(x = 200, y = 20)
        
        self.entery_point = ttk.Combobox(self, values = ['Сити1', 'Сити2','Сити3','Ман1','Ман2','Радуга','ТДЖ','Сити4','Вавилон','Искра','Магнит','Рынок7','Валентина'])
        self.entery_point.place(x = 200, y =50)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.place(x = 200, y = 80)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 120)
        
        btn_add = tk.Button(self, text = 'Добавить',bg = 'white')
        btn_add.place(x = 220, y =120)
        btn_add.bind('<Button-1>', lambda event: self.insert(self.entery_date.get(),self.entery_point.get(),self.entery_money.get()))
        
    def insert(self,date,point,money):
        data = pd.read_csv('d://Apps/Data/Sells.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,date,point,money]
        data.loc[len(data[text[0]])] = list
        data.to_csv ('d://Apps/Data/Sells.csv', encoding = 'utf-8',index=False)
        self.destroy()
        

class Child_edit(tk.Toplevel):
    
    def __init__(self,n, main):
        super().__init__()
        self.main = main
        self.n = n
        self.init_child()
        
        
    def init_child(self):
        self.title("Редактировтаь товар")
        self.geometry("400x180+550+150")
        self["bg"] = "white"
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        

        input_list = self.main.chosen(self.n)
        
        label_point = tk.Label(self, text = 'Отдел:',bg = 'white')
        label_point.place(x = 50 , y =50)
        
        label_money = tk.Label(self, text = 'Сумма:',bg = 'white')
        label_money.place(x = 50 , y =80)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =20)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, input_list[0])
        self.entery_date.place(x = 200, y = 20)

        self.entery_point = ttk.Combobox(self, values = ['Сити1', 'Сити2','Сити3','Ман1','Ман2','Радуга','ТДЖ','Сити4','Вавилон','Искра','Магнит','Рынок7','Валентина'])
        self.entery_point.insert(0, input_list[1])
        self.entery_point.place(x = 200, y =50)
        
        self.entery_money = ttk.Entry(self)
        self.entery_money.insert(0, input_list[2])
        self.entery_money.place(x = 200, y = 80)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 120)
        
        btn_edit = tk.Button(self, text = 'Редактировать',bg = 'white')
        btn_edit.place(x = 200, y =120)
        btn_edit.bind('<Button-1>', lambda event: self.edit(self.entery_date.get(),self.entery_point.get(), self.entery_money.get()))
        
    def edit(self,date,point,money):
        data = pd.read_csv('d://Apps/Data/Sells.csv')
        list =[self.n,date,point,money]
        data.loc[self.n] = list
        data.to_csv ('d://Apps/Data/Sells.csv', encoding = 'utf-8',index=False)
        self.destroy()
        