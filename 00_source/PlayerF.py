#Last Edit 27.07.19 02:09
import GamereportF
import csv
from datetime import date
from datetime import datetime
import os


class Player(object):
    def __init__(self, name, filePath=""):
        self.name = name
        self.filePath = ""
        if(filePath == ""):
            self.filePath = "./../data/stats" + self.name + ".csv"
            #print(self.filePath)
            #print( os.getcwd())
        else:
            self.filePath = filePath
        self.gamereports = list()
        with open(self.filePath, 'a+') as csvFile:
            csvFile.seek(0)
            reportReader = csv.reader(csvFile, delimiter=';', quotechar='|')
            for line in reportReader:
                if(len(line)>0 and ((int(line[5]) != 0 and int(line[6])!= 0)) and line[1] == self.name):
                    self.appendGamereport(GamereportF.Gamereport(line))

    def __str__(self):
        res = "Player: " + self.name + "\n"
        res += "File: " + self.filePath  + "\n"
        i=0
        for report in self.gamereports:
            res += "*****************************\n"
            res += "#" + str(i)  + "\n"
            res += str(report)
            res += "*****************************\n"
            i+=1
        return res

    def __repr__(self):
        return self.__str__()


    def appendGamereport(self, gamereport):
        self.gamereports.append(gamereport)

    def prependGamereport(self, gamereport):#depreciated
        print(self.gamereports[0].getTimestamp() + " < " + gamereport.getTimestamp())
        if(self.gamereports[0] < gamereport):
            self.gamereports.insert(0,gamereport)
            return 1
        else:
            print("Given gamereport is older. Data was not prepended.")
            return 0

    def insertGamereportIfNotInList(self, gamereport, addZeroKillsDeathsReport):
        print("Length at beginning: " + str(len(self.gamereports)))
        if(gamereport.getKills() == 0 and gamereport.getDeaths() == 0 and addZeroKillsDeathsReport == 0):
            print("Gamereport not added since kills&deaths=0")
            return -1
        if(self.isGamereportInList(gamereport)):
            return 0
        else:
            i=len(self.gamereports) -1
            if(len(self.gamereports) == 0): #if gamereports are empty
                i=0
            else:
                while(gamereport > self.gamereports[i] and i >=0):
                    i -=1
                i +=1
            self.gamereports.insert(i,gamereport)
            print("Inserted. Length:" + str(len(self.gamereports)) + " Pos:" + str(i))
            return 1


    def isGamereportInList(self, gamereport):
        for ownGamereport in self.gamereports:
            if(ownGamereport == gamereport):
                return 1
        return 0

    def isGamereportLinkAlreadyInList(self, url):
        for report in self.gamereports:
            if(url == report.getURL()):
                return 1
        return 0


    def onlineUpdate(self, amountScrollDowns=10):
        print("Player " + self.name + " updated.")

    def savePlayerToDisk(self):
            #save data to file
        with open(self.filePath, 'a+') as f:
            f.seek(0)
            f.truncate(0)
            for report in self.gamereports:
                f.write(report.toCSV())



    def clearDiskandUpdate(self):
        amountScrollDowns = 30
        print("Player " + self.name + " cleared and updated.")

    def getStats(self, gameMode = "All", amountReports=0,dateFrom=date(2000,1,1), dateTo=datetime.now()):
        killsList = list()
        deathsList = list()
        kdList = list()
        kdSingleList = list()
        dateList = list()
        scorePerMinList = list()

        killsSum = 0
        deathsSum = 0
        kdSum = 0
        kdTemp = 1
        reportCounter = 0
        for report in self.gamereports:
            if(report.getKills() != 0 and report.getDeaths() != 0):
                reportDate = report.toDatetime()
                if((gameMode == "All" or report.getGameMode() == gameMode) and reportDate >= dateFrom and reportDate <= dateTo):
                    killsSum = killsSum + report.getKills()
                    deathsSum = deathsSum + report.getDeaths()
                    if(deathsSum > 0):
                        kdSum = (killsSum/deathsSum)
                    else:
                        kdSum = killsSum
                    if(report.getDeaths() > 0):
                        kdSingleList.append(report.getKills()/report.getDeaths())
                    else:
                        kdSingleList.append(report.getKills())
                    killsList.append(report.getKills())
                    deathsList.append(report.getDeaths())
                    kdList.append(kdSum)
                    dateList.append(report.getTimestamp())
                    scorePerMinList.append(report.getScorePerMin())
            if(amountReports > 0 and reportCounter >= amountReports):
                break
            reportCounter +=1
        return killsList, deathsList, kdList, kdSingleList, dateList, scorePerMinList

    def _getStats(self, gameMode = "All", amountReports=0):
        killsList = list()
        deathsList = list()
        kdList = list()
        kdSingleList = list()
        dateList = list()

        killsSum = 0
        deathsSum = 0
        kdSum = 0
        kdTemp = 1
        reportCounter = 0
        for report in self.gamereports:
            if(report.getKills() != 0 and report.getDeaths() != 0):
                if(gameMode == "All" or report.getGameMode() == gameMode):
                    killsSum = killsSum + report.getKills()
                    deathsSum = deathsSum + report.getDeaths()
                    if(deathsSum > 0):
                        kdSum = (killsSum/deathsSum)
                    else:
                        kdSum = killsSum
                    if(report.getDeaths() > 0):
                        kdSingleList.append(report.getKills()/report.getDeaths())
                    else:
                        kdSingleList.append(report.getKills())
                    killsList.append(killsSum)
                    deathsList.append(deathsSum)
                    kdList.append(kdSum)
                    dateList.append(report.getTimestamp())
            if(amountReports > 0 and reportCounter >= amountReports):
                break
            reportCounter +=1
        return killsList, deathsList, kdList, kdSingleList, dateList

    def getName(self):
        return self.name


