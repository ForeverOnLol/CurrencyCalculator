from tkinter import *
from tkinter.ttk import Notebook, Frame, Combobox
class TabsControl():    
    def __init__ (self, root_tk, tabs_text_list):
        self.body = Notebook(root_tk)
        self.children = []
        self.root_geom = ""
        self.root = root_tk
        for i in range(len(tabs_text_list)):
            self.add_Tab(tabs_text_list[i])
        self.body.pack(expand = True, fill = BOTH)

    def add_Tab(self, txt):
        tab = Frame(self.body)
        self.body.add(tab, text=txt)
        self.children.append(tab)
    def __getitem__(self, i):
        return self.children[i]
    def changeResol(self, event):
            if self.root_geom == "700x175":
                self.root_geom = "1000x750"
                self.root.geometry(self.root_geom)
            else:
                self.root_geom = "700x175"
                self.root.geometry(self.root_geom)
    

def main():
    root = Tk()
    root.title("Конвертер валют")
    root.configure(background='#ffffff')
    root.resizable(width=False, height=False)

    tabscontrol = TabsControl(root, ["Калькулятор валют", "Динамика курса"])
    tab1 = tabscontrol[0]
    tab2 = tabscontrol[1]
    
    combobox1 = Combobox(tab1, width="25")
    combobox1.grid(row = 2, column = 2, rowspan = 2, pady = 20, padx = 15)
    combobox2 = Combobox(tab1, width="25")
    combobox2.grid(row = 4, column = 2, pady = 10, padx = 15)
    entry1 = Entry(tab1, show = "*")
    entry1.grid(row = 2, column = 3, pady = 20, padx = 15)
    label1 = Label(tab1, text="111.222", fg = "black", font = ("Courier New", 14, "bold"), bd = 10)
    label1.grid(row = 4, column = 3)
    btn1 = Button(tab1, text="Конвертировать")
    btn1.grid(row = 2, column = 4, padx = 15)


    label2 = Label(tab2, text="Валюта", fg = "black")
    label2.grid(row = 1, column = 1, pady = 3, padx = 0)
    label3 = Label(tab2, text="Период", fg = "black", padx = 2)
    label3.grid(row = 1, column = 2, pady = 3, padx = 40)
    label4 = Label(tab2, text="Выбор периода", fg = "black")
    label4.grid(row = 1, column = 3, pady = 3, padx = 30)
    combobox3 = Combobox(tab2, width="25")
    combobox3.grid(row = 2, column = 1, pady = 3, padx = 10)

    radiobutton1 = Radiobutton(tab2, text = "Неделя", value = 1, width = 20)
    radiobutton1.grid(row = 2, column = 2, pady = 3)
    radiobutton2 = Radiobutton(tab2, text = "Месяц", value = 2, width = 20)
    radiobutton2.grid(row = 3, column = 2, pady = 3, columnspan=1)
    radiobutton3 = Radiobutton(tab2, text = "Квартал", value = 3, width = 20)
    radiobutton3.grid(row = 4, column = 2, pady = 3)
    radiobutton4 = Radiobutton(tab2, text = "Год", value = 4, width = 20)
    radiobutton4.grid(row = 5, column = 2, pady = 3, )
    combobox4 = Combobox(tab2, width="25")
    combobox4.grid(row = 5, column = 3, rowspan = 2, pady = 3)
    btn2 = Button(tab2, text="Построить график", width=23)
    btn2.grid(row = 5, column = 1,  padx = 10)

    combobox5 = Combobox(tab2, width="25")

    
   
    # button2 = Button(tab2, text="Button #2")
    # button2.pack()
    tabscontrol.body.bind("<<NotebookTabChanged>>", tabscontrol.changeResol)
    root.mainloop()
def personalData(event, root):
    if event.widget.index("current") == 0: 
            root.geometry("700x175")
    else:
            root.geometry("700x12")
main()
