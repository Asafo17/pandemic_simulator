from random import randint
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
from settings import *
import os

"""
Created on Sun August 8th 2021

@author Dan Asafo-Agyei

This file includes the Pandemic and Animation class.

Run this module to run the simulation.
"""

class Pandemic(Settings):

    def __init__(self):

        """Initialises all lists and values that are needed in program,
        defines some folder and file paths"""

        super().__init__()
        self.files = ['susceptible.txt', 'infected.txt', 'recovered.txt', 'dead.txt']
        self.cwd = os.getcwd()
        self.logs = self.cwd + "\\simulations_logs\\"
        self.temp = self.cwd + "\\temp\\"
        self.counter_file = self.cwd + "\\counter.txt"
        self.current_day = 0
        self.activity_store, self.susceptible_people, self.infected_people, self.recovered_people, self.dead_people = \
            ([] for i in range(5))
        self.susceptible = [self.start_susceptible]
        self.infected = [self.start_infected]
        self.recovered = [0]
        self.dead = [0]
        self.run()

    def run(self):

        """Main function in the class. Runs other functions in the class."""

        self.create_folders()
        self.file_clear()
        self.starting_lists(self.start_susceptible, self.start_infected)
        self.adjust_inputs()
        while self.current_day < self.day:
            self.days()
            self.pandemic_growth()
            self.file_write()
            self.add_to_log()

    def create_folders(self):

        """Creates folder when called. Each new folder has a label with n+1 compared to
        previous folder. Creates files for message and writes input message to file."""

        number = int(self.counter1())
        os.mkdir(self.logs + f"simulation_{number}")
        new_number = number + 1
        with open(self.counter_file, 'w') as f:
            f.write(str(new_number))

    def counter1(self):
        with open(self.counter_file, 'r') as f:
            number = f.readline()
            return number

    def starting_lists(self, start_susceptible, start_infected):

        """Appends lists with starting values from user input."""

        for i in range(1, start_susceptible + 1):
            self.susceptible_people.append(f"person_{i}")
        for i in range(start_susceptible + 1, (start_infected + start_susceptible) + 1):
            self.infected_people.append(f"person_{i}")

    def days(self):

        """Adds 1 to current day when called."""

        self.current_day = self.current_day + 1
        print(f"\nDay: {self.current_day}")

    def add_to_log(self):

        """Writes statistics and activity to folder simulation_logs."""

        number = int(self.counter1()) - 1
        with open(self.logs + f"simulation_{number}\\day_{self.current_day}.txt", 'a') as f:
            f.write(self.statistics())
            for activity in self.activity_store:
                f.write(activity)

    def pandemic_growth(self):

        """Uses random integer from 1-100 to determine what each infected person will do. Divides range of 1-100 into
        4 sections based on user input.

        Person infects another person.
        Person recovers and is no longer susceptible.
        Person dies from infection.
        Person does nothing.

        Sorts each person into corresponding list based on what random integer is generated."""

        for person in self.infected_people:
            random = randint(1, 101)
            if random <= self.infection_rate:
                if len(self.susceptible_people) == 0:
                    pass
                else:
                    popped_susceptible = self.susceptible_people.pop(randint(0, len(self.susceptible_people) - 1))
                    self.infected_people.append(popped_susceptible)
                    self.activity_store.append(f"\n{person} infected {popped_susceptible}")

            elif self.infection_rate < random <= self.infection_rate + self.recovery_rate:
                popped_infected = self.infected_people.pop(randint(0, len(self.infected_people) - 1))
                self.recovered_people.append(popped_infected)
                self.activity_store.append(f"\n{popped_infected} recovered")

            elif random == (self.infection_rate + self.recovery_rate + self.death_rate):
                popped_infected = self.infected_people.pop(randint(0, len(self.infected_people) - 1))
                self.dead_people.append(popped_infected)
                self.activity_store.append(f"\n{popped_infected} died")
            else:
                pass

    def statistics(self):

        """Returns total number of people in each group when called."""

        self.susceptible.append(len(self.susceptible_people))
        self.infected.append(len(self.infected_people))
        self.recovered.append(len(self.recovered_people))
        self.dead.append(len(self.dead_people))
        return f"Infected: {self.infected[-1]}\nSusceptible: {self.susceptible[-1]}\n" \
               f"Recovered: {self.recovered[-1]}\nDead: {self.dead[-1]}\n\nActivity log:\n"

    def adjust_inputs(self):

        """If total user input for rates > 100% would cause bugs, adjusts each value accordingly so < 100%."""

        sum = self.infection_rate + self.recovery_rate + self.death_rate
        if sum > 100:
            difference = sum - 100
            fraction = difference / sum
            self.infection_rate = self.infection_rate - (self.infection_rate * fraction)
            self.recovery_rate = self.recovery_rate - (self.recovery_rate * fraction)
            self.death_rate = self.death_rate - (self.death_rate * fraction)
        else:
            pass

    def file_write(self):

        """Writes total amount of people in each list when called. Is called every day of pandemic."""

        states = [self.susceptible, self.infected, self.recovered, self.dead]
        i = 0
        for filename in self.files:
            file = open(self.temp + filename, 'a')
            file.write(str(states[i][-1]))
            file.write('\n')
            i = i + 1

    def file_clear(self):

        """Clears all files when program restarted."""

        for filename in self.files:
            file = open(self.temp + filename, 'r+')
            file.truncate(0)

