import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
import datetime
from datetime import  time, date

import TableGeneral
from TableGeneral import MainTable

import TablePoint
from TablePoint import Table

import TablePointMonth
from TablePointMonth import MainPointMonthTable

import TableYearsMonth
from TableYearsMonth import Main

class MainTables(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_main()
    
    def init_main(self):

        frame = tk.Frame(self, bg = 'white')
        frame.pack()

        def g_table_window():
            def close_table():
                g_table_btn.configure(state=tk.NORMAL)
                g_table_window.destroy()

            g_table_btn.configure(state=tk.DISABLED)
            g_table_window = MainTable()
            g_table_window.title("Общая таблица")
            g_table_window.geometry('1500x600+0+50')
            g_table_window["bg"] = "white"
            g_table_window.grab_set()
            g_table_window.focus_set()
            g_table_window.resizable(False, False)
            g_table_window.protocol("WM_DELETE_WINDOW", close_table)


        g_table_btn = tk.Button(frame, text="Общая таблица", width=20, height=3, cursor="hand2", wraplength=0,
                                    command=g_table_window,font=("Helvetica", 9, "bold"),bg = 'white')
        g_table_btn.grid(column = 1, row = 0,padx=20, pady=20)


        def p_table_window():
            def close_table():
                p_table_btn.configure(state=tk.NORMAL)
                p_table_window.destroy()

            p_table_btn.configure(state=tk.DISABLED)
            p_table_window = Table()
            p_table_window.title("Итог по отделам/год")
            p_table_window.geometry('+380+150')
            p_table_window["bg"] = "white"
            p_table_window.grab_set()
            p_table_window.focus_set()
            p_table_window.resizable(False, False)
            p_table_window.protocol("WM_DELETE_WINDOW", close_table)


        p_table_btn = tk.Button(frame, text="Итог по отделам/год", width=20, height=3, cursor="hand2", wraplength=0,
                                    command=p_table_window,font=("Helvetica", 9, "bold"),bg = 'white')
        p_table_btn.grid(column = 1, row = 1,padx=20, pady=20)




        def pm_table_window():
            def close_table():
                pm_table_btn.configure(state=tk.NORMAL)
                pm_table_window.destroy()

            pm_table_btn.configure(state=tk.DISABLED)
            pm_table_window = MainPointMonthTable()
            pm_table_window.title("Итог по отделам/месяц")
            pm_table_window.geometry('400x140+550+150')
            pm_table_window["bg"] = "white"
            pm_table_window.grab_set()
            pm_table_window.focus_set()
            pm_table_window.resizable(False, False)
            pm_table_window.protocol("WM_DELETE_WINDOW", close_table)


        pm_table_btn = tk.Button(frame, text="Итог по отделам/месяц", width=20, height=3, cursor="hand2", wraplength=0,
                                    command=pm_table_window,font=("Helvetica", 9, "bold"),bg = 'white')
        pm_table_btn.grid(column = 1, row = 2,padx=20, pady=20)


        def ym_table_window():
            def close_table():
                ym_table_btn.configure(state=tk.NORMAL)
                ym_table_window.destroy()

            ym_table_btn.configure(state=tk.DISABLED)
            ym_table_window = Main()
            ym_table_window.title("Общий итог")
            ym_table_window.geometry('')
            ym_table_window["bg"] = "white"
            ym_table_window.grab_set()
            ym_table_window.focus_set()
            ym_table_window.resizable(False, False)
            ym_table_window.protocol("WM_DELETE_WINDOW", close_table)


        ym_table_btn = tk.Button(frame, text="Общий итог", width=20, height=3, cursor="hand2", wraplength=0,
                                    command=ym_table_window,font=("Helvetica", 9, "bold"),bg = 'white')
        ym_table_btn.grid(column = 1, row = 3,padx=20, pady=20)