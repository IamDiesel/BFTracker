#Last Edit 29.07.19 02:09

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import GamereportF
import PlayerF
from datetime import date
from datetime import datetime

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)



def plotPlayer(player, GameMode = "All", amountGamereports=0, plotAttribute = "K/D", dateFrom=date(2000,1,1), dateTo=datetime.now()):
    killsList, deathsList, kdList, kdSingleList, datesList, scorePerMinList = player.getStats(GameMode, amountGamereports, dateFrom, dateTo)
    name = player.name
    x=np.arange(0,len(kdList),1)
    fig, ax = plt.subplots()

    if(len(datesList)> 0):
        if(plotAttribute == "K/D"):
            y2 = kdList
            y1 = kdSingleList
            ticksStart = 0
            ticksStep = 1.0
        elif(plotAttribute == "scorePerMin"):
            y1 = scorePerMinList
            ticksStart = min(y1) - (min(y1) % 50)
            ticksStep = 50.0
        elif(plotAttribute == "Kills"):
            y1 = killsList
            ticksStart = 0
            ticksStep = 5.0
        elif(plotAttribute == "Deaths"):
            y1 = deathsList
            ticksStart = 0
            ticksStep = 5.0
        sum = 0
        count = 1
        if(plotAttribute != "K/D"):
            y2 = []
            print(y1)
            for el in y1:
                sum += el
                y2.append(sum/count)
                count +=1
        y3 = np.empty(len(y2))
        y3.fill(y2[len(y2)-1])
        #y1 = deathsList
        plt.ylabel(plotAttribute)
        plt.xlabel('Gamereports: 0 = '+GamereportF.Gamereport.transformTimestampToReadable(str(datesList[0]))+"     " + str(len(datesList))+" = "+ GamereportF.Gamereport.transformTimestampToReadable(str(datesList[len(datesList)-1])))
        plt.title(plotAttribute + " " + name + " Mode="+GameMode, fontsize=20, color='gray')
        ax.plot(x,y1,'g^', label=r''+plotAttribute+" aus Gamereport")
        ax.plot(x,y2,'r',label=r''+plotAttribute+ " aufsummiert")
        ax.plot(x,y3,'r--', label=r''+plotAttribute + " AVE")
        plt.legend(loc='upper left', frameon=True)
        start, end = ax.get_ylim()
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%100.0f'))
        ax.yaxis.set_ticks(np.arange(ticksStart, end, ticksStep))
        plt.text(0.5, 0.5, plotAttribute+"="+f"{y3[len(y3)-1]:.2f}", size=18,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"),transform=ax.transAxes)
        plt.grid(True)
        plt.show(block=False)

    else:
        plt.title(plotAttribute + " " + name + " Mode="+GameMode, fontsize=20, color='gray')
        plt.text(0.5, 0.5, "No data available", size=18,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"))
        plt.show(block=False)
    #print(player)

def plotPlayerToGraph(ax, fig, x, player,colorOfGraphs='r', GameMode = "All", amountGamereports=0, plotAttribute = "K/D", dateFrom=date(2000,1,1), dateTo=datetime.now(),SinglePlayerPlot=True, dualPlayerIndex=-1,):
    killsList, deathsList, kdList, kdSingleList, datesList, scorePerMinList = player.getStats(GameMode, amountGamereports-1, dateFrom, dateTo)
    name = player.name
    if(len(datesList)> 0):
            if(plotAttribute == "K/D"):
                y2 = kdList
                y1 = kdSingleList
                ticksStart = 0
                ticksStep = 1.0
            elif(plotAttribute == "scorePerMin"):
                y1 = scorePerMinList
                ticksStart = min(y1) - (min(y1) % 50)
                ticksStep = 50.0
            elif(plotAttribute == "Kills"):
                y1 = killsList
                ticksStart = 0
                ticksStep = 5.0
            elif(plotAttribute == "Deaths"):
                y1 = deathsList
                ticksStart = 0
                ticksStep = 5.0
            sum = 0
            count = 1
            if(plotAttribute != "K/D"):
                y2 = []
                for el in y1:
                    sum += el
                    y2.append(sum/count)
                    count +=1
            y3 = np.empty(len(y2))
            y3.fill(y2[len(y2)-1])
            #y1 = deathsList
            plt.ylabel(plotAttribute)
            plt.xlabel('Gamereports: 0 = '+GamereportF.Gamereport.transformTimestampToReadable(str(datesList[0]))+"     " + str(len(datesList))+" = "+ GamereportF.Gamereport.transformTimestampToReadable(str(datesList[len(datesList)-1])))
            if(SinglePlayerPlot):
                plt.title(plotAttribute + " " + name + " Mode="+GameMode, fontsize=20, color='gray')
                ax.plot(x,y1,colorOfGraphs+'^', label=r''+name +" "+plotAttribute)
            ax.plot(x,y2,colorOfGraphs,label=r''+name+" "+plotAttribute+ " SUM")
            ax.plot(x,y3,colorOfGraphs+'--', label=r''+name+" "+plotAttribute + " AVE")
            plt.legend(loc='upper left', frameon=True)
            start, end = ax.get_ylim()
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%100.0f'))
            ax.yaxis.set_ticks(np.arange(ticksStart, end, ticksStep))
            if(SinglePlayerPlot == True):
                plt.text(0.5, 0.5, plotAttribute+"="+f"{y3[len(y3)-1]:.2f}", size=18,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"),transform=ax.transAxes)
            elif(dualPlayerIndex == 0):
                plt.text(0.5, 0.7, plotAttribute+"="+f"{y3[len(y3)-1]:.2f}", size=12,color=colorOfGraphs,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"),transform=ax.transAxes)
            elif(dualPlayerIndex == 1):
                plt.text(0.5, 0.6, "vs.", size=12,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"),transform=ax.transAxes)
                plt.text(0.5, 0.5, plotAttribute+"="+f"{y3[len(y3)-1]:.2f}", size=12,color=colorOfGraphs,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"),transform=ax.transAxes)
            plt.grid(True)
            #plt.show(block=False)
    else:
        if(SinglePlayerPlot):
            plt.title(plotAttribute + " " + name + " Mode="+GameMode, fontsize=20, color='gray')
        plt.text(0.5, 0.5, "No data available", size=18,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"))
        #plt.show(block=False)

def plotComparePlayers(playerA, playerB, amountGameReportsToCompare, plotAttribute= "K/D", GameMode = "All", dateFrom=date(2000,1,1), dateTo=datetime.now()):
    nameA = playerA.getName()
    nameB = playerB.getName()
    killsListA, deathsListA, kdListA, kdSingleListA, datesListA, scorePerMinListA = playerA.getStats(GameMode, amountGameReportsToCompare, dateFrom, dateTo)
    killsListB, deathsListB, kdListB, kdSingleListB, datesListB, scorePerMinListB = playerB.getStats(GameMode, amountGameReportsToCompare, dateFrom, dateTo)
    if(len(killsListA) < amountGameReportsToCompare):
        amountGameReportsToCompare = len(killsListA)
    if(len(killsListA) > len(killsListB)):
        amountGameReportsToCompare = len(killsListB)
    x = np.arange(0, amountGameReportsToCompare, 1)
    fig, ax = plt.subplots()

    if(amountGameReportsToCompare > 0):
        plt.ylabel(plotAttribute)
        textForXLabel = 'Gamereports:' + "\n" + '0 = ' + GamereportF.Gamereport.transformTimestampToReadable(str(datesListA[0]))  + "     "  + str(amountGameReportsToCompare) + " = "  + GamereportF.Gamereport.transformTimestampToReadable(str(datesListA[amountGameReportsToCompare - 1])) + " (" + nameA + ")" \
                        + "\n" + '0 = ' + GamereportF.Gamereport.transformTimestampToReadable(str(datesListB[0])) + "     " + str(amountGameReportsToCompare) + " = " +  GamereportF.Gamereport.transformTimestampToReadable(str(datesListB[amountGameReportsToCompare - 1]))+ " (" + nameB + ")"
        plt.xlabel(textForXLabel)
        myTitle = plt.title(plotAttribute+ "\n" + nameA +" vs. " +nameB + "\nMode="+GameMode, fontsize=20, color='gray')
        myTitle.set_y(1.0)
        fig.subplots_adjust(top=0.8,bottom=0.2)
        plotPlayerToGraph(ax,fig,x,playerA,'r',GameMode,amountGameReportsToCompare, plotAttribute,dateFrom,dateTo,False, 0)
        plotPlayerToGraph(ax,fig,x,playerB,'b',GameMode,amountGameReportsToCompare, plotAttribute,dateFrom,dateTo, False, 1)
        plt.show(block=False)
    else:
        plt.title(plotAttribute + nameA + "vs. " + nameB + " Mode="+GameMode, fontsize=20, color='gray')
        plt.text(0.5, 0.5, "No data available", size=18,va="baseline", ha="center", multialignment="center",bbox=dict(fc="none"))
        plt.show(block=False)


