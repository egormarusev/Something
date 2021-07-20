"""
    Авторы: Марусев Е.А., Шайкин Н.С., Шайкин К.А.
    Модуль содержит код для загрузки товара в базу посредством заполнения полей
    формата "Полный список".
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
os.chdir("d:/work/")


class DownlMain(tk.Toplevel):
    """
    DownlMain
    Класс, создащюий дочернее окно главного меню с полями для ввода информации
    о новом товаре, заказчике и потсавщике.
    Класс наследуется от виджета Toplevel библиотеки Tkinter.
    Автор: Марусев Е.А.
    """
    def __init__(self, btn):
        """
        __init__
        Конструктор класса DownlMain
        Автор: Марусев Е.А.
        """
        super().__init__()
        self.init_main()
        self.btn = btn

    def init_main(self):
        """
        init_main
        Метод, создающий дочернее окно с полями для ввода информации и кнопки
        взаимодейтсвия с ними.
        Параметр - self
        Автор: Марусев Е.А.
        """
        self.title("Загрузить товар")
        self.geometry("+500+200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_iet = tk.Label(self, text='ИЕТ:')
        label_iet.place(x=50, y=20)

        label_provider = tk.Label(self, text='Поставщик:')
        label_provider.place(x=50, y=50)

        label_phone = tk.Label(self, text='Номер телефона поставщика:')
        label_phone.place(x=50, y=80)

        label_country = tk.Label(self, text='Страна:')
        label_country.place(x=50, y=110)

        label_client = tk.Label(self, text='ФИО заказчика:')
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
        self.entery_iet.place(x=300, y=20)

        self.entery_phone = ttk.Entry(self)
        self.entery_phone.place(x=300, y=80)

        self.entery_country = ttk.Entry(self)
        self.entery_country.place(x=300, y=110)

        def change_phone_country(event):
            """
            change_phone_country
            Функция заполняет автоматически страну и телефон поставщика после
            выбора поставщика.
            Параметры - event
            Автор:  Шайкин К.А.
            """
            t_pr = self.entery_provider.get()
            db_providers = pd.read_csv('./data/db_providers.csv')
            prov_index = db_providers.loc[db_providers['Поставщик'] == t_pr]
            prov_index = prov_index.index[0]
            temp_provider_phone = db_providers.loc[prov_index]["Номер телефона поставщика"]
            self.entery_phone = ttk.Entry(self)
            self.entery_phone.place(x=300, y=80)
            self.entery_phone.insert(0, temp_provider_phone)
            self.entery_phone.config(state=tk.DISABLED)

            t_pr_country = db_providers.loc[prov_index]["Страна поставщика"]
            self.entery_country = ttk.Entry(self)
            self.entery_country.place(x=300, y=110)
            self.entery_country.insert(0, t_pr_country)
            self.entery_country.config(state=tk.DISABLED)

        db_providers = pd.read_csv('./data/db_providers.csv')
        prov_list = db_providers["Поставщик"].values.tolist()
        self.entery_provider = ttk.Combobox(self, values=prov_list)
        self.entery_provider.bind("<<ComboboxSelected>>", change_phone_country)
        self.entery_provider.place(x=300, y=50)

        self.entery_client = ttk.Entry(self)
        self.entery_client.place(x=300, y=140)

        self.entery_tel = ttk.Entry(self)
        self.entery_tel.place(x=300, y=170)

        self.entery_passport = ttk.Entry(self)
        self.entery_passport.place(x=300, y=200)

        self.entery_model = ttk.Entry(self)
        self.entery_model.place(x=300, y=230)

        winter_list = ['Лыжи', 'Сноуборд', 'Коньки']
        summer_list = ['Велосипед', 'Самокат', 'Ролики', 'Скейтборд',
                       'Гироскутер']

        ski_list = ['Горные', 'Обычные']
        snowboard_list = ['Directional', 'Twin', 'Directional-Twin']
        scates_list = ['Фигурные', 'Хокейные']
        bicycle_list = ['Элекстрический', 'Горный', 'Городской', 'Детский']
        csooter_list = ['Электрический', 'Обыкновенный']
        rollers_list = [' ']
        scateboard_list = ['Логборд', 'Пенниборд', 'Обычный']
        giroscooter_list = ['С рулем', 'Без руля']

        self.entery_type = ttk.Combobox(self, values=[' '])
        self.entery_type.place(x=300, y=290)

        self.entery_subtype = ttk.Combobox(self, values=[' '])
        self.entery_subtype.place(x=300, y=320)

        def change_subtype(event):
            """
            change_subtype
            Функция изменяет список подтипов товара после выбора типа товара.
            Параметры - event
            Автор: Шайкин Н.С.
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
            self.entery_subtype.place(x=300, y=320)

        def change_type(event):
            """
            change_type
            Функция изменяет список типов товара после выбора сезона.
            Параметры - event
            Автор: Марусев Е.А.
            """
            if self.entery_season.get() == 'Зима':
                season_list = winter_list
            elif self.entery_season.get() == 'Лето':
                season_list = summer_list
            self.entery_type = ttk.Combobox(self, values=season_list)
            self.entery_type.bind("<<ComboboxSelected>>", change_subtype)
            self.entery_type.place(x=300, y=290)

        self.entery_season = ttk.Combobox(self, values=['Зима', 'Лето'])
        self.entery_season.bind("<<ComboboxSelected>>", change_type)
        self.entery_season.place(x=300, y=260)

        self.entery_price = ttk.Entry(self)
        self.entery_price.place(x=300, y=350)

        def close():
            """
            close
            Функция, закрывающая дочернее окно.
            Автор: Шайкин Н.С.
            """
            self.btn.config(state=tk.NORMAL)
            self.destroy()
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=close)
        self.btn_cancel.place(x=300, y=400)

        self.btn_add = ttk.Button(self, text='Загрузить')
        self.btn_add.place(x=200, y=400)
        self.btn_add.bind('<Button-1>',
                          lambda event: self.insert(self.entery_iet.get(),
                                                    self.entery_provider.get(),
                                                    self.entery_phone.get(),
                                                    self.entery_country.get(),
                                                    self.entery_client.get(),
                                                    self.entery_tel.get(),
                                                    self.entery_passport.get(),
                                                    self.entery_model.get(),
                                                    self.entery_season.get(),
                                                    self.entery_type.get(),
                                                    self.entery_subtype.get(),
                                                    self.entery_price.get()))

    def chosen(self, num):
        """
        chosen
        Автор: Марусев Е.А.
        Метод возвращает лежащие в строчке значения при ее выборе.
        Параметры: self, num
        num - номер строки
        """
        data = pd.read_csv('./data/db_goods.csv')
        iet = data.loc[num]["ИЕТ"]
        provider = data.loc[num]["Поставщик"]
        client = data.loc[num]["Клиент"]
        name = data.loc[num]["Название модели"]
        season = data.loc[num]["Сезон"]
        ftype = data.loc[num]["Вид инвентаря"]
        sub_type = data.loc[num]["Подвид"]
        price = data.loc[num]["Цена"]
        fields_list = [iet, provider, client, name, season, ftype,
                       sub_type, price]
        return fields_list

    def insert(self, iet, provider, phone, country,
               client, telephone, passport, model,
               season, ftype, subtype, price):
        """
        insert
        Метод добавляющий в базу данных новую строчку на основе введенных данных.
        Инофрмация автоматически добавляется в таблицы товаров и заказчиков
        Параметры: self, iet self, iet, provider, phone, country,
               client, telephone, passport, model,
               season, ftype, subtype, price - все введенные данные

        Автор: Марусев Е.А.
        """
        db_goods = pd.read_csv('./data/db_goods.csv')
        text_goods = db_goods.columns.values
        goods_list = [len(db_goods[text_goods[0]]),
                      iet, provider, client, model, season, ftype,
                      subtype, price]
        db_goods.loc[len(db_goods[text_goods[0]])] = goods_list
        db_goods.to_csv('./data/db_goods.csv', encoding='utf-8', index=False)

        db_customers = pd.read_csv('./data/db_customers.csv')
        text_customers = db_customers.columns.values
        customer_list = [len(db_customers[text_customers[0]]),
                         iet, client, telephone, passport, model]
        db_customers.loc[len(db_customers[text_customers[0]])] = customer_list
        db_customers.to_csv('./data/db_customers.csv',
                            encoding='utf-8', index=False)
        self.destroy()
        self.btn.config(state=tk.NORMAL)
