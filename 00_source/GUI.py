#Last Edit 30.07.19 02:09
import tkinter as tk
from tkinter.scrolledtext import *
import plotHelper
import Battlefieldtracker
import PlayerF
import sys
import threading

import queue
from CalendarWidget import DateCalendar


class IORedirector(object):
    def __init__(self, text, root):
        self.text = text
    def write(self, s):
        #self.data.append(s)
        self.text.insert('end',s)
        self.text.see(tk.END)
    def flush(self):
        sys.stdout = sys.__stdout__
    def clear(self):
        self.text.delete('1.0', tk.END)

def closeEvent(self, event):
    sys.stdout = sys.__stdout__



gameModeChoices = ["All", "Team Deathmatch", "Conquest", "Squad Conquest","Rush","Frontlines (Medium)","Frontlines (Small)","Breakthrough", "Final Stand","Airborne","Domination"]
plotChoices = ["K/D", "scorePerMin", "Kills", "Deaths"]



def main():
    threadQueue = queue.Queue()
    guiQueue = queue.Queue()
    mainApp = MainApp(threadQueue,guiQueue)
    mainApp.mainloop()




class MainApp(tk.Tk):
    def __init__(self, thread_queue, gui_queue):
    ####### Do something ######
        super(MainApp,self).__init__()
        self.thread_queue = thread_queue
        self.gui_queue = gui_queue
        #self.myframe = Frame(self)
        #self.myframe.grid(row=0, column=0, sticky='nswe')
        #self.mylabel = Label(self.myframe) # Element to be updated
        #self.mylabel.config(text='No message')
        #self.mylabel.grid(row=0, column=0)
        #self.mybutton = Button(self.myframe, text='Change message', command=self.startThread)
        #self.mybutton.grid(row=1, column=0)

        self.title("BFV Stats")

        tk.Label(self, text="PlayerA").grid(row=0)
        tk.Label(self, text="PlayerB").grid(row=1)
        tk.Label(self, text="Amount Gamereports").grid(row=4, column=0)
        tk.Label(self, text="Game-Mode: ").grid(row=5, column=0)
        tk.Label(self, text="Plottype: ").grid(row=6, column=0)

        self.entryNameA = tk.Entry(self)
        self.entryNameB = tk.Entry(self)
        self.entryAmountGR = tk.Entry(self)
        self.entryNameA.insert(10, "DauerfeuerDetlef")
        self.entryNameB.insert(10, "Wuschel-Walter")
        self.entryAmountGR.insert(10, "1000")
        self.consoleFrame = tk.Frame()
        self.consoleText = ScrolledText(self.consoleFrame, height=20, width=200)
        self.consoleText.pack(side=tk.LEFT)
        self.consoleFrame.grid(row=8, column=0, columnspan=16, rowspan=2, sticky=tk.E + tk.W + tk.S + tk.N)

        self.tkvarGamemode = tk.StringVar(self)
        self.tkvarGamemode.set(gameModeChoices[0])  # set the default option
        self.popupMenuGamemode = tk.OptionMenu(self, self.tkvarGamemode, *gameModeChoices)
        self.popupMenuGamemode.config(width=20)
        self.popupMenuGamemode.grid(row=5, column=1, sticky="ew")
        self.tkvarPlottype = tk.StringVar(self)
        self.tkvarPlottype.set(plotChoices[0])  # set the default option
        self.popupMenuPlottype = tk.OptionMenu(self, self.tkvarPlottype, *plotChoices)
        self.popupMenuPlottype.config(width=20)
        self.popupMenuPlottype.grid(row=6, column=1, sticky="ew")

        self.entryNameA.grid(row=0, column=1, sticky="ew")
        self.entryNameB.grid(row=1, column=1, sticky="ew")
        self.entryAmountGR.grid(row=4, column=1, sticky="ew")

        self.calendarFrom = DateCalendar(self, "Plot Gamereports From:", height=500, width=300)
        self.calendarFrom.grid(row=2, column=4, columnspan=3, rowspan=6)
        self.calendarTo = DateCalendar(self, "Plot Gamereports To:", height=500, width=300)
        self.calendarTo.grid(row=2, column=9, columnspan=3, rowspan=6)

        self.bigUpdateAButton = tk.Button(self, text='Big Update A', command=threading.Thread(target=self.updatePlayerA).start)
        self.bigUpdateAButton.grid(row=0, column=2,sticky=tk.W, pady=4)
        self.bigUpdateBButton = tk.Button(self, text='Big Update B', command=threading.Thread(target=self.updatePlayerB).start)
        self.bigUpdateBButton.grid(row=1, column=2,sticky=tk.W, pady=4)
        self.smallUpdateAButton = tk.Button(self, text='Small Update A', command=self.smallUpdatePlayerA)
        self.smallUpdateAButton.grid(row=0,column=3,sticky=tk.W,pady=4)
        self.smallUpdateBButton = tk.Button(self, text='Small Update B', command=threading.Thread(target=self.smallUpdatePlayerB).start)
        self.smallUpdateBButton.grid(row=1,column=3,sticky=tk.W,pady=4)
        tk.Button(self, text='Plot Both Players', command=self.comparePlayers).grid(row=7, column=2, sticky=tk.W, pady=4)
        tk.Button(self, text='Plot PlayerA', command=self.plotPlayerKDA).grid(row=7, column=0, sticky=tk.W, pady=4, padx=4)
        tk.Button(self, text='Plot PlayerB', command=self.plotPlayerKDB).grid(row=7, column=1, sticky=tk.W, pady=4)
        tk.Button(self, text="Clear Console", command=self.clearConsole).grid(row=11, column=0, sticky=tk.W, pady=4, padx=4)

        # redirect stdout to Console in GUI
        # to restore stdout use: sys.stdout = sys.__stdout__
        self.redirectHandler = IORedirector(self.consoleText, self)
        sys.stdout = self.redirectHandler

    def activateUpdateButtons(self):
        self.bigUpdateAButton.configure(state=tk.NORMAL)
        self.bigUpdateBButton.configure(state=tk.NORMAL)
        self.smallUpdateAButton.configure(state=tk.NORMAL)
        self.smallUpdateBButton.configure(state=tk.NORMAL)
    def deactivateUpdateButtons(self):
        self.bigUpdateAButton.configure(state=tk.DISABLED)
        self.bigUpdateBButton.configure(state=tk.DISABLED)
        self.smallUpdateAButton.configure(state=tk.DISABLED)
        self.smallUpdateBButton.configure(state=tk.DISABLED)

    def startThread(self):
    #Spawn a new thread for running long loops in background
        self.mylabel.config(text='Running loop')
        self.mybutton["state"] = tk.DISABLED
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.plotPlayerKDA())
        self.new_thread.start()
        self.after(100, self.listen_for_result)

    def listen_for_result(self):
        #Check if there is something in the queue
        try:
            res = self.gui_queue.get(0)
            #self.mylabel.config(text='Loop terminated:'+str(res))
            print("Finished Update Task.")
            self.activateUpdateButtons()
        except queue.Empty:
            self.after(1000, self.listen_for_result)

    def plotPlayerKDA(self):
        plotHelper.plotPlayer(PlayerF.Player(self.entryNameA.get()), self.tkvarGamemode.get(), int(eval(self.entryAmountGR.get())),self.tkvarPlottype.get(), dateFrom=self.calendarFrom.getDate(), dateTo=self.calendarTo.getDate())

    def plotPlayerKDB(self):
        plotHelper.plotPlayer(PlayerF.Player(self.entryNameB.get()), self.tkvarGamemode.get(), int(eval(self.entryAmountGR.get())),self.tkvarPlottype.get(), dateFrom=self.calendarFrom.getDate(), dateTo=self.calendarTo.getDate())
    def comparePlayers(self):
        plotHelper.plotComparePlayers(PlayerF.Player(self.entryNameA.get()), PlayerF.Player(self.entryNameB.get()), int(eval(self.entryAmountGR.get())), self.tkvarPlottype.get(), self.tkvarGamemode.get(), dateFrom=self.calendarFrom.getDate(), dateTo=self.calendarTo.getDate())

    def updatePlayerA(self):
        self.deactivateUpdateButtons()
        playerRef = [PlayerF.Player(self.entryNameA.get())]
        self.new_thread = threading.Thread(target=Battlefieldtracker.onlineUpdatePlayer, kwargs={'playerRef':playerRef,'amountScrollDowns':100,'breakWhenReportIsInList':0,'gui_queue':self.gui_queue})
        self.new_thread.start()
        self.after(1000, self.listen_for_result())
        #Battlefieldtracker.onlineUpdatePlayer([PlayerF.Player(self.entryNameA.get())], 20, 0)
    def smallUpdatePlayerA(self):
        self.deactivateUpdateButtons()
        playerRef = [PlayerF.Player(self.entryNameA.get())]
        self.new_thread = threading.Thread(target=Battlefieldtracker.onlineUpdatePlayer, kwargs={'playerRef':playerRef,'amountScrollDowns':1,'breakWhenReportIsInList':1,'gui_queue':self.gui_queue})
        self.new_thread.start()
        self.after(1000, self.listen_for_result())
        #.onlineUpdatePlayer([PlayerF.Player(self.entryNameA.get())], 1, 1)
    #TODO amount scrolldowns changed from 30 to 100--> auto detection of page end
    def updatePlayerB(self):
        self.deactivateUpdateButtons()
        playerRef = [PlayerF.Player(self.entryNameB.get())]
        self.new_thread = threading.Thread(target=Battlefieldtracker.onlineUpdatePlayer, kwargs={'playerRef':playerRef,'amountScrollDowns':100,'breakWhenReportIsInList':0,'gui_queue':self.gui_queue})
        self.new_thread.start()
        self.after(1000, self.listen_for_result())
        #Battlefieldtracker.onlineUpdatePlayer([PlayerF.Player(self.entryNameB.get())], 20, 0)

    def smallUpdatePlayerB(self):
        self.deactivateUpdateButtons()
        playerRef = [PlayerF.Player(self.entryNameB.get())]
        self.new_thread = threading.Thread(target=Battlefieldtracker.onlineUpdatePlayer, kwargs={'playerRef':playerRef,'amountScrollDowns':1,'breakWhenReportIsInList':1,'gui_queue':self.gui_queue})
        self.new_thread.start()
        self.after(1000, self.listen_for_result())
        #Battlefieldtracker.onlineUpdatePlayer([PlayerF.Player(self.entryNameB.get())], 1, 1)

    def clearConsole(self):
        self.redirectHandler.clear()

