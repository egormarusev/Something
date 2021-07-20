"""
    db_full_list.py
    Авторы: Шайкин К.А., Марусев Е.А.
    Модуль содержит код для таблицы "Полный список" и кнопок взаиодействия с ней.
"""
import os
import tkinter as tk
from tkinter import ttk
import pandas as pd

os.chdir("d:/work/")


class MainFull(tk.Toplevel):
    """
    MainFull
    Автор: Шайкин К.А.
    Класс наследуется от виджета Toplevel из библиотеки tkinter
    Класс, создающий дочернее окно главного с таблицей "Полный список" и кнопку
    'Фильрация' для фильрации полного списка.
    """
    def __init__(self):
        """
        __init__
        Автор: Шайкин К.А.
        Конструктор класса MainFull.
        Параметры - self.
        """
        super().__init__()
        self.init_main()

    def init_main(self):
        """
        init_main
        Автор: Шайкин К.А.
        Метод, создающая таблицу "Полный список" и тулбар с кнопкой
        взаимодействия с ней. В этой функции создается таблица
        полного списка посредством соединения остальных таблиц.
        Параметры - self.
        """
        self.toolbar = tk.Frame(self, bg="white", bd=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_open_dialog = tk.Button(self.toolbar, text="Фильтрация",
                                         command=self.open_dialog, bg="white",
                                         bd=1,
                                         compound=tk.TOP)
        self.btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=10)

        self.tree = ttk.Treeview(self, columns=(
            "IET", "Providers", "Phone", "Country", "FIO",
            "Telephone", "Passport", "Model", "Season", "Type",
            "Subtype", "Price"), height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.tree.column("IET", width=50, anchor=tk.CENTER)
        self.tree.column('Providers', width=110, anchor=tk.CENTER)
        self.tree.column('Phone', width=200, anchor=tk.CENTER)
        self.tree.column('Country', width=120, anchor=tk.CENTER)
        self.tree.column('FIO', width=110, anchor=tk.CENTER)
        self.tree.column('Telephone', width=200, anchor=tk.CENTER)
        self.tree.column('Passport', width=130, anchor=tk.CENTER)
        self.tree.column('Model', width=120, anchor=tk.CENTER)
        self.tree.column('Season', width=50, anchor=tk.CENTER)
        self.tree.column('Type', width=120, anchor=tk.CENTER)
        self.tree.column('Subtype', width=120, anchor=tk.CENTER)
        self.tree.column('Price', width=115, anchor=tk.CENTER)

        self.tree.heading('IET', text='ИЕТ')
        self.tree.heading('Providers', text='Поставщик')
        self.tree.heading('Phone', text='Номер телефона поставщика')
        self.tree.heading('Country', text='Страна поставщика')
        self.tree.heading('FIO', text='ФИО Заказчика')
        self.tree.heading('Telephone', text='Номер телефона заказчика')
        self.tree.heading('Passport', text='Паспортные данные')
        self.tree.heading('Model', text='Название модели')
        self.tree.heading('Season', text='Сезон')
        self.tree.heading('Type', text='Вид инвентаря')
        self.tree.heading('Subtype', text='Подвид')
        self.tree.heading('Price', text='Цена')

        def denorm(db_1, db_2, key):
            """
            denorm
            Автор: Марусев Е.А.
            Функция осуществляет соединение двух таблиц по ключу.
            Параметры - db1, db2 - pandas dataframes, key - ключ слияния
            """
            from pandas import merge
            return merge(db_1, db_2, on=key)

        dfgoods = pd.read_csv('./data/db_goods.csv')
        dfgoods = dfgoods.drop(['ID'], axis=1)
        dfgoods = dfgoods.drop(['ФИО Заказчика'], axis=1)
        dfprovider = pd.read_csv('./data/db_providers.csv')
        dfprovider = dfprovider.drop(['ID'], axis=1)
        dfclient = pd.read_csv('./data/db_customers.csv')
        dfclient = dfclient.drop(['ID'], axis=1)
        dfclient = dfclient.drop(['Название модели'], axis=1)
        k = denorm(dfprovider, dfgoods, "Поставщик")
        k = denorm(k, dfclient, 'ИЕТ')
        column = k.columns.tolist()
        new_df = [column[3]]+column[0:3]+column[4:]
        new_columns = new_df[0:4]+new_df[-3:]+new_df[4:9]
        full_list = k[new_columns]
        full_list.to_csv('d://work/data/db_full_list.csv',
                         encoding='utf-8', index=False)
        text = full_list.columns.values
        for i in range(len(full_list[text[0]])):
            self.tree.insert('', 'end', text=full_list[text[0]][i],
                             values=list(map(lambda x: full_list[x][i],
                                             text[0:])))
        self.tree.pack()

    def open_dialog(self):
        """
        open_dialog
        Автор: Шайкин К.А.
        Метод запускает класс Child, который открывет дочернее окно
        Фильтрации.
        параметры - self
        """
        Child()


class Child(tk.Toplevel):
    """
    Child
    Автор: Марусев Е.А.
    Класс наследуется от виджета Toplevel из библиотеки tkinter
    Класс, содержащий поля для фильтраци таблицы "Полный список" и кнопку
    для выполнения ее.
    """
    def __init__(self):
        """
        __init__
        Автор: Марусев Е.А.
        Конструктор класса Child
        параметры - self
        """
        super().__init__()
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Марусев Е.А.
        Метод, создающий окно с полями для фильтрации. Поля формата
        'Полный список'
        """
        self.title("Фильтрация")
        self.geometry("400x600+500+0")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_iet = tk.Label(self, text='ИЕТ:')
        label_iet.place(x=50, y=20)

        label_provider = tk.Label(self, text='Поставщик:')
        label_provider.place(x=50, y=50)

        label_phone = tk.Label(self, text='Номер телефона поставщика:')
        label_phone.place(x=50, y=80)

        label_country = tk.Label(self, text='Страна Поставщика:')
        label_country.place(x=50, y=110)

        label_client = tk.Label(self, text='ФИО Заказчика:')
        label_client.place(x=50, y=140)

        label_telephone = tk.Label(self, text='Номер телефона заказчика:')
        label_telephone.place(x=50, y=170)

        label_passport = tk.Label(self, text='Паспортные данные:')
        label_passport.place(x=50, y=200)

        label_model = tk.Label(self, text='Название модели:')
        label_model.place(x=50, y=230)

        label_season = tk.Label(self, text='Сезон:')
        label_season.place(x=50, y=260)

        label_type = tk.Label(self, text='Вид инвентаря:')
        label_type.place(x=50, y=290)

        label_subtype = tk.Label(self, text='Подвид:')
        label_subtype.place(x=50, y=320)

        label_price = tk.Label(self, text='Цена:')
        label_price.place(x=50, y=350)

        self.entery_iet = ttk.Entry(self)
        self.entery_iet.place(x=250, y=20)

        self.entery_phone = ttk.Entry(self)
        self.entery_phone.place(x=250, y=80)

        self.entery_country = ttk.Entry(self)
        self.entery_country.place(x=250, y=110)

        def change_phone_country():
            """
            change_phone_country
            Автор: Марусев Е.А.
            Заполняет поля 'телефон поставщика' и 'страна постащика' автоматически
            после выора постащика
            """
            temp_provider = self.entery_provider.get()
            db_providers = pd.read_csv('./data/db_providers.csv')
            prov_index = db_providers.loc
            [db_providers['Поставщик'] == temp_provider]
            prov_index = prov_index.index[0]
            temp_provider_phone = db_providers.loc[prov_index]
            ["Номер телефонапоставщика"]
            self.entery_phone = ttk.Entry(self)
            self.entery_phone.place(x=250, y=80)
            self.entery_phone.insert(0, temp_provider_phone)
            self.entery_phone.config(state=tk.DISABLED)

            temp_provider_country = db_providers.loc[prov_index]["Страна поставщика"]
            self.entery_country = ttk.Entry(self)
            self.entery_country.place(x=250, y=110)
            self.entery_country.insert(0, temp_provider_country)
            self.entery_country.config(state=tk.DISABLED)

        db_providers = pd.read_csv('./data/db_providers.csv')
        prov_list = db_providers["Поставщик"].values.tolist()
        self.entery_provider = ttk.Combobox(self, values=prov_list)
        self.entery_provider.bind("<<ComboboxSelected>>", change_phone_country)
        self.entery_provider.place(x=250, y=50)

        winter_list = [u'Лыжи', 'Сноуборд', u'Коньки']
        summer_list = [u'Велосипед', u'Самокат', u'Ролики',
                       u'Скейтборд', u'Гироскутер']

        ski_list = [u'Горные', u'Обычные']
        snowboard_list = [u'Directional', u'Twin', u'Directional-Twin']
        scates_list = [u'Фигурные', u'Хокейные']
        bicycle_list = [u'Элекстрический', u'Горный', u'Городской', u'Детский']
        csooter_list = [u'Электрический', u'Обыкновенный']
        rollers_list = [u' ']
        scateboard_list = [u'Логборд', u'Пенниборд', u'Обычный']
        giroscooter_list = [u'С рулем', u'Без руля']

        self.entery_client = ttk.Entry(self)
        self.entery_client.place(x=250, y=140)

        self.entery_telephone = ttk.Entry(self)
        self.entery_telephone.place(x=250, y=170)

        self.entery_type = ttk.Combobox(self, values=[' '])
        self.entery_type.place(x=250, y=290)

        self.entery_subtype = ttk.Combobox(self, values=[' '])
        self.entery_subtype.place(x=250, y=320)

        def change_subtype():
            """
            change_subtype
            Автор: Марусев Е.А.
            Менят список выбора подтипа товара после выбора типа.
            параметры отсутствуют
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
            self.entery_subtype.place(x=250, y=320)

        self.entery_passport = ttk.Entry(self)
        self.entery_passport.place(x=250, y=200)

        self.entery_model = ttk.Entry(self)
        self.entery_model.place(x=250, y=230)

        def change_type():
            """
            change_type
            Автор: Марусев Е.А.
            Меняет список типов после выбора сезона.
            параметры - нет
            """
            if self.entery_season.get() == 'Зима':
                season_list = winter_list
            elif self.entery_season.get() == 'Лето':
                season_list = summer_list
            self.entery_type = ttk.Combobox(self, values=season_list)
            self.entery_type.bind("<<ComboboxSelected>>", change_subtype)
            self.entery_type.place(x=250, y=170)

        self.entery_season = ttk.Combobox(self, values=[u'Зима', u'Лето'])
        self.entery_season.bind("<<ComboboxSelected>>", change_type)
        self.entery_season.place(x=250, y=260)

        self.entery_price = ttk.Entry(self)
        self.entery_price.place(x=250, y=350)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=150, y=400)

        btn_add = ttk.Button(self, text='Фильтровать')
        btn_add.place(x=50, y=400)
        btn_add.bind('<Button-1>',
                     lambda event: self.filter(self.entery_iet.get(),
                                               self.entery_provider.get(),
                                               self.entery_phone.get(),
                                               self.entery_country.get(),
                                               self.entery_client.get(),
                                               self.entery_telephone.get(),
                                               self.entery_passport.get(),
                                               self.entery_model.get(),
                                               self.entery_season.get(),
                                               self.entery_type.get(),
                                               self.entery_subtype.get(),
                                               self.entery_price.get()))

    def filter(self, iet, provider, phone, country, client,
               telephone, passport, model, season, itype, subtype, price):
        """
        filter
        Автор: Шайкин К.А.
        метод осуществляет фильтрацию таблицы на основе введенных данных.
        """
        full_list = pd.read_csv('./data/db_full_list.csv')
        f_dict = {}
        headers = ["ИЕТ", "Поставщик", "Номер телефона поставщика",
                   "Страна поставщика", "ФИО заказчика",
                   "Номер телефона заказчика", "Паспортные данные",
                   "Название модели", "Сезон", "Вид", "Подвид", "Цена"]
        s_list = [iet, provider, phone, country, client,
                  telephone, passport, model, season, itype, subtype, price]
        k = -1
        for i in s_list:
            k += 1
            f_dict[headers[k]] = i
        for i in f_dict:
            if f_dict[i] != '':
                full_list = full_list[lambda full_list: (full_list[i] == f_dict[i])]

        filtered_list = full_list
        filtered_list.to_csv('./data/db_filtered_list.csv',
                             encoding='utf-8', index=False)
        FilteredChild()


