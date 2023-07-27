import os
from tkinter import *

class Test:

    def __init__(self):
        self.root = Tk()
        self.cwd = os.getcwd()
        self.logs = self.cwd + "\\simulations_logs\\"
        self.temp = self.cwd + "\\temp\\"
        self.counter_file = self.cwd + "\\counter.txt"
        self.counter_test = '29'
        self.requested_person = 'person_1000'
        self.days = 50
        self.labels = []
        self.input("ENTER DAY", "ENTER PERSON", "CLEAR")
        self.root.mainloop()

    def get_data(self, day):
        print(day)
        self.data = []
        with open(self.logs + f"simulation_{self.counter_test}\\day_{day}.txt") as f:
            for i in range(0):
                self.data.append(f.readlines()[i].rstrip('\n'))
        print(self.data)

    def get_person(self, day):
        self.activity = []
        for i in range(1, day):
            with open(self.logs + f"simulation_{self.counter_test}\\day_{i}.txt") as f:
                for line in f.readlines():
                    if 'person_100' in line:
                        self.activity.append(line.rstrip('\n'))

    def input(self, enter, enter1, enter2):
        self.e = Entry(self.root, width=50, bg='black', fg='white', borderwidth=5)
        day = Button(self.root, text=enter, command=self.click)
        self.e.pack()
        day.pack()

        self.e1 = Entry(self.root, width=50, bg='black', fg='white', borderwidth=5)
        person = Button(self.root, text=enter1, command=self.click1)
        self.e1.pack()
        person.pack()

        clear = Button(self.root, text=enter2, command=self.clear)
        clear.pack()

    def click(self):
        requested_day = self.e.get()
        self.get_data(int(requested_day))
        label = Label(self.root, text=f"DAY {requested_day}")
        self.labels.append(label)
        label.pack()
        for data in self.data:
            label1 = Label(self.root, text=data)
            self.labels.append(label1)
            label1.pack()

    def click1(self):
        self.get_person(self.days)


    def clear(self):
        for label in self.labels:
            label.destroy()
        pass

Test()