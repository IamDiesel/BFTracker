#Last Edit 29.07.19 02:09
import PlayerF
import plotHelper
import Battlefieldtracker
import GamereportF
import GUI
import os

gamereportC = GamereportF.Gamereport(["07/26/19 @ 7:42 PM","Baserape-Bob","0","0.00","0.00","1","1","Team Deathmatch","https://battlefieldtracker.com/bfv/gamereport/origin/1157659636916525248?handle=Baserape-Bob"])
gamereportB = GamereportF.Gamereport(["07/26/19 @ 7:57 PM","Baserape-Bob","0","0.00","0.00","1","1","Team Deathmatch","https://battlefieldtracker.com/bfv/gamereport/origin/1157655734125041856?handle=Baserape-Bob"])
# gamereportA = GamereportF.Gamereport(["07/26/19 @ 8:12 PM","Baserape-Bob","0","0.00","0.00","1","1","Team Deathmatch"])
#
# bob = PlayerF.Player("Baserape-Bob")
# print("hello")
# print(bob.isGamereportLinkAlreadyInList(gamereportC.getURL()))
# linkList = list()
# list.append(gamereportC.getURL())
# list.append(gamereportB.getURL())
#
# print(list)
#
# if(bob.isGamereportLinkAlreadyInList(gamereportC.getURL())):
#     linkList.remove(gamereportC.getURL())
# print(linkList)

#bob.insertGamereportIfNotInList(gamereportA)
#bob.insertGamereportIfNotInList(gamereportB)
#bob.insertGamereportIfNotInList(gamereportC)
#print(bob)

#print(bob)
#plotHelper.plotPlayer(bob)
#plotHelper.plotPlayer(bob, "Team Deathmatch")
#plotHelper.plotPlayer(bob, "Team Deathmatch", 50)
#Battlefieldtracker.onlineUpdatePlayer([bob],5)
#plotHelper.plotPlayer(bob, "Team Deathmatch", 50)
#bob.savePlayerToDisk()

# dataA = ["07/28/19 @ 5:58 PM","Baserape-Bob","1","0.00","0.00","0","1","Team Deathmatch"]
# dataB= ["07/28/19 @ 5:58 PM","Baserape-Bob","0","0.00","0.00","0","1","Team Deathmatch"]
# reportA = GamereportF.Gamereport(dataA)
# reportB = GamereportF.Gamereport(dataB)
# print("test")
# print(reportA == reportB)

if __name__ == "__main__":
    #set Path for geckodriver and selenium
    os.environ['Path'] += os.pathsep + 'C:\\bin\\'
    #run GUI
    GUI.main()

