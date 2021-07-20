"""
db_providers.py
Автор: Шайкин Н.С.
Модуль содержит код для таблицы "Информация о поставщиках"
и кнопок взаимодействия.
"""
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
os.chdir("d:/work/")


class MainProviders(tk.Toplevel):
    """
    MainProviders
    Автор: Шайкин Н.С.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором формируется
    таблица "Данные о поставщиках"
    Класс необходим для работы с таблицей поставщиков.
    """
    def __init__(self):
        """
        __init__
        Автор: Шайкин Н.С.
        конструктор класса MainProviders
        Параметры: self
        """
        super().__init__()
        self.init_main()

    def init_main(self):
        """
        init_main
        Автор: Шайкин Н.С.
        Метод осуществляет доспуп к таблице "Данные о поставщиках"
        Параметры: self
        """
        self.toolbar = tk.Frame(self, bg="white", bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open_dialog = tk.Button(self.toolbar,
                                         text="Добавить позицию",
                                         command=self.open_dialog, bg="white",
                                         bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Обновить",
                                         command=self.update, bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Редактировать",
                                         command=self.open_edit,
                                         bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Удалить",
                                         command=self.delete, bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'Providers', 'Phone', 'Country'),
                                 height=15, show='headings')

        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("Providers", width=110, anchor=tk.CENTER)
        self.tree.column('Phone', width=200, anchor=tk.CENTER)
        self.tree.column('Country', width=130, anchor=tk.CENTER)

        self.tree.heading('ID', text='№')
        self.tree.heading('Providers', text='Поставщик')
        self.tree.heading('Phone', text='Номер телефона поставщика')
        self.tree.heading('Country', text="Страна поставщика")

        data = pd.read_csv('./data/db_providers.csv')
        text = data.columns.values

        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

        self.tree.pack()

    def open_dialog(self):
        """
        open_dialog
        Автор: Шайкин Н.С.
        Метод осуществляет открытие нового окна
        Параметры: self
        """
        Child()

    def open_edit(self):
        """
        open_edit
        Автор: Шайкин Н.С.
        Метод осуществляет открытие нового окна для редактирования
        Параметры: self
        """
        if self.tree.selection() != ():
            num = int(self.tree.set(self.tree.selection()[0])["ID"])
            ChildEdit(num, self)

    def delete(self):
        """
        delete
        Автор: Шайкин Н.С.
        Метод осуществляет удаление в таблице "Данные о поставщиках"
        Параметры: self
        """
        data = pd.read_csv('./data/db_providers.csv')
        del_list = []
        for selection_item in self.tree.selection():
            del_list.append(int(self.tree.set(selection_item, "#1")))
        data = data.drop(del_list)
        data.to_csv('./data/db_providers.csv', encoding='utf-8', index=False)
        self.update()

    def update(self):
        """
        update
        Автор: Шайкин Н.С.
        Метод обнавляет таблицу после редактирования
        Параметры: self
        """
        data = pd.read_csv('./data/db_providers.csv')
        text = data.columns.values

        [self.tree.delete(i) for i in self.tree.get_children()]

        data.set_index(np.arange(len(data.index)))
        data["ID"] = (np.arange(len(data.index)))
        data.reset_index(drop=True)
        data.to_csv('./data/db_providers.csv', encoding='utf-8', index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

    def chosen(self, num):
        """
        chosen
        Автор: Шайкин Н.С.
        Метод возвращает лежащие в строчке значения при ее выборе.
        Параметры: self, num
        num - номер строки
        """
        data = pd.read_csv('./data/db_providers.csv')
        provider = data.loc[num]["Поставщик"]
        phone = data.loc[num]["Номер телефона поставщика"]
        country = data.loc[num]["Страна поставщика"]
        field_list = [provider, phone, country]
        return field_list


class Child(tk.Toplevel):
    """
    Child
    Автор: Шайкин Н.С.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором можно добавить нового поставщика
    в таблицу
    Класс необходим для добавления нового поставщика
    """
    def __init__(self):
        """
        __init__
        Автор: Шайкин Н.С.
        Конструктор класса Child
        Параметры: self
        """
        super().__init__()
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Шайкин Н.С.
        Метод необходим для добавления нового поставщика в таблицу.
        Параметры: self
        """
        self.title("Добавить Поставщика")
        self.geometry("400x340+500+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_provider = tk.Label(self, text='Поставщик:')
        label_provider.place(x=50, y=20)

        label_phone = tk.Label(self, text='Номер телефона поставщика:')
        label_phone.place(x=50, y=80)

        label_country = tk.Label(self, text='Страна поставщика:')
        label_country.place(x=50, y=50)

        self.entery_provider = ttk.Entry(self)
        self.entery_provider.place(x=240, y=20)

        self.entery_phone = ttk.Entry(self)
        self.entery_phone.place(x=240, y=80)

        self.entery_country = ttk.Entry(self)
        self.entery_country.place(x=240, y=50)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=280, y=280)

        btn_add = ttk.Button(self, text='Добавить')
        btn_add.place(x=200, y=280)
        btn_add.bind('<Button-1>',
                     lambda event: self.insert(self.entery_provider.get(),
                                               self.entery_phone.get(),
                                               self.entery_country.get()))

    def insert(self, provider, phone, country):
        """
        insert
        Автор: Шайкин Н.С.
        Метод необходима для вставки новых данных в таблицу
        Параметры: self, provider, phone, country
        Вся информация параметров берется из предыдущих функций
        """
        data = pd.read_csv('./data/db_providers.csv')
        text = data.columns.values
        field_list = [len(data[text[0]]) + 1, provider, phone, country]
        data.loc[len(data[text[0]])] = field_list
        data.to_csv('./data/db_providers.csv', encoding='utf-8', index=False)
        self.destroy()


class ChildEdit(tk.Toplevel):
    """
    ChildEdit
    Автор: Шайкин Н.С.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором можно редактировать выбранного
    поставщика в таблице
    Класс необходим для добавления нового поставщика
    """

    def __init__(self, num, main):
        """
        __init__
        Автор: Шайкин Н.С.
        Конструктор класса ChildEdit
        Параметры: self, num, main
        num - номер строки

        """
        super().__init__()
        self.main = main
        self.num = num
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Шайкин Н.С.
        Метод необходим для редактирования данных о поставщике в таблице
        Параметры: self
        """
        self.title("Редактировтаь информацию о поставщике")
        self.geometry("430x340+500+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        input_list = self.main.chosen(self.num)

        label_provider = tk.Label(self, text='Поставщик:')
        label_provider.place(x=50, y=20)

        label_phone = tk.Label(self, text='Номер телефона поставщика:')
        label_phone.place(x=50, y=50)

        label_country = tk.Label(self, text='Страна:')
        label_country.place(x=50, y=80)

        self.entery_provider = ttk.Entry(self)
        self.entery_provider.insert(0, input_list[0])
        self.entery_provider.place(x=240, y=20)

        self.entery_phone = ttk.Entry(self)
        self.entery_phone.insert(0, input_list[1])
        self.entery_phone.place(x=240, y=50)

        self.entery_country = ttk.Entry(self)
        self.entery_country.insert(0, input_list[2])
        self.entery_country.place(x=240, y=80)

        self.btn_cancel = ttk.Button(self, text='Закрыть',
                                     command=self.destroy)
        self.btn_cancel.place(x=300, y=280)

        self.btn_add = ttk.Button(self, text='Редактировать')
        self.btn_add.place(x=200, y=280)
        self.btn_add.bind('<Button-1>',
                          lambda event: self.edit(self.entery_provider.get(),
                                                  self.entery_phone.get(),
                                                  self.entery_country.get()))

    def edit(self, provider, phone, country):
        """
        edit
        Автор: Шайкин Н.С.
        Метод редактирует соответствующую строку в базе данных
        Параметры: self, provider, phone, country
        Вся информация параметров берется из предыдущих функций
        """
        data = pd.read_csv('./data/db_providers.csv')
        field_list = [self.num, provider, phone, country]
        data.loc[self.num] = field_list
        data.to_csv('./data/db_providers.csv', encoding='utf-8', index=False)
        self.destroy()

    def insert(self, iet, client, telephone, passport, model):
        """
        insert
        Автор: Шайкин Н.С.
        Метод вставляет соответствующую строку в базе данных
        Параметры: self, iet, client, telephone, passport, model
        Вся информация параметров берется из предыдущих функций
        """
        data = pd.read_csv('./data/db_providers.csv')
        text = data.columns.values
        field_list = [len(data[text[0]]) + 1, iet, client, telephone,
                      passport, model]
        data.loc[len(data[text[0]])] = field_list
        data.to_csv('./data/db_providers.csv', encoding='utf-8', index=False)
        self.destroy()
