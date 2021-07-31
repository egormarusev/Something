import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
plt.style.use('ggplot')
import pandas as pd
import os.path
#os.environ['MATPLOTLIBDATA'] = 'location of mpl-data folder'

class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
    
    def init_main(self):
        root["bg"] = "white"

        #Init values to Entry
        init_values = np.arange(12) * 0 + 1
        if os.path.exists('data.csv'):
            data = pd.read_csv('data.csv')
            init_values = data.values[0]
        #print(init_values)
        #print(init_values[5:])
        #print(data)

        #Labels of price
        label_price = tk.Label(root, text = 'Цена:', bg = 'white')
        label_price.place(x=155, y=20)

        label_fxdm_price = tk.Label(root, text = 'FXDM', bg = 'white')
        label_fxdm_price.place(x=50, y=50)

        label_games_price = tk.Label(root, text = 'Games', bg = 'white')
        label_games_price.place(x=50, y=80)

        label_gold_price = tk.Label(root, text = 'Gold', bg = 'white')
        label_gold_price.place(x=50, y=110)

        label_tips_price = tk.Label(root, text = 'Tips', bg = 'white')
        label_tips_price.place(x=50, y=140)

        label_nasdaq_price = tk.Label(root, text = 'NASDAQ', bg = 'white')
        label_nasdaq_price.place(x=40, y=170)

        #Input lines for price
        self.entery_fxdm_price = ttk.Entry(root,justify='center')
        self.entery_fxdm_price.insert(0, init_values[2])
        self.entery_fxdm_price.place(x = 100, y = 50)

        self.entery_games_price = ttk.Entry(root,justify='center')
        self.entery_games_price.insert(0, init_values[1])
        self.entery_games_price.place(x = 100, y = 80)

        self.entery_gold_price = ttk.Entry(root,justify='center')
        self.entery_gold_price.insert(0, init_values[4])
        self.entery_gold_price.place(x = 100, y = 110)

        self.entery_tips_price = ttk.Entry(root,justify='center')
        self.entery_tips_price.insert(0, init_values[3])
        self.entery_tips_price.place(x = 100, y = 140)

        self.entery_nasdaq_price = ttk.Entry(root,justify='center')
        self.entery_nasdaq_price.insert(0, init_values[0])
        self.entery_nasdaq_price.place(x = 100, y = 170)

        #Label of numbers
        label_num = tk.Label(root, text = 'Кол-во:', bg = 'white')
        label_num.place(x=246, y=20)

        #Input lines for numbers
        self.entery_fxdm_num = ttk.Entry(root,width=6,justify='center')
        self.entery_fxdm_num.insert(0, int(init_values[7]))
        self.entery_fxdm_num.place(x = 250, y = 50)

        self.entery_games_num = ttk.Entry(root,width=6,justify='center')
        self.entery_games_num.insert(0, int(init_values[6]))
        self.entery_games_num.place(x = 250, y = 80)

        self.entery_gold_num = ttk.Entry(root,width=6,justify='center')
        self.entery_gold_num.insert(0, int(init_values[9]))
        self.entery_gold_num.place(x = 250, y = 110)

        self.entery_tips_num = ttk.Entry(root,width=6,justify='center')
        self.entery_tips_num.insert(0, int(init_values[8]))
        self.entery_tips_num.place(x = 250, y = 140)

        self.entery_nasdaq_num = ttk.Entry(root,width=6,justify='center')
        self.entery_nasdaq_num.insert(0, int(init_values[5]))
        self.entery_nasdaq_num.place(x = 250, y = 170)

        #Label of dolar
        label_dolar = tk.Label(root, text = 'Доллар', bg = 'white')
        label_dolar.place(x=40, y=220)

        #Input line of dolar
        self.entery_dolar = ttk.Entry(root,justify='center')
        self.entery_dolar.insert(0, init_values[10])
        self.entery_dolar.place(x = 100, y = 220)


        #Label of add money
        label_add_money = tk.Label(root, text = 'Добавить', bg = 'white')
        label_add_money.place(x=35, y=260)

        #Input line of add money
        self.entery_add_money = ttk.Entry(root,justify='center')
        self.entery_add_money.insert(0, init_values[11])
        self.entery_add_money.place(x = 100, y = 260)

        #Buttons
        btn_now = tk.Button(root,text = 'Портфель сейчас', command = self.open_show_now)
        btn_now['bg'] = 'white'
        btn_now.place(x = 20, y= 300)
        
        btn_to_buy = tk.Button(root,text = 'Сколько докупить', command = self.open_to_buy)
        btn_to_buy['bg'] = 'white'
        btn_to_buy.place(x = 140, y= 300)

        btn_to_save = tk.Button(root,text = 'Сохранить', command = self.save)
        btn_to_save['bg'] = 'white'
        btn_to_save.place(x = 265, y= 300)


    def open_show_now(self):
        self.numbers_ = np.array([int(float(self.entery_nasdaq_num.get())), int(float(self.entery_games_num.get())),
                             int(float(self.entery_fxdm_num.get())),
                             int(float(self.entery_tips_num.get())),
                             int(float(self.entery_gold_num.get()))])
        self.prices_ = np.array([float(self.entery_nasdaq_price.get()), float(self.entery_games_price.get()), float(self.entery_fxdm_price.get()),
                             float(self.entery_tips_price.get()), float(self.entery_gold_price.get())])



        prices = self.prices_.copy()
        dolar = float(self.entery_dolar.get())
        prices[0] *= dolar
        sums = self.numbers_ * prices
        total = sums.sum()
        precents = sums / total * 100
        
        labels = 'NASDAQ', 'Games', 'FXDM', 'Tips', 'Gold'
        sizes = precents

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        
        ax1.axis('equal')

        plt.show()

    def open_to_buy(self):
        to_buy = self.how_many_buy()
        to_buy = to_buy.astype(int)
        def addlabels(x,y):
            for i in range(len(x)):
                plt.text(i, y[i]/2, y[i], ha = 'center')
        x = 'NASDAQ', 'Games', 'FXDM', 'Tips', 'Gold'
        y = to_buy 
        y_list = y.tolist()
        y_list[0] = y_list[0] / 10
        plt.figure(figsize = (10, 5))
        plt.bar(x, y_list, color = ['#e34930','#318bbe', '#998fd6', '#777777', '#fbc25e'])
        addlabels(x, y_list)
        plt.title("Докупить бумаги")
        plt.show()
        


    def how_many_buy(self):
        porpose_precent = np.array([0.25, 0.25, 0.25, 0.15, 0.10])
        self.numbers_ = np.array([int(float(self.entery_nasdaq_num.get())), int(float(self.entery_games_num.get())),
                             int(float(self.entery_fxdm_num.get())),
                             int(float(self.entery_tips_num.get())), int(float(self.entery_gold_num.get()))])
        self.prices_ = np.array([float(self.entery_nasdaq_price.get()), float(self.entery_games_price.get()), float(self.entery_fxdm_price.get()),
                             float(self.entery_tips_price.get()), float(self.entery_gold_price.get())])

        numbers = self.numbers_
        prices1 = self.prices_
        dolar = float(self.entery_dolar.get())
        add = float(self.entery_add_money.get())

        price = prices1.copy()
        sums = numbers * price
        sums[0] *= dolar

        total = sums.sum()
        new_total = total + add

        purpose_sums = porpose_precent * new_total

        diff = purpose_sums - sums
        diff[0] /= dolar

        to_buy = diff / price
        
        return to_buy


    def save(self):
        values = [float(self.entery_nasdaq_price.get()), float(self.entery_games_price.get()), float(self.entery_fxdm_price.get()),
                  float(self.entery_tips_price.get()), float(self.entery_gold_price.get()),int(float(self.entery_nasdaq_num.get())),
                  int(float(self.entery_games_num.get())), int(float(self.entery_fxdm_num.get())),
                  int(float(self.entery_tips_num.get())), int(float(self.entery_gold_num.get())), float(self.entery_dolar.get()),
                  float(self.entery_add_money.get())]
        name_columns = ['nasdaq_price', 'games_price', 'fxdm_price', 'tips_price', 'gold_price',
                        'nasdaq_num', 'games_num', 'fxdm_num', 'tips_num', 'gold_num', 'dollar', 'add']
        data = pd.DataFrame(data=[values], columns=name_columns)
        data.to_csv('data.csv', index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Инвестиционный Портфель")
    root.geometry("350x340+570+180")
    root.resizable(False, False)
    root.mainloop()