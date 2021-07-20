# -*- coding: utf-8 -*-
"""
    graphics.py
    Авторы: Марусев Е.А., Шайкин Н.С., Шайкин К.А.
    В модуле написана работа с графикой и библиотекой matplotlib.
    Модуль подготавливает иллюстрированные диаграммы и таблицы:
    Базовая Статистика - таблица содержит информацию о числе позиций баз данных
    в зависимости от сезона, Сводная таблица - Таблица содержит список
    всех товаров с указанием сезона и цены, Круговая диаграмма и Столбчатая
    диаграмма - иллюстрируют количество товаров в зависимости от сезона,
    Диаграмма Бокса-Вискера.
"""
import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandas import merge
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
os.chdir("d:/work/")
class MainGraphics(tk.Toplevel):
    """
    MainGraphics
    Автор: Шайкин К.А.
    Класс наследуется от виджета Toplevel из библиотеки tkinter
    Класс представляет собой дочернее окно "Отчетность" вызываемое из main.py,
    Окно содержит 5 кнопок, отвечающие за изображение информации на
    соответствующей диаграмме(таблице).
    """
    def __init__(self):
        """
        Конструктор класса MainGraphics
        Автор: Шайкин К.А.
        Параметры - self.
        """
        super().__init__()
        self.init_main()
    def init_main(self):
        """
        init_main
        Автор: Шайкин К.А.
        Метод выполняет функционал построения таблиц Базовая статистика и
        сводная таблица, столбчатой, круговой и диаграммы Бокса-Вескера.
        Параметры - self.
        """
        def denorm(db1, db2, key):
            """
            denorm
            Автор: Марусев Е.А.
            Функция осуществляет соединение двух таблиц по ключу.
            Параметры - db1, db2 - pandas dataframes, key - ключ слияния
            """
            return merge(db1, db2, on=key)
        dfgoods = pd.read_csv('./data/db_goods.csv')
        dfgoods = dfgoods.drop(['ID'], axis=1)
        dfgoods = dfgoods.drop(['ФИО Заказчика'], axis=1)
        dfprovider = pd.read_csv('./data/db_providers.csv')
        dfprovider = dfprovider.drop(['ID'], axis=1)
        dfclient = pd.read_csv('./data/db_customers.csv')
        dfclient = dfclient.drop(['ID'], axis=1)
        dfclient = dfclient.drop(['Название модели'], axis=1)
        base = denorm(dfprovider, dfgoods, "Поставщик")
        base = denorm(base, dfclient, 'ИЕТ')
        column = base.columns.tolist()
        num = [column[3]] + column[0:3] + column[4:]
        new_columns = num[0:4] + num[-3:] + num[4:9]
        full_list = base[new_columns]
        full_list.to_csv('d://work/data/db_full_list.csv',
                         encoding='utf-8', index=False)
        def basic_stats():
            """
            basic_stats
            Автор: Шайкин К.А.
            Построение базовой статистики
            создание экземпляра класса BasicStatistics.
            """
            BasicStatistics()
        self.grab_set()
        self.focus_set()
        self.stats_btn = tk.Button(self,
                                   text="Базовая статистика",
                                   command=basic_stats)
        self.stats_btn.pack(pady=20)

        def summary_table():
            """
            summary_table
            Автор: Марусев Е.А.
            Построение сводной таблицы
            Создание экземпляра класса SummaryTable
            Параметры отсутствуют
            """
            SummaryTable()
        self.summary_btn = tk.Button(self,
                                     text="Сводная таблица",
                                     command=summary_table)
        self.summary_btn.pack(pady=20)

        def pie_chart():
            """
            pie_chart
            Автор: Марусев Е.А.
            Построение Круговой диаграммы из базы данных "Полный список"
            Параметры отсутствуют
            """
            full_list = pd.read_csv('./data/db_full_list.csv')
            fig = plt.figure()
            axs = fig.add_axes([0, 0, 1, 1])
            axs.axis('equal')
            arg = ['Лето', 'Зима']
            val = [(full_list["Сезон"] == "Лето").sum(),
                   (full_list["Сезон"] == "Зима").sum()]
            axs.pie(val, labels=arg, autopct='%1.2f%%')
            plt.show()
        self.pie_chart_btn = tk.Button(self, text="Круговая диаграмма",
                                       command=pie_chart)
        self.pie_chart_btn.pack(pady=20)
        def bar_chart():
            """
            bar_chart
            Автор: Шайкин Н.С.
            Построение столбчатой диаграммы из базы данных "Полный список"
            Параметры отсутствуют
            """
            groups = ['Лето', 'Зима']
            counts = [(full_list["Сезон"] == "Лето").sum(),
                      (full_list["Сезон"] == "Зима").sum()]
            plt.bar(groups, counts)
        self.bar_chart_btn = tk.Button(self,
                                       text="Столбчатая диаграмма",
                                       command=bar_chart)
        self.bar_chart_btn.pack(pady=20)
        def box_chart():
            """
            box_chart
            Автор: Шайкин Н.С.
            Построение диаграммы Бокса-Вискера из базы данных "Полный список"
            Параметры отсутствуют
            """
            def boxplot(x_data, y_data, base_color="#539caf",
                        median_color="#297083", title=""):
                """
                box_chart
                Автор: Шайкин Н.С.
                Построение диаграммы Бокса-Вескера из базы данных
                "Полный список"
                Параметры:
                    x_data - значение по оси X,
                    y_data - значение по оси Y,
                    base_color - цвет по умолчанию,
                    median_color - медианный цвет,
                    title - заголовок.

                """
                _, axs = plt.subplots()
                axs.boxplot(y_data, patch_artist=True,
                            medianprops={'color': median_color},
                            boxprops={'color': base_color,
                                      'facecolor': base_color},
                                      whiskerprops={'color': base_color},
                                      capprops={'color': base_color})
                axs.set_xticklabels(x_data)
                axs.set_ylabel('Кол-во')
                axs.set_title(title)
            boxplot(['Зима / Лето'],
                    [(full_list["Сезон"] == "Зима").sum(),
                     (full_list["Сезон"] == "Лето").sum()])
        self.box_chart_btn = tk.Button(self,
                                       text="Диаграмма Бокса - Вискера",
                                       command=box_chart)
        self.box_chart_btn.pack(pady=20)


