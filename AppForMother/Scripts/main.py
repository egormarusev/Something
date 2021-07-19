"""
Автор: Шайкин К.А., Шайкин Н.С.
"""

import os
import tkinter as tk
import tkinter.ttk as ttk
import glob
import csv
#from xlsxwriter.workbook import Workbook
import numpy as np
import shutil
import sys



import Sells
from Sells import MainSells

import Expense
from Expense import MainExpense

import Analysis
from Analysis import MainAnalysis

import Tables
from Tables import MainTables

"""import db_customers
from db_customers import MainCustomers

import db_providers
from db_providers import MainProviders

import db_full_list
from db_full_list import MainFull

import DownloadMain
from DownloadMain import DownlMain"""

root = tk.Tk()
root["bg"] = "white"
root.title("Главное меню")
root.geometry('400x500+550+150')
root.resizable(False, False)
frame = tk.Frame(root, bg = 'white')
frame.pack()


def sells_window():
    def close_sells():
        sells_btn.configure(state=tk.NORMAL)
        s_window.destroy()

    sells_btn.configure(state=tk.DISABLED)
    s_window = MainSells()
    s_window.title("Продажи")
    s_window.geometry('400x500+550+150')
    s_window["bg"] = "white"
    s_window.grab_set()
    s_window.focus_set()
    s_window.resizable(False, False)
    s_window.protocol("WM_DELETE_WINDOW", close_sells)


sells_btn = tk.Button(frame, text="Продажи", width=20, height=3, cursor="hand2", command=sells_window,
font=("Helvetica", 9, "bold"),bg = 'white')
sells_btn.grid(column = 0, row = 1,padx=20, pady=20)


def expense_window():
    def close_expense():
        db_expense_btn.configure(state=tk.NORMAL)
        exp_window.destroy()

    db_expense_btn.configure(state=tk.DISABLED)
    exp_window = MainExpense()
    exp_window.title("Расходы")
    exp_window.geometry('400x500+550+150')
    exp_window["bg"] = "white"
    exp_window.grab_set()
    exp_window.focus_set()
    exp_window.resizable(False, False)
    exp_window.protocol("WM_DELETE_WINDOW", close_expense)


db_expense_btn = tk.Button(frame, text="Расходы", width=20, height=3, cursor="hand2", wraplength=0,
                            command=expense_window,font=("Helvetica", 9, "bold"),bg = 'white')
db_expense_btn.grid(column = 0, row = 2,padx=20, pady=20)


"""
def analysis_window():
    def close_analysis():
        db_analysis_btn.configure(state=tk.NORMAL)
        analys_window.destroy()

    db_analysis_btn.configure(state=tk.DISABLED)
    analys_window = MainAnalysis()
    analys_window.title("Анализ")
    analys_window.geometry('400x200+550+150')
    analys_window["bg"] = "white"
    analys_window.grab_set()
    analys_window.focus_set()
    analys_window.resizable(False, False)
    analys_window.protocol("WM_DELETE_WINDOW", close_analysis)


db_analysis_btn = tk.Button(frame, text="Анализ", width=20, height=3, cursor="hand2", wraplength=0,
                            command=analysis_window,font=("Helvetica", 9, "bold"),bg = 'white')
db_analysis_btn.grid(column = 0, row = 3,padx=20, pady=20)
"""

"""
def table_window():
    def close_table():
        db_table_btn.configure(state=tk.NORMAL)
        table_window.destroy()

    db_table_btn.configure(state=tk.DISABLED)
    table_window = MainTable()
    table_window.title("Полная таблица")
    table_window.geometry('1500x600+0+0')
    table_window["bg"] = "white"
    table_window.grab_set()
    table_window.focus_set()
    table_window.resizable(False, False)
    table_window.protocol("WM_DELETE_WINDOW", close_table)


db_table_btn = tk.Button(frame, text="Полная таблица", width=20, height=3, cursor="hand2", wraplength=0,
                            command=table_window,font=("Helvetica", 9, "bold"),bg = 'white')
db_table_btn.grid(column = 0, row = 4,padx=20, pady=20)

"""


def tables_window():
    def close_table():
        db_tables_btn.configure(state=tk.NORMAL)
        tables_window.destroy()

    db_tables_btn.configure(state=tk.DISABLED)
    tables_window = MainTables()
    tables_window.title("Таблицы")
    tables_window.geometry('400x500+550+150')
    tables_window["bg"] = "white"
    tables_window.grab_set()
    tables_window.focus_set()
    tables_window.resizable(False, False)
    tables_window.protocol("WM_DELETE_WINDOW", close_table)


db_tables_btn = tk.Button(frame, text="Таблицы", width=20, height=3, cursor="hand2", wraplength=0,
                            command=tables_window,font=("Helvetica", 9, "bold"),bg = 'white')
db_tables_btn.grid(column = 0, row = 4,padx=20, pady=20)



exit_btn = tk.Button(frame, text="Выйти", width=20, height=3, cursor="hand2",font=("Helvetica", 9, "bold"),bg = 'white')
exit_btn.grid(column=0, row=5, padx=20, pady=20)
exit_btn.config(command=root.destroy)

root.mainloop()
