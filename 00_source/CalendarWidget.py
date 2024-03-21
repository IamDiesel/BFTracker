from tkinter import *
from datetime import date
from datetime import datetime
from calendar import *

class DateCalendar(Frame):
    def __init__(self, master, titleText, height, width):
        Frame.__init__(self, master, height=height, width=width)
        self.grid()
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.buttons = list()
        self.title = titleText
        self.create_widgets()

    def buttonClick(self, btn):
        self.day = int(btn.cget('text'))
        for somebutton in self.buttons:
            somebutton.config(bg='grey')
        btn.config(bg='yellow')
    def yearButtonDecrease(self):
        if(self.year > 2017):
            self.year -=1
            #self.labelYear.configure(text=str(self.year))
            self.create_widgets()
    def yearButtonIncrease(self):
        if(self.year < 3000):
            self.year +=1
            #self.labelYear.configure(text=str(self.year))
            self.create_widgets()

    def monthButtonDecrease(self):
        if(self.month == 1):
            self.month = 12
        else:
            self.month -= 1
        self.create_widgets()
    def monthButtonIncrease(self):
        if(self.month == 12):
            self.month = 1
        else:
            self.month += 1
        self.create_widgets()

    def getDate(self):
        return date(self.year, self.month, self.day)

    def create_widgets(self):
        for button in self.buttons:
            button.grid_forget()
        Label(self, text=self.title).grid(row=0, column = 0, columnspan = 7)
        Button(self, text=" < ", command=self.yearButtonDecrease).grid(row=1, column=0, columnspan = 2)
        Button(self, text=" > ", command=self.yearButtonIncrease).grid(row=1, column=6, columnspan = 2)
        Button(self, text=" < ", command=self.monthButtonDecrease).grid(row=2, column=0, columnspan = 2)
        Button(self, text=" > ", command=self.monthButtonIncrease).grid(row=2, column=6, columnspan = 2)
        Label(self, text=str(self.year)).grid(row=1, column=2, columnspan=3)
        Label(self, text=str(self.month)).grid(row = 2, column = 2, columnspan=3)
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        #create labels
        for i in range(7):
            label = Label(self, text=days[i])
            label.grid(row = 3, column = i)

        weekday, numDays = monthrange(self.year, self.month)
        week = 1+3
        for i in range(1, numDays + 1):
            button = Button(self, text = str(i),width = 3)
            button.configure(command=lambda btn=button:self.buttonClick(btn))
            if(i == self.day):
                button.configure(bg='yellow')
            else:
                button.configure(bg='grey')
            button.grid(row = week, column = weekday,sticky='N')
            self.buttons.append(button)

            weekday += 1
            if weekday > 6:
                week += 1
                weekday = 0

        while week < 9:
            week +=1
            invisibleBtn = Button(self, text=" \n",borderwidth=0, relief='flat')
            invisibleBtn.grid(row = week, column = 0,sticky='N')

