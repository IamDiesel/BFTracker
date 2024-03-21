#Last Edit 07.08.19 02:09
from datetime import date

class Gamereport(object):
    def __init__(self, timestamp,playername, score, scorePerMin, kills, deaths, kd, gameMode, url):
        self.timestamp = timestamp
        self.score = int(score.replace(',',''))
        self.scorePerMin = float(scorePerMin)
        self.kills = int(kills)
        self.deaths = int(deaths)
        self.kd = float(kd)
        self.gameMode = gameMode
        self.playername = playername
        self.url = url

    def __init__(self, lineArray):
        if(len(lineArray) >= 8):
            self.timestamp = lineArray[0]
            self.playername = lineArray[1]
            self.score = int(lineArray[2].replace(',',''))
            self.scorePerMin = float(lineArray[3].replace(',',''))
            self.kd = float(lineArray[4])
            self.kills = int(lineArray[5])
            self.deaths = int(lineArray[6])
            self.gameMode = lineArray[7]
            self.url = lineArray[8]
        else:
            print("Array out of bounds, while initializing gamereport. Length is " + str(len(lineArray)) + " but should be 7.")
    def toCSV(self, sep=";"):
        res = self.timestamp + ";" + self.playername + ";" + str(self.score) + ";" + f"{self.scorePerMin:.2f}" + ";" + f"{self.kd:.2f}" + ";" + str(self.kills) + ";" + str(self.deaths) + ";"  + self.gameMode + ";" + self.url + "\n"
        return res

    def isOwnGameNewer(self, other):
        a = self.getTimePower()
        b = other.getTimePower()
        #print(str(self) + " ? " + str(other))
        if(a > b):
            return 1
        if(a < b):
            return -1
        if(a==b):
            return 0

    def getTimePower(self):
        result = 0
        firstPart, secondPart = self.timestamp.split(" @ ")
        month, day, year = firstPart.split("/")
        thirdPart, fourthPart = secondPart.split(" ")
        hours, minutes = thirdPart.split(":")
        minutesFactor = 0
        #print(fourthPart)
        if(fourthPart == "PM"):
            minutesFactor = 60*12;
        minutesOverall = int(hours) * 60 + int(minutes) + minutesFactor
        tmp = int(year + month + day) * 10000 + minutesOverall
        tmpStr = str(tmp)

        return int(tmpStr)

    def getRealTimestamp(self):
        firstPart, secondPart = self.timestamp.split(" @ ")
        month, day, year = firstPart.split("/")
        return day + "." + month + " " + year + " " + secondPart

    def toDatetime(self):
        firstPart, secondPart = self.timestamp.split(" @ ")
        month, day, year = firstPart.split("/")
        year = "20" + year
        return date(int(year), int(month), int(day))



    @staticmethod
    def transformTimestampToReadable(timestamp):
        firstPart, secondPart = timestamp.split(" @ ")
        month, day, year = firstPart.split("/")
        return day + "." + month + ".20" + year + "@" + secondPart



    def __ne__(self, other): #!=
        a = self.getTimePower()
        b = other.getTimePower()
        if(a != b):
            return 1
        return 0

    def __eq__(self, other):
        if(self.isOwnGameNewer(other) == 0):
            return 1
        return 0

    def __ge__(self, other): #>=
        if(self.isOwnGameNewer(other) == 1 or self.isOwnGameNewer(other) == 0):
            return 1
        return 0

    def __le__(self, other): #<=
        if(self.isOwnGameNewer(other) == -1 or self.isOwnGameNewer(other) == 0):
            return 1
        return 0

    def __gt__(self, other): #>
        if(self.isOwnGameNewer(other) == 1):
            return 1
        return 0

    def __lt__(self, other): #<
        if(self.isOwnGameNewer(other) == -1):
            return 1
        return 0

    def __str__(self):
        res = "Gamereport\n"
        res += "Timestamp: " + str(self.timestamp) + "\n"
        res += "Playername: " + str(self.playername) + "\n"
        res += "score: " + str(self.score) + "\n"
        res += "score/min: " + str(self.scorePerMin) + "\n"
        res += "K/D: " + str(self.kd) + "\n"
        res += "Kills: " + str(self.kills) + "\n"
        res += "deaths: " + str(self.deaths) + "\n"
        res += "Game-Mode: " + str(self.gameMode) + "\n"
        res += "URL: " + str(self.url) + "\n"
        return res

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return self.isOwnGameNewer(other)


    def getTimestamp(self):
        return self.timestamp
    def getScore(self):
        return self.score
    def getScorePerMin(self):
        return self.scorePerMin
    def getKills(self):
        return self.kills
    def getDeaths(self):
        return self.deaths
    def getGameMode(self):
        return self.gameMode
    def getCalcKD(self):
        return self.kills / self.deaths
    def getPlayername(self):
        return self.playername
    def getURL(self):
        return self.url