class FilteredChild(tk.Toplevel):
    """
    FilteredChild
    Автор: Шайкин К.А.
    Класс, создающий дочернее окно Child с отфильтрованной таблицей.
    Класс наследуется от виджета Toplevel библиотеки Tkinter.
    """
    def __init__(self):
        """
        Автор: Шайкин К.А.
        Конструктор класса FilteredChild.
        """
        super().__init__()
        self.init_child()

    def init_child(self):
        """
        init_child
        Автор: Шайкин К.А.
        Функция создает дочернее окно с отфильтрованной таблицей.
        """
        self.title("Отфильтрованная база данных")
        self.geometry("+50+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        self.tree = ttk.Treeview(self, columns=(
            'IET', 'Providers', 'Phone', "Country", "FIO", "Telephone",
            'Passport', "Model", "Season", "Type", "Subtype", "Price"),
                                 height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.tree.column("IET", width=70, anchor=tk.CENTER)
        self.tree.column('Providers', width=110, anchor=tk.CENTER)
        self.tree.column('Phone', width=200, anchor=tk.CENTER)
        self.tree.column('Country', width=120, anchor=tk.CENTER)
        self.tree.column('FIO', width=110, anchor=tk.CENTER)
        self.tree.column('Telephone', width=200, anchor=tk.CENTER)
        self.tree.column('Passport', width=130, anchor=tk.CENTER)
        self.tree.column('Model', width=120, anchor=tk.CENTER)
        self.tree.column('Season', width=110, anchor=tk.CENTER)
        self.tree.column('Type', width=120, anchor=tk.CENTER)
        self.tree.column('Subtype', width=70, anchor=tk.CENTER)
        self.tree.column('Price', width=70, anchor=tk.CENTER)

        self.tree.heading('IET', text='ИЕТ')
        self.tree.heading('Providers', text='Поставщик')
        self.tree.heading('Phone', text='Номер телефона поставщика')
        self.tree.heading('Country', text='Страна поставщика')
        self.tree.heading('FIO', text='ФИО Заказчика')
        self.tree.heading('Telephone', text='Номер телефона заказчика')
        self.tree.heading('Passport', text='Паспортные данные')
        self.tree.heading('Model', text='Название модели')
        self.tree.heading('Season', text='Сезон')
        self.tree.heading('Type', text='Вид инвентаря')
        self.tree.heading('Subtype', text='Подвид')
        self.tree.heading('Price', text='Цена')

        data = pd.read_csv('./data/db_filtered_list.csv')
        text = data.columns.values
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))

        self.tree.pack()

        os.remove(os.path.join('./data/db_filtered_list.csv'))
        os.remove(os.path.join('./data/db_full_list.csv'))