class BasicStatistics(tk.Toplevel):
    """
    BasicStatistics
    Автор: Шайкин К.А.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Представляет собой окно, в котором формируется таблица "Базовая статистика"
    Базовая статистика содержит:
        Количество товаров в зависимости от сезона(Лето / Зима)
        Минимальную и максимальную цену сезона(Лето / Зима)
        Среднюю цену сезона (Лето / Зима)
    """
    def __init__(self):
        """
        Автор: Шайкин К.А.
        Конструктор класса BasicStatistics
        Параметры - self.
        """
        super().__init__()
        self.init_main()

    def init_main(self):
        """
        init_main
        Автор: Шайкин К.А.
        Основной метод формирования таблицы Базовая статистика.
        Параметры - self.
        """
        self.title("Базовая статистика")
        self.geometry("+400+250")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.tree = ttk.Treeview(self, columns=(' ', 'Лето', 'Зима'),
                                 height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.tree.column(" ", width=100, anchor=tk.CENTER)
        self.tree.column('Лето', width=110, anchor=tk.CENTER)
        self.tree.column('Зима', width=200, anchor=tk.CENTER)
        self.tree.heading(' ', text=' ')
        self.tree.heading('Лето', text='Лето')
        self.tree.heading('Зима', text='Зима')
        full_list = pd.read_csv('./data/db_full_list.csv')
        season = full_list["Сезон"]
        price = full_list["Цена"]
        df3 = pd.concat([season, price], axis=1)
        text = df3.columns.values
        winter_max = -1
        summer_max = -1
        sum_winter = 0
        sum_summer = 0
        n_winter = 0
        n_summer = 0
        for i in range(len(df3[text[0]])):
            if df3.loc[i]["Сезон"] == 'Зима':
                winter_min = df3.loc[i]["Цена"]
                sum_winter += df3.loc[i]["Цена"]
                n_winter += 1
            if df3.loc[i]["Сезон"] == 'Лето':
                summer_min = df3.loc[i]["Цена"]
                sum_summer += df3.loc[i]["Цена"]
                n_summer += 1
        for i in range(len(df3[text[0]])):
            if df3.loc[i]["Сезон"] == 'Зима' and df3.loc[i]['Цена'] > winter_max:
                winter_max = df3.loc[i]['Цена']
            if df3.loc[i]["Сезон"] == 'Лето' and df3.loc[i]['Цена'] > summer_max:
                summer_max = df3.loc[i]['Цена']
            if df3.loc[i]["Сезон"] == 'Зима' and df3.loc[i]['Цена'] < winter_min:
                winter_min = df3.loc[i]['Цена']
            if df3.loc[i]["Сезон"] == 'Лето' and df3.loc[i]['Цена'] < summer_min:
                summer_min = df3.loc[i]['Цена']
        if n_winter != 0:
            averagewinter = sum_winter / n_winter
        else:
            averagewinter = "Неудалось подсчитать среднее"
        if n_summer != 0:
            averagesummer = sum_summer / n_summer
        else:
            averagesummer = "Неудалось подсчитать среднее"
        if (full_list["Сезон"] == "Лето").sum() == 0:
            if (full_list["Сезон"] == "Зима").sum() == 0:
                self.tree.insert('', 'end', text='',
                                 values=('Кол-во:', 0, 0))
                self.tree.insert('', 'end', text='',
                                 values=('Max цена:', 0, 0))
                self.tree.insert('', 'end', text='',
                                 values=('Min цена:', 0, 0))
                self.tree.insert('', 'end', text='',
                                 values=('Средняя цена:', 0, 0))
            elif (full_list["Сезон"] == "Зима").sum() != 0:
                self.tree.insert('', 'end', text='',
                                 values=('Кол-во:', 0, (full_list["Сезон"] == "Зима").sum()))
                self.tree.insert('', 'end', text='',
                                 values=('Max цена:', 0, winter_max))
                self.tree.insert('', 'end', text='',
                                 values=('Min цена:', 0, winter_min))
                self.tree.insert('', 'end', text='',
                                 values=('Средняя цена:', 0, averagewinter))
        if (full_list["Сезон"] == "Зима").sum() == 0 and (full_list["Сезон"] == "Лето").sum() != 0:
            self.tree.insert('', 'end', text='',
                             values=('Кол-во:',
                                     (full_list["Сезон"] == "Лето").sum(), 0))
            self.tree.insert('', 'end', text='',
                             values=('Max цена:', summer_max, 0))
            self.tree.insert('', 'end', text='',
                             values=('Min цена:', summer_min, 0))
            self.tree.insert('', 'end', text='',
                             values=('Средняя цена:', averagesummer, 0))
        if (full_list["Сезон"] == "Зима").sum() != 0 and (full_list["Сезон"] == "Лето").sum() != 0:
            self.tree.insert('', 'end', text='',
                             values=('Кол-во:',
                             (full_list["Сезон"] == "Лето").sum(),
                             (full_list["Сезон"] == "Зима").sum()))
            self.tree.insert('', 'end', text='', values=('Max цена:',
                                                         summer_max,
                                                         winter_max))
            self.tree.insert('', 'end', text='', values=('Min цена:',
                                                         summer_min,
                                                         winter_min))
            self.tree.insert('', 'end', text='', values=('Средняя цена:',
                                                         averagesummer,
                                                         averagewinter))
        self.tree.pack()

class SummaryTable(tk.Toplevel):
    """
    SummaryTable
    Автор: Марусев Е.А.
    Класс наследуется от виджета Toplevel библиотеки tkinter
    Класс представляет собой окно, в котором создается сводная таблица,
    содержащая полный список товаров с указанием цены и сезона.
    """
    def __init__(self):
        """
        Конструктор класса SummaryTable
        Автор: Марусев Е.А.
        Класс наследуется от виджета Toplevel библиотеки tkinter
        Класс представляет собой окно, в котором создается сводная таблица,
        содержащая полный список товаров с указанием цены и сезона.
        """
        super().__init__()
        self.init_main()
    def init_main(self):
        """
        init_main
        Автор: Марусев Е.А.
        Основной метод для создания дочернего окна и сводной таблицы
        сводная таблица содержит полный список товаров с указанием цены
        и сезона.
        """
        self.title("Сводная таблица")
        self.geometry("+400+250")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.tree = ttk.Treeview(self, columns=('Название', 'Сезон', 'Цена'),
                                 height=15, show='headings')
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.tree.column("Название", width=100, anchor=tk.CENTER)
        self.tree.column('Сезон', width=110, anchor=tk.CENTER)
        self.tree.column('Цена', width=200, anchor=tk.CENTER)
        self.tree.heading('Название', text='Название')
        self.tree.heading('Сезон', text='Сезон')
        self.tree.heading('Цена', text='Цена')
        data_goods = pd.read_csv('./data/db_goods.csv')
        text_df = data_goods.columns.values
        data = pd.DataFrame(columns=['Название', 'Сезон', 'Цена'])
        for i in range(len(data_goods[text_df[0]])):
            text1 = data.columns.values
            data.loc[len(data[text1[0]])] = [data_goods.loc[i]["Поставщик"] + ' ' + data_goods.loc[i]["Название модели"], data_goods.loc[i]["Сезон"], data_goods.loc[i]["Цена"]]
        text = data.columns.values
        for i in range(len(data[text[0]])):
            self.tree.insert('', 'end', text=data[text[0]][i],
                             values=list(map(lambda x: data[x][i], text[0:])))
        self.tree.pack()
