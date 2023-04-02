import os
from tkinter import BOTH, Frame, Tk, ttk, Entry, Label, CENTER, END, Button, Radiobutton, IntVar, StringVar
from tkinter.ttk import Notebook, Combobox
from abc import ABCMeta, abstractmethod

import matplotlib
import matplotlib.pyplot as plt

from common.models import ValuteConv, ValuteAnalize
from gui.format import ticks_format


class GUIController:
    def __init__(self, model: dict, view):
        self.model = model
        self.view = view

    def start(self):
        self.view.start(self)

    def names(self, with_rub: bool = True):
        return self.model['converter'].names(with_rub=with_rub)

    def convert(self, first, second, count):
        return self.model['converter'].today(first, second, count)

    def period_intervals(self, period):
        return self.model['analyze'].period(period_name=period)

    def prices(self, date_list, valute_name):
        return self.model['analyze'].valute_prices(date_list=date_list, valute_name=valute_name)


class Tab(metaclass=ABCMeta):
    def __init__(self, frame, controller: GUIController):
        self.frame = frame
        self.controller = controller
        self.load_content()

    @property
    @abstractmethod
    def title(self):
        raise NotImplementedError

    @abstractmethod
    def load_content(self):
        raise NotImplementedError


class ExchangeTab(Tab):
    title = 'Обмен валют'

    def __init__(self, frame: Frame, controller):
        super().__init__(frame, controller)

    def load_content(self):
        # Левая колонка
        Label(self.frame, text='У меня имеется').place(x=40, y=10)
        self.combobox1 = Combobox(self.frame, width=20, values=self.controller.names(), font=('Georgia 12'),
                                  state='readonly')
        self.combobox1.current(0)
        self.combobox1.place(x=30, y=40)
        self.combobox1.bind("<<ComboboxSelected>>", self.combobox_handler)

        self.entry1 = Entry(self.frame, show="", width=18, justify=CENTER, name='entry1', font=('Georgia 15'))
        self.entry1.place(x=30, y=95, height=30)
        self.entry1.bind("<KeyRelease>", self.entry_conv_handler)

        # Правая колонка
        Label(self.frame, text='Получу').place(x=335, y=10)
        self.combobox2 = Combobox(self.frame, width=20, values=self.controller.names(), font=('Georgia 12'),
                                  state='readonly')
        self.combobox2.current(0)
        self.combobox2.place(x=325, y=40)
        self.combobox2.bind("<<ComboboxSelected>>", self.combobox_handler)

        self.entry2 = Entry(self.frame, show="", width=18, justify=CENTER, name='entry2', font=('Georgia 15'))
        self.entry2.place(x=325, y=95, height=30)
        self.entry2.bind("<KeyRelease>", self.entry_conv_handler)

    def entry_conv_handler(self, event):
        if len(event.widget.get()) > 0:
            if str(event.widget).split(".")[-1] == 'entry1':
                string = self.controller.convert(self.combobox1.get(), self.combobox2.get(), self.entry1.get())
                entry = self.entry2
            elif str(event.widget).split(".")[-1] == 'entry2':
                string = self.controller.convert(self.combobox2.get(), self.combobox1.get(), self.entry2.get())
                entry = self.entry1
            else:
                raise ValueError
            entry.delete(0, END)
            entry.insert(0, string)
        else:
            self.entry1.delete(0, END)
            self.entry2.delete(0, END)

    def combobox_handler(self, event):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)


