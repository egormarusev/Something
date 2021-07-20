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
        
        self.tree = ttk.Treeview(self, columns = ('ID', 'Date','Author','Name'), height = 15, show = 'headings')
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        
        self.tree.column("ID", width = 30, anchor = tk.CENTER)
        self.tree.column('Date', width = 130, anchor = tk.CENTER)
        self.tree.column('Author', width = 150, anchor = tk.CENTER)
        self.tree.column('Name', width = 200, anchor = tk.CENTER)
        
        self.tree.heading('ID',text = 'ID')
        self.tree.heading('Date',text = 'Дата')
        self.tree.heading('Author',text = 'Автор')
        self.tree.heading('Name',text = 'Название')

        data = pd.read_csv('DataBase.csv')
        #data['Sum'] = np.round(data['Sum'], 2)
        text = data.columns.values
            
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i], values=list(map(lambda x: data[x][i], text[0:])))
        
        self.tree.pack()
        
    def open_dialog(self):
        Child()      
        
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
        Name = df.loc[n]["Name"]
        Author = df.loc[n]["Author"]
        list = [Date,Author,Name]
        return list

    
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        
        
    def init_child(self):
        self.title("Добавить доходы / расходы")
        self.geometry("400x180+430+180")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self["bg"] = "white"
        
        label_name = tk.Label(self, text = 'Название:',bg = 'white')
        label_name.place(x = 50 , y =60)
        
        label_author = tk.Label(self, text = 'Автор:',bg = 'white')
        label_author.place(x = 50 , y =20)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =100)
        
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
        self.check_date.place(x = 100, y = 100)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, datetime.date.today())
        self.entery_date.config(state=tk.DISABLED)
        self.entery_date.place(x = 200, y = 100)

        self.entery_name = ttk.Entry(self)
        self.entery_name.place(x = 200, y = 60)
        
        self.entery_author = ttk.Entry(self)
        self.entery_author.place(x = 200, y =20)

        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy)
        btn_cancel['bg'] = 'white'
        btn_cancel.place(x = 300, y= 140)
        
        btn_add = tk.Button(self, text = 'Добавить')
        btn_add['bg'] = 'white'
        btn_add.place(x = 220, y =140)
        btn_add.bind('<Button-1>', lambda event: self.insert(self.entery_date.get(),self.entery_name.get(),
                                                            self.entery_author.get()))
        
        
    def insert(self,date,name,author):
        data = pd.read_csv('DataBase.csv')
        text = data.columns.values
        list =[len(data[text[0]])+1,date,author,name]
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
        label_name.place(x = 50 , y =60)
        
        label_author = tk.Label(self, text = 'Автор:',bg = 'white')
        label_author.place(x = 50 , y =20)
        
        label_date = tk.Label(self, text = 'Дата:',bg = 'white')
        label_date.place(x = 50 , y =100)
        
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
        self.check_date.place(x = 100, y = 100)
        
        self.entery_date = ttk.Entry(self)
        self.entery_date.insert(0, input_list[0])
        self.entery_date.config(state=tk.DISABLED)
        self.entery_date.place(x = 200, y = 100)

        self.entery_author = ttk.Entry(self)
        self.entery_author.insert(0, input_list[1])
        self.entery_author.place(x = 200, y = 20)

        self.entery_name = ttk.Entry(self)
        self.entery_name.insert(0, input_list[2])
        self.entery_name.place(x = 200, y = 60)
        
        btn_cancel = tk.Button(self,text = 'Закрыть', command = self.destroy,bg = 'white')
        btn_cancel.place(x = 300, y= 150)
        
        btn_edit = tk.Button(self, text = 'Редактировать',bg = 'white')
        btn_edit.place(x = 200, y =150)
        btn_edit.bind('<Button-1>', lambda event: self.edit(self.entery_date.get(),self.entery_name.get(),self.entery_author.get()))
        
    def edit(self,date, name, author):
        data = pd.read_csv('DataBase.csv')
        #text = data.columns.values
        list =[self.n,date,author,name]
        data.loc[self.n] = list
        data.to_csv ('DataBase.csv', encoding = 'utf-8',index=False)
        self.destroy()
        
    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Книги")
    root.geometry("530x420+430+180")
    root.resizable(False, False)
    root.mainloop()