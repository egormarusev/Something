"""
db_customers.py
Авторы: Шайкин Н.С., Марусев Е.А., Шайкин К.А.
Модуль содержит код для таблицы "Информация о заказчиках"
и кнопок взаимодействия.
"""

import os
import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd

os.chdir("d:/work/")


class MainCustomers(tk.Toplevel):
    """
    MainCustomers
    Автор: Марусев Е.А.
    Класс наследуется от виджета Toplevel из библиотеки tkinter
    Класс, открывающий дочернее окно главного меню, содержащие таблицу "Инофрмация о заказчиках".
    Также в дочернем окне находятся кнопки взаимодействия с таблицей:
    "Обновить","Удаление","Редактирование".При удалении строчки,
    соответствующая информация удаляется из таблицы "Информация о Заказачиках".
    """
    def __init__(self):
        """
        __init__
        Автор: Марусев Е.А.
        Конструктор класса MainCustomers.
        параметры - self
        """
        super().__init__()
        self.init_main()

    def init_main(self):
        """
        init_main
        Метод создает таблицу "Информация о заказачиках" и toolbar с кнопками
        для взаимодействия с ней.
        параметры - self
        """
        self.toolbar = tk.Frame(self, bg="white", bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open_edit = tk.Button(self.toolbar, text="Редактировать",
                                       command=self.open_edit, bg="white",
                                       bd=1, compound=tk.TOP)
        self.btn_open_edit.pack(side=tk.LEFT,  padx=5, pady=10)
        self.btn_open_dialog = tk.Button(self.toolbar, text="Обновить",
                                         command=self.update,
                                         bg="white", bd=1, compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)
        self.btn_open_dialog = tk.Button(self.toolbar, text="Удалить",
                                         command=self.delete, bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)
        self.tree = ttk.Treeview(self, columns=('ID', 'IET', 'ClientName',
                                                'Telephone', 'Passport',
                                                'Model'),
                                 height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("IET", width=110, anchor=tk.CENTER)
        self.tree.column('ClientName', width=110, anchor=tk.CENTER)
        self.tree.column('Telephone', width=200, anchor=tk.CENTER)
        self.tree.column('Passport', width=130, anchor=tk.CENTER)
        self.tree.column('Model', width=120, anchor=tk.CENTER)
        self.tree.heading('ID', text='№')
        self.tree.heading('IET', text='ИЕТ')
        self.tree.heading('ClientName', text='ФИО Заказчика')
        self.tree.heading('Telephone', text='Номер телефона заказчика')
        self.tree.heading('Passport', text='Паспортные данные')
        self.tree.heading('Model', text='Название модели')
        data = pd.read_csv('./data/db_customers.csv')
        text = data.columns.values
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))
        self.tree.pack()

    def open_edit(self):
        """
        open_edit
        Автор: Марусев Е.А.
        Функция открывает дочернее окно редактирования класса ChildEdit и проверяет
        условие выбора нужной строки.
        параметры - self
        """
        if self.tree.selection() != ():
            select_num = int(self.tree.set(self.tree.selection()[0])["ID"])
            ChildEdit(select_num, self)

    def delete(self):
        """
        delete
        Автор: Марусев Е.А.
        Метод удаляет выбранную строку из таблицы.
        параметры отсутствуют
        """
        data_frame = pd.read_csv('./data/db_customers.csv')
        db_goods = pd.read_csv('./data/db_goods.csv')
        del_list = []
        del_client_list = []
        for selection_item in self.tree.selection():
            del_list.append(int(self.tree.set(selection_item, "#1")))
            del_client_list.append(int(self.tree.set(selection_item, "#2")))
        data_frame = data_frame.drop(del_list)
        for selection_item in del_client_list:
            y_ort = db_goods.loc[db_goods["ИЕТ"] == selection_item]
            y_ort = y_ort.index[0]
            db_goods = db_goods.drop(y_ort)
        data_frame.to_csv('./data/db_customers.csv',
                          encoding='utf-8', index=False)
        db_goods.to_csv('./data/db_goods.csv', encoding='utf-8', index=False)
        self.update()

    def update(self):
        """
        update
        Автор: Марусев Е.А.
        Функция обновляеет таблицу после изменений.
        параметры - self.
        """
        data = pd.read_csv('./data/db_customers.csv')
        text = data.columns.values
        [self.tree.delete(i) for i in self.tree.get_children()]
        data.set_index(np.arange(len(data.index)))
        data["ID"] = (np.arange(len(data.index)))
        data.reset_index(drop=True)
        data.to_csv('./data/db_customers.csv', encoding='utf-8', index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

    def chosen(self, index):
        """
        chosen
        Автор: Марусев Е.А.
        Функция возвращает лежащие в строчке значения при ее выборе.
        (используется в ChildEdit при редактировании).
        параметры - index - номер выделенной строки
        """
        data_frame = pd.read_csv('./data/db_customers.csv')
        iet = data_frame.loc[index]["ИЕТ"]
        client = data_frame.loc[index]["ФИО Заказчика"]
        telephone = data_frame.loc[index]["Номер телефона заказчика"]
        passport = data_frame.loc[index]["Паспортные данные"]
        model = data_frame.loc[index]["Название модели"]
        fields_list = [iet, client, telephone, passport, model]
        return fields_list


class ChildEdit(tk.Toplevel):
    """
    ChildEdit
    Автор: Марусев Е.А.
    Класс наследуется от виджета Toplevel из библиотеки tkinter
    Класс, открывающий дочернее окно MainCustomers для редактирования выбранной
    строчки. Содержит поля ввода, в которых уже лежат предыдущие значния.
    """

    def __init__(self, number, main):
        """
        __init__
        Автор: Марусев Е.А.
        Конструктор класса ChildEdit.
        Параметры - number - номер выделенной строки для изменения
        main - родительское окно
        """
        super().__init__()
        self.main = main
        self.number = number
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Марусев Е.А.
        Метод, содержащий поля для редактирования полей и кнопки взаимодействия.
        параметры - self
        """
        self.title("Редактировтаь информацию о заказчике")
        self.geometry("400x340+500+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        input_list = self.main.chosen(self.number)
        old_client = input_list[1]
        old_iet = input_list[0]
        label_iet = tk.Label(self, text='ИЕТ:')
        label_iet.place(x=50, y=20)
        label_client = tk.Label(self, text='ФИО Заказчика:')
        label_client.place(x=50, y=50)
        label_telephone = tk.Label(self, text='Номер телефона:')
        label_telephone.place(x=50, y=80)
        label_passport = tk.Label(self, text='Паспортные данные:')
        label_passport.place(x=50, y=110)
        label_model = tk.Label(self, text='Название модели:')
        label_model.place(x=50, y=140)
        self.entery_iet = ttk.Entry(self)
        self.entery_iet.insert(0, input_list[0])
        self.entery_iet.place(x=200, y=20)
        self.entery_client = ttk.Entry(self)
        self.entery_client.insert(0, input_list[1])
        self.entery_client.place(x=200, y=50)
        self.entery_telephone = ttk.Entry(self)
        self.entery_telephone.insert(0, input_list[2])
        self.entery_telephone.place(x=200, y=80)
        self.entery_passport = ttk.Entry(self)
        self.entery_passport.insert(0, input_list[3])
        self.entery_passport.place(x=200, y=110)
        self.entery_model = ttk.Entry(self)
        self.entery_model.insert(0, input_list[4])
        self.entery_model.place(x=200, y=140)
        self.btn_cancel = ttk.Button(self, text='Закрыть',
                                     command=self.destroy)
        self.btn_cancel.place(x=300, y=280)
        self.btn_add = ttk.Button(self, text='Редактировать')
        self.btn_add.place(x=200, y=280)
        self.btn_add.bind('<Button-1>',
                          lambda event: self.edit(self.entery_iet.get(),
                                                  self.entery_client.get(),
                                                  self.entery_telephone.get(),
                                                  self.entery_passport.get(),
                                                  self.entery_model.get(),
                                                  old_client, old_iet))

    def edit(self, iet, client, telephone, passport,
             model, old_client, old_iet):
        """
        edit
        Автор: Марусев Е.А.
        Метод редактирует в базе измененные значения.
        """
        df = pd.read_csv('./data/db_customers.csv')
        db_goods = pd.read_csv('./data/db_goods.csv')
        if old_client != client:
            db_goods.loc[db_goods["ФИО Заказчика"] == old_client,
                         "ФИО Заказчика"] = client
            db_goods.to_csv('./data/db_goods.csv',
                            encoding='utf-8', index=False)
        if old_iet != iet:
            db_goods.loc[db_goods["ИЕТ"] == old_iet, "ИЕТ"] = iet
            db_goods.to_csv('./data/db_goods.csv',
                            encoding='utf-8', index=False)
        fields_list = [self.number, iet, client, telephone, passport, model]
        df.loc[self.number] = fields_list
        df.to_csv('./data/db_customers.csv', encoding='utf-8', index=False)
        self.destroy()
