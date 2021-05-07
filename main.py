from datetime import *
from tkinter import *
from tkinter.ttk import Notebook, Frame, Combobox
from module_functions import *
from module_structures import *
from module_parse import *

import matplotlib
import matplotlib.pyplot as plt
import math 
import pylab




# Класс, реализующий управление вкладками и их создание.
class TabsControl:    
    def __init__ (self, root_tk, tabs_text_list):
        self.body = Notebook(root_tk)
        self.children = []
        self.root_geom = ""
        self.root = root_tk
        for i in range(len(tabs_text_list)):
            self.add_Tab(tabs_text_list[i])
        self.body.pack(expand = True, fill = BOTH)
    # Создание вкладок и их добавление в управление
    def add_Tab(self, txt):
        tab = Frame(self.body)
        self.body.add(tab, text=txt)
        self.children.append(tab)
    def __getitem__(self, i):
        return self.children[i]
    # Метод, для переключения размера окна при переключении между вкладками
    def changeResol(self, event):
            if self.root_geom == "700x175":
                self.root_geom = "1100x600"
                self.root.geometry(self.root_geom)
            else:
                self.root_geom = "700x175"
                self.root.geometry(self.root_geom)

class SelectedCombobox():
    def checkRadioButton(self):
        value = lang.get()
        self.period_name = setvalues(value)
        combobox4["values"] = findboxvalues(setvalues(value))
        combobox4.set('')
        combobox4.current(0)
        combobox4.grid(row = lang.get(), column = 3)
        num = combobox4.current() + 1
        self.period = getPeriod(self.period_name, num)
        self.dates_list = finddates(self.period[0], self.period[1])
    def setdates(self, event):
        num = combobox4.current() + 1
        self.period = getPeriod(self.period_name, num)
        self.dates_list = finddates(self.period[0], self.period[1])
    def getdates(self):
        return self.dates_list

 



def getTimeNow():
    d1 = datetime.utcnow()
    return (d1.strftime("%d/%m/%Y"))
def runConvert():
    el_was =  all_valutegroup_today[combobox1.current()]
    el_be =  all_valutegroup_today[combobox2.current()]
    was_val = el_was.price
    be_val = el_be.price
    money = entry1.get()
    was_val_count = el_was.count
    be_val_count = el_be.count
    result_convert = float(money)*float(was_val)*float(be_val_count)/(float(be_val)*float(was_val_count))
    label1.config(text=result_convert)


def setSchedule(labels, y_list):
    # настройка значений графика    
    xlist = []
    d = 1
    for i in range(len(y_list)):
        xlist.append(d)
        d+=1
    plt.xlim(xlist[0], xlist[-1])
    plt.autoscale(True, 'y')
    plt.plot(xlist, y_list, 'g')
    plt.xticks(xlist, labels)
    canvas.draw()
    

# Функция-контроллер для запуска парсера и постройки графика
def runSchedule():
    plt.gcf().clear()
    plt.grid()
    name = combobox3.get()    
    dates_list = selectedcmb.getdates()
    value_list = []
    labels = dates_list
    if (selectedcmb.period_name != 'quarts' and selectedcmb.period_name != "years"):
        for i in range(len(dates_list)):            
            el = float(runParse(dates_list[i], False, name).price)
            value_list.append(el)
    if (selectedcmb.period_name == 'quarts'):
        for i in range(len(dates_list)):
            if (dates_list[i][:2] == '01' or dates_list[i][:2] == '15'):
                el = runParse(dates_list[i], False, name).price
                value_list.append(el)
        last_el = runParse(dates_list[len(dates_list) - 1] , False, name).price
        value_list.append(last_el)
    if (selectedcmb.period_name == 'years'):
        for i in range(len(dates_list)):
            if (dates_list[i][:2] == '01' or dates_list[i][:2] == '15'):
                el = runParse(dates_list[i], False, name).price
                value_list.append(el)
        last_el = runParse(dates_list[len(dates_list) - 1] , False, name).price
    labels = shorttitle(selectedcmb.period_name, labels)
    setSchedule(labels, value_list)
    
    
    


