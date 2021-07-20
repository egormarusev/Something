"""
Автор: Шайкин К.А.
Модуль содержит код для таблицы "Информация о заказчиках"
и кнопок взаимодействия.
"""
import os
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
os.chdir("d:/work/")


class MainGoods(tk.Toplevel):
    """
    MainProviders
    Автор: Шайкин К.А.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором формируется
    таблица "Товары"
    Класс необходим для работы с таблицей товаров.
    """
    def __init__(self):
        """
        __init__
        Автор: Шайкин К.А.
        конструктор класса __init__
        Параметры: self
        """
        super().__init__()
        self.init_main()

    def init_main(self):
        """
        init_main
        Автор: Шайкин К.А.
        Метод необходим для редактирования данных о товарах в таблице
        Параметры: self
        """
        self.toolbar = tk.Frame(self, bg="white", bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Обновить",
                                         command=self.update, bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_edit = tk.Button(self.toolbar, text="Редактировать",
                                  command=self.open_edit, bg="white", bd=1,
                                  compound=tk.TOP)
        self.btn_edit.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Удалить",
                                         command=self.delete, bg="white", bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.tree = ttk.Treeview(self, columns=(
            'ID', 'IET', 'Providers', 'Client', 'Name', 'Season', 'Type',
            'SubType', 'Price'), height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("IET", width=110, anchor=tk.CENTER)
        self.tree.column('Providers', width=110, anchor=tk.CENTER)
        self.tree.column('Client', width=110, anchor=tk.CENTER)
        self.tree.column('Name', width=120, anchor=tk.CENTER)
        self.tree.column('Season', width=150, anchor=tk.CENTER)
        self.tree.column('Type', width=120, anchor=tk.CENTER)
        self.tree.column('SubType', width=120, anchor=tk.CENTER)
        self.tree.column('Price', width=115, anchor=tk.CENTER)

        self.tree.heading('ID', text='№')
        self.tree.heading('IET', text='ИЕТ')
        self.tree.heading('Providers', text='Поставщик')
        self.tree.heading('Client', text='ФИО Заказчика')
        self.tree.heading('Name', text='Название модели')
        self.tree.heading('Season', text='Сезон')
        self.tree.heading('Type', text='Вид инвентаря')
        self.tree.heading('SubType', text='Подвид')
        self.tree.heading('Price', text='Цена')

        data = pd.read_csv('./data/db_goods.csv')
        text = data.columns.values

        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

        self.tree.pack()

    def open_edit(self):
        """
        open_edit
        Автор: Шайкин К.А.
        Метод осуществляет открытие нового окна для редактирования
        Параметры: self
        """
        if self.tree.selection() != ():
            num = int(self.tree.set(self.tree.selection()[0])["ID"])
            ChildEdit(num, self)

    def delete(self):
        """
        delete
        Автор: Шайкин К.А.
        Метод осуществляет удаление в таблице "Товары"
        Параметры: self
        """
        data_frame = pd.read_csv('./data/db_goods.csv')
        db_customers = pd.read_csv('./data/db_customers.csv')
        del_list = []
        del_iet_list = []
        for selection_item in self.tree.selection():
            del_list.append(int(self.tree.set(selection_item, "#1")))
            del_iet_list.append(int(self.tree.set(selection_item, "#2")))
        data_frame = data_frame.drop(del_list)
        for selection_item in del_iet_list:
            elem = db_customers.loc[db_customers["ИЕТ"] == selection_item]
            elem = elem.index[0]
            db_customers = db_customers.drop(elem)
        data_frame.to_csv('./data/db_goods.csv', encoding='utf-8', index=False)
        db_customers.to_csv('./data/db_customers.csv',
                            encoding='utf-8', index=False)
        self.update()

    def update(self):
        """
        update
        Автор: Шайкин К.А.
        Метод необходима для обнавления таблицы после редактирования
        Параметры: self
        """
        data = pd.read_csv('./data/db_goods.csv')
        text = data.columns.values

        [self.tree.delete(i) for i in self.tree.get_children()]

        data.set_index(np.arange(len(data.index)))
        data["ID"] = (np.arange(len(data.index)))
        data.reset_index(drop=True)
        data.to_csv('./data/db_goods.csv', encoding='utf-8', index=False)
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

    def chosen(self, num):
        """
        chosen
        Автор: Шайкин К.А.
        Метод возвращает лежащие в строчке значения при ее выборе.
        Параметры: self, num
        num - номер строки
        """
        data = pd.read_csv('./data/db_goods.csv')
        iet = data.loc[num]["ИЕТ"]
        provider = data.loc[num]["Поставщик"]
        client = data.loc[num]["ФИО Заказчика"]
        name = data.loc[num]["Название модели"]
        season = data.loc[num]["Сезон"]
        ftype = data.loc[num]["Вид инвентаря"]
        sub_type = data.loc[num]["Подвид"]
        price = data.loc[num]["Цена"]
        fields_list = [iet, provider, client, name,
                       season, ftype, sub_type, price]
        return fields_list


class ChildEdit(tk.Toplevel):
    """
    ChildEdit
    Автор: Шайкин К.А.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором редактируется
    таблица "Товары"
    Класс необходим для работы с таблицей товаров.
    """

    def __init__(self, number, main):
        """
        __init__
        Автор: Шайкин К.А.
        конструктор класса __init__
        Параметры: self, number, main
        """
        super().__init__()
        self.main = main
        self.number = number
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Шайкин К.А.
        Метод дает возможность редактирования товаров в таблице
        Параметры: self
        """
        self.title("Редактировтаь товар")
        self.geometry("400x340+500+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        input_list = self.main.chosen(self.number)
        old_client = input_list[2]
        old_iet = input_list[0]

        label_iet = tk.Label(self, text='ИЕТ:')
        label_iet.place(x=50, y=20)

        label_provider = tk.Label(self, text='Поставщик:')
        label_provider.place(x=50, y=50)

        label_client = tk.Label(self, text='ФИО Заказчика:')
        label_client.place(x=50, y=80)

        label_name = tk.Label(self, text='Название модели:')
        label_name.place(x=50, y=110)

        label_season = tk.Label(self, text='Сезон:')
        label_season.place(x=50, y=140)

        label_type = tk.Label(self, text='Вид инвентаря:')
        label_type.place(x=50, y=170)

        label_subtype = tk.Label(self, text='Подвид:')
        label_subtype.place(x=50, y=200)

        label_price = tk.Label(self, text='Цена:')
        label_price.place(x=50, y=230)

        self.entery_iet = ttk.Entry(self)
        self.entery_iet.insert(0, input_list[0])
        self.entery_iet.place(x=200, y=20)

        self.entery_provider = ttk.Entry(self)
        self.entery_provider.insert(0, input_list[1])
        self.entery_provider.place(x=200, y=50)

        self.entery_client = ttk.Entry(self)
        self.entery_client.insert(0, input_list[2])
        self.entery_client.place(x=200, y=80)

        self.entery_name = ttk.Entry(self)
        self.entery_name.insert(0, input_list[3])
        self.entery_name.place(x=200, y=110)

        winter_list = ['Лыжи', 'Сноуборд', 'Коньки']
        summer_list = ['Велосипед', 'Самокат', 'Ролики',
                       'Скейтборд', 'Гироскутер']

        ski_list = ['Горные', 'Обычные']
        snowboard_list = ['Directional', 'Twin', 'Directional-Twin']
        scates_list = ['Фигурные', 'Хокейные']
        bicycle_list = ['Элекстрический', 'Горный', 'Городской', 'Детский']
        csooter_list = ['Электрический', 'Обыкновенный']
        rollers_list = [' ']
        scateboard_list = ['Логборд', 'Пенниборд', 'Обычный']
        giroscooter_list = ['С рулем', 'Без руля']

        self.entery_type = ttk.Combobox(self, values=[' '])
        self.entery_type.insert(0, input_list[5])
        self.entery_type.place(x=200, y=170)

        self.entery_subtype = ttk.Combobox(self, values=[' '])
        self.entery_subtype.insert(0, input_list[6])
        self.entery_subtype.place(x=200, y=200)

        def change_subtype():
            """
            change_subtype
            Автор: Шайкин К.А.
            Функция позволяет выбрать подтип товара
            Параметры отсутствуют
            """
            if self.entery_type.get() == 'Лыжи':
                list1 = ski_list
            elif self.entery_type.get() == 'Сноуборд':
                list1 = snowboard_list
            elif self.entery_type.get() == 'Коньки':
                list1 = scates_list
            elif self.entery_type.get() == 'Велосипед':
                list1 = bicycle_list
            elif self.entery_type.get() == 'Самокат':
                list1 = csooter_list
            elif self.entery_type.get() == 'Ролики':
                list1 = rollers_list
            elif self.entery_type.get() == 'Скейтборд':
                list1 = scateboard_list
            elif self.entery_type.get() == 'Гироскутер':
                list1 = giroscooter_list

            self.entery_subtype = ttk.Combobox(self, values=list1)
            self.entery_subtype.place(x=200, y=200)

        def change_type():
            """
            change_type
            Автор: Шайкин К.А.
            Функция позволяет выбрать тип товара в зависимости от сезона товара
            Параметры отсутствуют
            """
            if self.entery_season.get() == 'Зима':
                season_list = winter_list
            elif self.entery_season.get() == 'Лето':
                season_list = summer_list
            self.entery_type = ttk.Combobox(self, values=season_list)
            self.entery_type.bind("<<ComboboxSelected>>", change_subtype)
            self.entery_type.place(x=200, y=170)

        self.entery_season = ttk.Combobox(self, values=['Зима', 'Лето'])
        self.entery_season.insert(0, input_list[4])
        self.entery_season.bind("<<ComboboxSelected>>", change_type)
        self.entery_season.place(x=200, y=140)

        self.entery_price = ttk.Entry(self)
        self.entery_price.insert(0, input_list[7])
        self.entery_price.place(x=200, y=230)

        self.btn_cancel = ttk.Button(self, text='Закрыть',
                                     command=self.destroy)
        self.btn_cancel.place(x=300, y=280)

        self.btn_add = ttk.Button(self, text='Редактировать')
        self.btn_add.place(x=200, y=280)
        self.btn_add.bind('<Button-1>',
                          lambda event: self.edit(self.entery_iet.get(),
                                                  self.entery_provider.get(),
                                                  self.entery_client.get(),
                                                  self.entery_name.get(),
                                                  self.entery_season.get(),
                                                  self.entery_type.get(),
                                                  self.entery_subtype.get(),
                                                  self.entery_price.get(),
                                                  old_client, old_iet))

    def edit(self, iet, provider, client, name, season, type1,
             subtype, price, old_client, old_iet):
        """
        edit
        Автор: Шайкин К.А.
        Метод позволяет внести изменения в таблицу.
        Параметры: self, iet, provider, client, name, season, type1,
             subtype, price, old_client, old_iet
        Вся информация о параметрах берется из предыдущих функций
        """
        data = pd.read_csv('./data/db_goods.csv')
        db_customers = pd.read_csv('./data/db_customers.csv')
        if old_client != client:
            db_customers.loc[db_customers["ФИО Заказчика"] == old_client,
                             "ФИО Заказчика"] = client
            db_customers.to_csv('./data/db_customers.csv',
                                encoding='utf-8', index=False)
        if old_iet != iet:
            db_customers.loc[db_customers["ИЕТ"] == old_iet, "ИЕТ"] = iet
            db_customers.to_csv('./data/db_customers.csv',
                                encoding='utf-8', index=False)

        fields_list = [self.number, iet, provider, client, name, season,
                       type1, subtype, price]
        data.loc[self.number] = fields_list
        data.to_csv('./data/db_goods.csv', encoding='utf-8', index=False)
        self.destroy()
