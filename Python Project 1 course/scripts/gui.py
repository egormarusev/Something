"""
 main.py
 Автор: Шайкин К.А.
 Осуществляет запуск приложения.
 В этом файле описан интерфейс основного окна (главного меню приложения)
"""

import os
import sys
import shutil
import tkinter as tk
import glob
import csv
#from xlsxwriter.workbook import Workbook

os.chdir("d:/work/")
sys.path.append("../work/")
import library as lib

root = object()


def create_app():
    """
    create_app
    Автор: Шайкин К.А.
    Основная функция для инициализации графического интерфейса
    """
    global root
    root = tk.Tk()
    root.title("Главное меню")
    root.geometry('580x540+450+100')
    root.resizable(False, False)
    frame = tk.Frame(root)
    frame.pack()

    def goods_window():
        """
        goods_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Товары" при нажатии на кнопку "Товары"
        параметры отсутствуют
        """

        def close_goods():
            """
            goods_window
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Товары"
            параметры отсутствуют
            """
            goods_btn.configure(state=tk.NORMAL)
            g_window.destroy()

        goods_btn.configure(state=tk.DISABLED)
        g_window = lib.db_goods.MainGoods()
        g_window.title("Товары")
        g_window.geometry('+240+180')
        g_window.resizable(False, False)
        g_window.protocol("WM_DELETE_WINDOW", close_goods)

    def provider_window():
        """
        provider_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Данные о поставщиках" при нажатии на кнопку
        "Данные о поставщиках"
        параметры отсутствуют
        """

        def close_provider():
            """
            close_provider
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Данные о поставщиках"
            параметры отсутствуют
            """
            db_provider_btn.configure(state=tk.NORMAL)
            pr_window.destroy()

        db_provider_btn.configure(state=tk.DISABLED)
        pr_window = lib.db_providers.MainProviders()
        pr_window.title("Данные о поставщиках")
        pr_window.geometry('+480+180')
        pr_window.resizable(False, False)
        pr_window.protocol("WM_DELETE_WINDOW", close_provider)

    def customer_window():
        """
        provider_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Данные о заказчиках" при нажатии на кнопку
        "Данные о заказчиках"
        параметры отсутствуют
        """

        def close_customer():
            """
            close_customer
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Данные о заказчиках"
            параметры отсутствуют
            """
            db_customer_btn.configure(state=tk.NORMAL)
            c_window.destroy()

        db_customer_btn.configure(state=tk.DISABLED)
        c_window = lib.db_customers.MainCustomers()
        c_window.title("Данные о заказчиках")
        c_window.geometry('+450+180')
        c_window.resizable(False, False)
        c_window.protocol("WM_DELETE_WINDOW", close_customer)

    def graphics_window():
        """
        graphics_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Отчетность" при нажатии на кнопку
        "Отчетность"
        параметры отсутствуют
        """

        def close_graphics():
            """
            close_graphics
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Отчетность"
            параметры отсутствуют
            """
            graphics_btn.configure(state=tk.NORMAL)
            graph_window.destroy()

        graphics_btn.configure(state=tk.DISABLED)
        graph_window = lib.graphics.MainGraphics()
        graph_window.title("Отчетность")
        graph_window.geometry('400x400+450+180')
        graph_window.resizable(False, False)
        graph_window.protocol("WM_DELETE_WINDOW", close_graphics)

    def download_g_window():
        """
        download_g_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Загрузить товар" при нажатии на кнопку
        "Загрузить товар"
        параметры отсутствуют
        """

        def close_download():
            """
            close_download
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Загрузить товар"
            параметры отсутствуют
            """
            download_good_btn.configure(state=tk.NORMAL)
            dl_window.destroy()

        download_good_btn.configure(state=tk.DISABLED)
        dl_window = lib.download_main.DownlMain(download_good_btn)
        dl_window.title("Загрузить товар")
        dl_window.geometry('600x600+450+180')
        dl_window.resizable(False, False)
        dl_window.protocol("WM_DELETE_WINDOW", close_download)

    def save_window():
        """
        save_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Сохранить данные" при нажатии на кнопку
        "Сохранить данные"
        параметры отсутствуют
        """

        def close_save():
            """
            close_save
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Сохранить данные"
            параметры отсутствуют
            """
            save_btn.configure(state=tk.NORMAL)
            sv_window.destroy()

        def save_goods():
            """
            save_goods
            автор: Шайкин К.А.
            Функция осуществляет экспорт таблицы
            "Товары" в формат xlsx при нажатии на кнопку
            "Сохранить "Данные о поставщиках"" дочернего окна "Сохранить данные"
            параметры отсутствуют
            """
            for csvfile in glob.glob(os.path.join('data/', 'db_goods.csv')):
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf8') as file:
                    reader = csv.reader(file)
                    for r_param, row in enumerate(reader):
                        for c_param, col in enumerate(row):
                            worksheet.write(r_param, c_param, col)
                workbook.close()
            shutil.copyfile(os.path.join('data/db_goods.xlsx'),
                            os.path.join('output/Товары.xlsx'))
            os.remove(os.path.join('data/db_goods.xlsx'))
            save_goods_btn.configure(state=tk.DISABLED,
                                     text="Успешно сохранено!")

        def save_providers():
            """
            save_providers
            автор: Шайкин К.А.
            Функция осуществляет экспорт таблицы
            "Данные о поставщиках"" в формат xlsx при нажатии на кнопку
            "Сохранить "Данные о поставщиках"" дочернего окна "Сохранить данные"
            параметры отсутствуют
            """
            for csvfile in glob.glob(os.path.join('data/',
                                                  'db_providers.csv')):
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf8') as file:
                    reader = csv.reader(file)
                    for r_param, row in enumerate(reader):
                        for c_param, col in enumerate(row):
                            worksheet.write(r_param, c_param, col)
                workbook.close()
            shutil.copyfile(os.path.join('data/db_providers.xlsx'),
                            os.path.join('output/Информация о поставщиках.xlsx'))
            os.remove(os.path.join('data/db_providers.xlsx'))
            save_prov_btn.configure(state=tk.DISABLED, text="Успешно сохранено!")

        def save_customers():
            """
            save_customers
            автор: Шайкин К.А.
            Функция осуществляет экспорт таблицы
            "Данные о заказчиках"" в формат xlsx при нажатии на кнопку
            "Сохранить "Данные о заказчиках"" дочернего окна "Сохранить данные"
            параметры отсутствуют
            """
            for csvfile in glob.glob(os.path.join('data/', 'db_customers.csv')):
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf8') as file:
                    reader = csv.reader(file)
                    for r_param, row in enumerate(reader):
                        for c_param, col in enumerate(row):
                            worksheet.write(r_param, c_param, col)
                workbook.close()
            shutil.copyfile(os.path.join('data/db_customers.xlsx'),
                            os.path.join('output/Информация о заказчиках.xlsx'))
            os.remove(os.path.join('data/db_customers.xlsx'))
            save_customers_btn.configure(state=tk.DISABLED,
                                         text="Успешно сохранено!")

        def save_full():
            """
            save_full
            автор: Шайкин К.А.
            Функция осуществляет экспорт таблицы
            "Полный список" в формат xlsx при нажатии на кнопку
            "Сохранить "Полный список"" дочернего окна "Сохранить данные"
            параметры отсутствуют
            """
            for csvfile in glob.glob(os.path.join('data/', 'db_full_list.csv')):
                workbook = Workbook(csvfile[:-4] + '.xlsx')
                worksheet = workbook.add_worksheet()
                with open(csvfile, 'rt', encoding='utf8') as file:
                    reader = csv.reader(file)
                    for r_param, row in enumerate(reader):
                        for c_param, col in enumerate(row):
                            worksheet.write(r_param, c_param, col)
                workbook.close()
            shutil.copyfile(os.path.join('data/db_full_list.xlsx'),
                            os.path.join('output/Полный список.xlsx'))
            os.remove(os.path.join('data/db_full_list.xlsx'))
            save_full_btn.configure(state=tk.DISABLED, text="Успешно сохранено!")

        save_btn.configure(state=tk.DISABLED)
        sv_window = tk.Toplevel()
        sv_window.title("Сохранить данные")
        sv_window.geometry('580x300+450+180')
        sv_window.resizable(False, False)

        save_goods_btn = tk.Button(sv_window, text="Сохранить \"Товары\"",
                                   command=save_goods)
        save_goods_btn.pack(pady=20)

        save_prov_btn = tk.Button(sv_window,
                                  text="Сохранить \"Информация о поставщиках\"",
                                  command=save_providers)
        save_prov_btn.pack(pady=20)

        save_customers_btn = tk.Button(sv_window,
                                       text="Сохранить\"Информация о заказчиках\"",
                                       command=save_customers)
        save_customers_btn.pack(pady=20)

        save_full_btn = tk.Button(sv_window, text="Сохранить \"Полный список\"",
                                  command=save_full)
        save_full_btn.pack(pady=20)

        sv_window.protocol("WM_DELETE_WINDOW", close_save)

    def full_list_window():
        """
        full_list_window
        автор: Шайкин К.А.
        Функция осуществляет запуск дочернего
        окна приложения "Полный список" при нажатии на кнопку
        "полный список"
        параметры отсутствуют
        """

        def close_full_list():
            """
            close_provider
            автор: Шайкин К.А.
            Функция осуществляет закрытие дочернего окна "Полный список"
            параметры отсутствуют
            """
            full_list_btn.configure(state=tk.NORMAL)
            fl_window.destroy()

        full_list_btn.configure(state=tk.DISABLED)
        fl_window = lib.db_full_list.MainFull()
        fl_window.title("Полный список")
        fl_window.geometry('+40+100')
        fl_window.resizable(False, False)
        fl_window.protocol("WM_DELETE_WINDOW", close_full_list)

    goods_btn = tk.Button(frame, text="Товары", width=20, height=3,
                          cursor="hand2", command=goods_window)
    goods_btn.grid(column=2, row=1, pady=20)

    db_provider_btn = tk.Button(frame, text="Данные о поставщиках", width=20,
                                height=3, cursor="hand2", wraplength=0,
                                command=provider_window)
    db_provider_btn.grid(column=1, row=2, padx=20, pady=20)
    db_customer_btn = tk.Button(frame, text="Данные о заказчиках", width=20,
                                height=3, cursor="hand2",
                                command=customer_window)
    db_customer_btn.grid(column=3, row=2, padx=(20), pady=(20))
    graphics_btn = tk.Button(frame, text="Отчетность", width=20,
                             height=3, cursor="hand2",
                             command=graphics_window)
    graphics_btn.grid(column=1, row=3, padx=(20), pady=(20))

    download_good_btn = tk.Button(frame, text="Загрузить товар",
                                  width=20, height=3, cursor="hand2",
                                  command=download_g_window)
    download_good_btn.grid(column=3, row=3, padx=20, pady=20)
    save_btn = tk.Button(frame, text="Сохранить данные",
                         width=20, height=3,
                         cursor="hand2", command=save_window)
    save_btn.grid(column=1, row=4, padx=(20), pady=(20))

    full_list_btn = tk.Button(frame, text="Полный список",
                              width=20, height=3,
                              cursor="hand2", command=full_list_window)
    full_list_btn.grid(column=3, row=4, padx=20, pady=20)

    exit_btn = tk.Button(frame, text="Выйти",
                         width=20, height=3,
                         cursor="hand2")
    exit_btn.grid(column=2, row=5, padx=20, pady=20)
    exit_btn.config(command=root.destroy)


def mainloop():
    """
    mainloop
    Автор: Шайкин К.А.
    Запуск основного цикла интерфейса
    """
    global root

    root.mainloop()