root = Tk()
root.title("Конвертер валют")
root.configure(background='#ffffff')
root.resizable(width=False, height=False)
tabscontrol = TabsControl(root, ["Калькулятор валют", "Динамика курса"])
tab1 = tabscontrol[0]
tab2 = tabscontrol[1]

all_valutegroup_today = runParse(getTimeNow(), TRUE)
# list_valute_now = runParse(getTimeNow())
list_valute_names = ()

for el in all_valutegroup_today:
    p = str(el.name)
    list_valute_names = list_valute_names+ (p,)

# Все элементы первой вкладки
combobox1 = Combobox(tab1, width="25")


combobox1["values"] = list_valute_names
combobox1.grid(row = 2, column = 2, rowspan = 2, pady = 20, padx = 15)
combobox2 = Combobox(tab1, width="25")
combobox2["values"] = list_valute_names
combobox2.grid(row = 4, column = 2, pady = 10, padx = 15)


entry1 = Entry(tab1, show = "")
entry1.grid(row = 2, column = 3, pady = 20, padx = 15)
label1 = Label(tab1, text="0", fg = "black", font = ("Courier New", 14, "bold"), bd = 10)
label1.grid(row = 4, column = 3)
btn1 = Button(tab1, text="Конвертировать", command=runConvert)
btn1.grid(row = 2, column = 4, padx = 15)

# Все элементы второй вкладки
label2 = Label(tab2, text="Валюта", fg = "black")
label2.grid(row = 1, column = 1, pady = 3, padx = 0)
label3 = Label(tab2, text="Период", fg = "black", padx = 2)
label3.grid(row = 1, column = 2, pady = 3, padx = 40)
label4 = Label(tab2, text="Выбор периода", fg = "black")
label4.grid(row = 1, column = 3, pady = 3, padx = 30)
combobox3 = Combobox(tab2, width="25")
combobox3["values"] = list_valute_names
combobox3.grid(row = 2, column = 1, pady = 3, padx = 10)

lang = IntVar()
value_list = []

selectedcmb = SelectedCombobox()
combobox4 = Combobox(tab2, width="25")
radiobutton1 = Radiobutton(tab2, text = "Неделя", value = 2, width = 20, variable=lang, command=selectedcmb.checkRadioButton)
# Эмитация нажатия(дефолтное значение, при выборе вкладки)
radiobutton1.invoke()
radiobutton1.grid(row = 2, column = 2, pady = 3)
radiobutton2 = Radiobutton(tab2, text = "Месяц", value = 3, width = 20, variable=lang, command=selectedcmb.checkRadioButton)
radiobutton2.grid(row = 3, column = 2, pady = 3, columnspan=1)
radiobutton3 = Radiobutton(tab2, text = "Квартал", value = 4, width = 20, variable=lang, command=selectedcmb.checkRadioButton)
radiobutton3.grid(row = 4, column = 2, pady = 3)
radiobutton4 = Radiobutton(tab2, text = "Год", value = 5, width = 20, variable=lang, command=selectedcmb.checkRadioButton)
radiobutton4.grid(row = 5, column = 2, pady = 3)


btn2 = Button(tab2, text="Построить график", width=23, command=runSchedule)
btn2.grid(row = 5, column = 1,  padx = 10)
# создание графика
# установка расположения графика на вкладке
matplotlib.use('TkAgg')

fig, ax = plt.subplots(1, 1, figsize=(5.5, 4.1))
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
plot_widget = canvas.get_tk_widget()
plot_widget.grid(row=7, column=4)

    
tabscontrol.body.bind("<<NotebookTabChanged>>", tabscontrol.changeResol)
combobox4.bind("<<ComboboxSelected>>", selectedcmb.setdates)
root.mainloop()
