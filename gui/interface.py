from tkinter import BOTH, Frame, Tk, ttk, Entry, Label, CENTER, END
from tkinter.ttk import Notebook, Combobox
from abc import ABCMeta, abstractmethod


class Tab(metaclass=ABCMeta):
    def __init__(self, frame):
        self.frame = frame
        self.load_content()
    @property
    @abstractmethod
    def title(self):
        raise NotImplementedError

    @abstractmethod
    def load_content(self):
        raise NotImplementedError

    def load_data(self):
        pass



class ExchangeTab(Tab):
    title = 'Обмен валют'

    def __init__(self, frame: Frame):
        super().__init__(frame)

    def load_content(self):
        # Левая колонка
        Label(self.frame, text='У меня имеется').place(x=40, y=10)
        self.combobox1 = Combobox(self.frame, width=20, values=['yes', 'no'], font=('Georgia 12'))
        self.combobox1.current(0)
        self.combobox1.place(x=30, y=40)

        self.entry1 = Entry(self.frame, show="", width=18, justify=CENTER, name='entry1', font=('Georgia 15'))
        self.entry1.place(x=30, y=95, height=30)
        self.entry1.bind("<KeyRelease>", self.entry_conv_handler)

        # Правая колонка
        Label(self.frame, text='Получу').place(x=335, y=10)
        self.combobox2 = Combobox(self.frame, width=20, values=['yes', 'no'], font=('Georgia 12'))
        self.combobox2.current(0)
        self.combobox2.place(x=325, y=40)

        self.entry2 = Entry(self.frame, show="", width=18, justify=CENTER, name='entry2', font=('Georgia 15'))
        self.entry2.place(x=325, y=95, height=30)
        self.entry2.bind("<KeyRelease>", self.entry_conv_handler)

    def entry_conv_handler(self, event):
        value = event.widget.get()
        string = "value '%s'" % (value)
        entry = None

        if str(event.widget).split(".")[-1] == 'entry1':
            entry = self.entry2
        elif str(event.widget).split(".")[-1] == 'entry2':
            entry = self.entry1

        entry.delete(0, END)
        entry.insert(0, string)


class StatisticsTab(Tab):
    title = 'Статистика и графики'

    def __init__(self, frame):
        super().__init__(frame)
    def load_content(self):
        self.combobox1 = Combobox(self.frame, width=20, values=['yes', 'no'], font=('Georgia 12'))
        self.combobox1.current(0)
        self.combobox1.place(x=30, y=40)



class TabController:
    TAB_LIST = [ExchangeTab, StatisticsTab]

    def __init__(self, root_tk):
        self.body = Notebook(root_tk)
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
        for i in range(len(TabController.TAB_LIST)):
            frame = Frame(self.body)
            TabController.TAB_LIST[i](frame)
            self.body.add(frame, text=TabController.TAB_LIST[i].title)
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
    def __init__(self):
        self.root = Tk()
        self.root.tk.call('source', 'forest-light.tcl')
        ttk.Style().theme_use('forest-light')

        self.root.configure(bg="#FFFFFF")
        self.root.resizable(width=False, height=False)
        self.root.title("Конвертер валют")
        self.tabs = TabController(self.root)
        self.root.mainloop()