class StatisticsTab(Tab):
    title = 'Статистика и графики'

    def __init__(self, frame, controller: GUIController):
        super().__init__(frame, controller)

    def load_content(self):
        # Левая колонка
        Label(self.frame, text='Валюта').place(x=80, y=10)
        self.combobox1 = Combobox(self.frame, width=20, values=self.controller.names(with_rub=False), font=('Georgia 12'))
        self.combobox1.current(0)
        self.combobox1.place(x=10, y=40)
        self.btn = Button(self.frame, width=20, text="Построить график", font=('Georgia 12'), command=self.btn_action)
        self.btn.place(x=10, y=110)

        # Сначала создаём правую часть центральной колонки, а затем левую, чтобы корректно работал хендлер.
        # Центральная колонка, правая часть
        Label(self.frame, text='Выбор периода').place(x=600, y=10)
        self.combobox2 = Combobox(self.frame, width=20, font=('Georgia 12'))
        self.combobox2.place(x=550, y=40)

        # Центральная колонка, левая часть
        Label(self.frame, text='Период').place(x=300, y=10)
        self.rbtn_value = StringVar()

        self.rbtn_week = Radiobutton(self.frame, text="Неделя", value="Неделя", width=20, anchor='w',
                                     variable=self.rbtn_value, command=self.comb_intervals_action)
        self.rbtn_week.invoke()
        self.rbtn_week.place(x=300, y=30)
        self.rbtn_month = Radiobutton(self.frame, text="Месяц", value="Месяц", width=20, anchor='w',
                                      variable=self.rbtn_value, command=self.comb_intervals_action)
        self.rbtn_month.place(x=300, y=50)
        self.rbtn_quart = Radiobutton(self.frame, text="Квартал", value="Квартал", width=20, anchor='w',
                                      variable=self.rbtn_value, command=self.comb_intervals_action)
        self.rbtn_quart.place(x=300, y=70)
        self.rbtn_year = Radiobutton(self.frame, text="Год", value="Год", width=20, anchor='w',
                                     variable=self.rbtn_value, command=self.comb_intervals_action)
        self.rbtn_year.place(x=300, y=90)

        self.rbtn_week.invoke()

    def comb_intervals_action(self):
        comb_option = self.rbtn_value.get()
        self.selected_data = self.controller.period_intervals(period=comb_option)
        self.combobox2['values'] = [k for k in self.selected_data.keys()]
        self.combobox2.current(0)

    def btn_action(self):
        interval = self.combobox2.get()
        interval_title = self.rbtn_value.get()
        dates = self.selected_data[interval]
        prices = self.controller.prices(date_list=dates, valute_name=self.combobox1.get())
        dates = ticks_format(dates=dates, period_name=interval_title)
        self.create_plot()
        self.draw_currency(prices=prices, dates=dates)

    def draw_currency(self, prices: list, dates: list):
        coords_x = []
        d = 1
        for i in range(len(prices)):
            coords_x.append(d)
            d += 1

        plt.xlim(coords_x[0], coords_x[-1])
        plt.autoscale(True, 'y')
        plt.plot(coords_x, prices, 'g')
        plt.grid()
        plt.xticks(coords_x, dates)


    def create_plot(self):
        matplotlib.use('TkAgg')
        fig, ax = plt.subplots(1, 1, figsize=(6.7, 4.1))

        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self.frame)
        plot_widget = self.canvas.get_tk_widget()
        plot_widget.place(x=400, y=100)
        plot_widget
        ax.set_xticklabels(ax.get_xticks(), rotation=25, fontsize=8)


class TabLoader:
    TAB_LIST = [ExchangeTab, StatisticsTab]

    def __init__(self, root_tk, controller):
        self.body = Notebook(root_tk)
        self.controller = controller
        self.children = []
        self.root_geom = ""
        self.root = root_tk
        self.build_tabs()

        self.body.pack(expand=True, fill=BOTH)
        self.body.bind("<<NotebookTabChanged>>", self.change_resol)

    def build_tabs(self):
        '''
        Создание двух вкладок
        :return:
        '''
        for i in range(len(TabLoader.TAB_LIST)):
            frame = Frame(self.body)
            TabLoader.TAB_LIST[i](frame, self.controller)
            self.body.add(frame, text=TabLoader.TAB_LIST[i].title)
            self.children.append(frame)

    def change_resol(self, event):
        '''
        Метод, для переключения размера окна при переключении между вкладками
        :param event:
        :return:
        '''
        if self.root_geom == "600x200":
            self.root_geom = "1100x600"
            self.root.geometry(self.root_geom)
        else:
            self.root_geom = "600x200"
            self.root.geometry(self.root_geom)


class GUI:
    def start(self, controller):
        self.root = Tk()
        self.root.tk.call('source', f'{os.path.dirname(os.path.realpath(__file__))}/forest-light.tcl')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        ttk.Style().theme_use('forest-light')

        self.root.configure(bg="#FFFFFF")
        self.root.resizable(width=False, height=False)
        self.root.title("Конвертер валют")
        self.tabs = TabLoader(self.root, controller)
        self.root.mainloop()

    def on_closing(self):
        self.root.quit()


def run_desktop():
    model = {
        'converter': ValuteConv(),
        'analyze': ValuteAnalize()
    }
    controller = GUIController(view=GUI(), model=model)
    controller.start()
