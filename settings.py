from tkinter import *

"""
This file includes the Settings class, parent class to Main class in main.py. 
Gets all user inputs via a gui and stores them.
Uses function is_valid_input to reject non valid user input until valid input entered.
"""

class Settings:

    def __init__(self):
        self.root = Tk()
        self.counter = 0
        self.rates = ["INFECTION RATE (Eg '15%')", "RECOVERY RATE", "DEATH RATE", "START SUSCEPTIBLE (MAX 100,000)",
                      "START INFECTED (MAX 100,000)", "PANDEMIC DURATION (DAYS)"]
        self.inputs = []
        self.get_inputs()
        self.root.mainloop()

    def assign_variables(self):
        self.infection_rate = self.inputs[0]
        self.recovery_rate = self.inputs[1]
        self.death_rate = self.inputs[2]
        self.start_susceptible = self.inputs[3]
        self.start_infected = self.inputs[4]
        self.day = self.inputs[5]

    def click(self):
        user_input = self.e.get().replace('%', '')
        valid_inputs = []
        if self.counter < 3:
            for i in range(0, 101):
                valid_inputs.append(str(i))
                char = '%'
        elif 3 <= self.counter < 6:
            for i in range(0, 100001):
                valid_inputs.append(str(i))
                char = ''
        else:
            valid_inputs = ('Y', 'y')

        if self.is_valid_input(user_input, valid_inputs):
            self.inputs.append(int(user_input))
            label = Label(self.root, text=(f"{self.rates[self.counter]}: {user_input}{char}"))
            label.pack()
            self.counter += 1
            self.get_inputs()
        else:
            label = Label(self.root, text=("-----INVALID INPUT-----"))
            label.pack()
            pass

    def is_valid_input(self, user_input, valid_inputs):
        if user_input in valid_inputs:
            return True
        else:
            print("-----INVALID INPUT-----")
            return False

    def get_inputs(self):
        if self.counter == 6:
            self.root.destroy()
            self.assign_variables()
        else:
            self.input(self.rates[self.counter])

    def input(self, enter):
        self.e = Entry(self.root, width=50, bg='black', fg='white', borderwidth=5)
        self.e.pack()
        self.button = Button(self.root, text=enter, command=self.click)
        self.button.pack()