class Animation(Pandemic):

    def __init__(self):

        """Defines all parameters needed to draw graph axis and opens all temp files containing data about the days
        list totals."""

        super().__init__()
        self.ys, self.xs, self.yi, self.xi, self.yr, self.xr, self.yd, self.xd = ([] for i in range(8))
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.day - 1)
        self.ax.set_ylim(0, self.start_susceptible + self.start_infected)
        self.ax.set_ylabel("People")
        self.ax.set_xlabel("time (days)")
        self.ax.set_title('Pandemic')
        self.lns, = self.ax.plot(0, self.start_susceptible, color='green', label='Susceptible')
        self.lni, = self.ax.plot(0, self.start_infected, color='red', label='Infected')
        self.lnr, = self.ax.plot(0, 0, color='blue', label='Recovered')
        self.lnd, = self.ax.plot(0, 0, color='grey', label='Dead')
        self.ax.legend(loc='upper right')

        with open(self.temp + 'susceptible.txt') as s:
            self.susceptible = s.readlines()
        with open(self.temp + 'infected.txt') as i:
            self.infected = i.readlines()
        with open(self.temp + 'recovered.txt') as r:
            self.recovered = r.readlines()
        with open(self.temp + 'dead.txt') as d:
            self.dead = d.readlines()

    def animation_frame(self, i):

        """Adds new point to all 4 lines when called and returns the new lines.

        ys/xs - total people susceptible
        yi/xi - total people infected
        yr/xr - total people recovered
        yd/xd - total people dead
        """

        while True:
            while i <= self.day - 1:
                self.ys.append(int(self.susceptible[i]))
                self.xs.append(i)
                self.lns.set_xdata(self.xs)
                self.lns.set_ydata(self.ys)

                self.yi.append(int(self.infected[i]))
                self.xi.append(i)
                self.lni.set_xdata(self.xi)
                self.lni.set_ydata(self.yi)

                self.yr.append(int(self.recovered[i]))
                self.xr.append(i)
                self.lnr.set_xdata(self.xr)
                self.lnr.set_ydata(self.yr)

                self.yd.append(int(self.dead[i]))
                self.xd.append(i)
                self.lnd.set_xdata(self.xd)
                self.lnd.set_ydata(self.yd)

                return self.lns, self.lni, self.lnr, self.lnd,
            self.animation.event_source.stop()
            break

    def func_animation(self):

        """Uses matplotlib.animation to create an animated line plot."""

        self.animation = ani.FuncAnimation(self.fig, func=self.animation_frame,
                                           frames=np.arange(0, self.day + 1, 1), interval=100)
        plt.show()

if __name__ == "__main__":
    Animation().func_animation()

