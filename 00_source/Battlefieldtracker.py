#Last Edit 05.08.19 02:09
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  TimeoutException
from selenium.common.exceptions import JavascriptException
import GamereportF
import argparse
import re
import sys
import queue


def openTabs(url, isFirstTab, driver):
    import time
    if(len(driver.window_handles) > 0 and isFirstTab == 1):
        driver.get(url)
    else:
        time.sleep(1.2)
        documentLoading = True
        while(documentLoading):
            try:
                driver.execute_script("window.open('"+url+"');")
                documentLoading = False
            except JavascriptException as exc:
                print(exc.__str__())
                documentLoading = True
                time.sleep(1.2)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

def fetchTabs(playername, driver):
    import time
    gamereportList = list()
    while(len(driver.window_handles) > 0):
        driver.switch_to.window(driver.window_handles[0])
        #time.sleep(0.3)
        #time.sleep(1)
        if(driver.current_url.casefold() != "about:blank".casefold()):
            gamereport = getGameReportDataByPlayername(driver.current_url, playername, driver,10)
            gamereportList.append(gamereport)
        if(len(driver.window_handles) > 1):
            driver.close()
        else:
            break
    return gamereportList

def getGamereportListViaTabsAndMultithreading(urlList, playername):
    import time
    MAXTABS = 15
    gamereportList = list()
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    #profile.set_preference("dom.disable_open_during_load", True)
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(firefox_options=options)

    isFirstTab = 1
    if(len(urlList) > MAXTABS):
        i = 0
        while(i <= len(urlList)):
            tmpList = urlList[i:i+MAXTABS]
            isFirstTab = 1
            #Parallel(n_jobs=0)(delayed(openTabs)(url) for url in tmpList)
            for url in tmpList:
                    openTabs(url, isFirstTab, driver)
                    isFirstTab = 0
            #time.sleep(1)
            print("Fetching (" + str(i) +"->"+str(i+MAXTABS)+ "/" + str(len(urlList))+ ")..")
            gamereportList.extend(fetchTabs(playername, driver))
            print("Fetching (" + str(i) +"->"+str(i+MAXTABS)+ "/" + str(len(urlList))+ ") finished")
            driver.close()
            driver = webdriver.Firefox(firefox_options=options)

            if(i+2*MAXTABS > len(urlList)):
                tmpList = urlList[i+MAXTABS:len(urlList)]
                isFirstTab = 1
                #Parallel(n_jobs=0)(delayed(openTabs)(url) for url in tmpList)
                for url in tmpList:
                    openTabs(url, isFirstTab, driver)
                    isFirstTab = 0
                #time.sleep(5)
                print("Fetching (" + str(i+MAXTABS) +"->"+str(len(urlList))+ "/" + str(len(urlList))+ ")..")
                gamereportList.extend(fetchTabs(playername, driver))
                print("Fetching (" + str(i+MAXTABS) +"->"+str(len(urlList))+ "/" + str(len(urlList))+ ") finished")
                break
            i += MAXTABS
    else:
        isFirstTab = 1
        #Parallel(n_jobs=0)(delayed(openTabs)(url) for url in urlList)
        for url in urlList:
            openTabs(url, isFirstTab, driver)
            isFirstTab = 0
            #time.sleep(5)
            print("Fetching (1->"+str(len(urlList))+ "/" + str(len(urlList))+ ")..")
            gamereportList.extend(fetchTabs(playername, driver))
            print("Fetching (1->"+str(len(urlList))+ "/" + str(len(urlList))+ ") finished")

    #close any remaining driver windows
    driver.stop_client()
    driver.quit()
    print("Update finished..")
    return gamereportList


def getGamereportListViaTabs(urlList, playername):
    import time
    amountTabs = 10
    gamereportList = list()
    if(len(urlList) < amountTabs):
        amountTabs = len(urlList)
    options = Options()
    options.headless = False
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(firefox_options=options)
    i = 0
    for url in urlList:
        if(i != 0):
            driver.execute_script("window.open('"+url+"');")
            #driver.get(url)
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
        else:
            driver.get(url)

        i+=1

        if((i % amountTabs == 0 and i != 0) or url == urlList[len(urlList)-1]):
            time.sleep(1)

            while(len(driver.window_handles) > 0):
                driver.switch_to.window(driver.window_handles[0])
                #time.sleep(1)
                gamereport = getGameReportDataByPlayername(driver.current_url, playername, driver,0)
                gamereportList.append(gamereport)
                if(len(driver.window_handles) > 1):
                    driver.close()
                else:
                    break

    driver.close()
    return gamereportList

def onlineUpdatePlayer(playerRef, amountScrollDowns, breakWhenReportIsInList, gui_queue): #Multithreading variant
    player = playerRef[0]
    playername = player.name
    linkList = getGamereportLinklist("https://battlefieldtracker.com/bfv/profile/origin/"+playername+"/gamereports",amountScrollDowns)
    lenBefore = len(linkList)
    for link in linkList:
        if(player.isGamereportLinkAlreadyInList(link)):
            linkList.remove(link)
    print("URL-List was reduced from "+str(lenBefore) + " to " + str(len(linkList)))
    gamereportDataList = getGamereportListViaTabsAndMultithreading(linkList, playername)

    i=0
    for gameReportData in gamereportDataList:
        i=i+1
        if(len(gameReportData)>0):
            gamereport = GamereportF.Gamereport(gameReportData)
            addResult = player.insertGamereportIfNotInList(gamereport,1)
            if(addResult >0): #if new data is not in list
                print("***************")
                print("Link " + str(i) +"/"+str(len(linkList)))
                print(gamereport)
                print("***************")
            elif(addResult == -1):
                print("***************")
                print("Gamereport skipped")
                print("***************")
            else:
                print("***************")
                print("Data of Game-Report is already in list")
                print(gamereport)
                print("***************")
                # if(breakWhenReportIsInList):
                #     break
    player.savePlayerToDisk()
    gui_queue.put(1)

#https://codereview.stackexchange.com/questions/197972/measure-website-home-page-total-network-size-in-bytes
def getSizeOfWebsiteInKBytes(driver, urlpage):
    DATA_LENGTH_REGEX = r"encodedDataLength\":(.*?),"
    totalKBytes = 0
    driver.get(urlpage)
    try:
        for entry in driver.get_log('performance'):
            entry = str(entry)
            if "Netwórk.dataReceived" in entry:
                r = re.search(DATA_LENGTH_REGEX, entry)
                totalBytes = totalKBytes + int(r.group(1)) /1000 #data size in Bytes
    except Exception:
        driver.close()
        print("Exception at receiving page size")

    return totalKBytes

#used
def getGamereportLinklist(urlpage,amountScrollDowns):
    import time
    print(urlpage)
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox()
    # get web page
    driver.get(urlpage)
    i=0

    sizeWebsite = getSizeOfWebsiteInKBytes(driver, urlpage)
    time.sleep(2)
    while (sizeWebsite - getSizeOfWebsiteInKBytes(driver, urlpage) != 0): #feature trying to identify changes in website via size in KB. When scrolling down doesnt load new content, then scrolling is finished
        #execute script to scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        #sleep for 30s
        sizeWebsite = getSizeOfWebsiteInKBytes(driver, urlpage)
        time.sleep(2)
    #todo test feature: Error while loading driver

    # while (i<amountScrollDowns):
    #     #execute script to scroll down the page
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    #     #sleep for 30s
    #     time.sleep(2)
    #     i=i+1
    # find elements by xpath
    reportLinks = driver.find_elements_by_xpath("//*[@class='reports-list']//*[contains(@class,'entries')]//*[contains(@class,'link')]")
    #print('Number of results', len(reportLinks))
    reportTimes = driver.find_elements_by_xpath("//*[@class='reports-list']//*[contains(@class,'entries')]//*[contains(@class,'time')]")
    print('Retrieving data. \n Number of results', len(reportTimes))
    data = []
    # loop over results
    i=0
    for link in reportLinks:
        #print(link.get_attribute("href"))
        #print(reportTimes[i].text)
        data.append(link.get_attribute("href"))
        i=i+1

    driver.quit()
    return data


#unused but kept
def getGameReportData(urlpage):
    import time
    # specify the url
    #urlpage = 'https://battlefieldtracker.com/bfv/gamereport/origin/1150102235045606528?handle=Baserape-Bob'
    print(urlpage)
    #Load Options
    options = Options()
    options.headless = True
    # run firefox webdriver from executable path of your choice
    driver = webdriver.Firefox(firefox_options=options)
    # get web page
    driver.get(urlpage)
    # sleep for 4s
    time.sleep(4)
    # find elements by xpath
    players = driver.find_elements_by_xpath("//*[@class='player-header']//*[contains(@class,'name')]")
    #print('Number of results', len(players))
    stats = driver.find_elements_by_xpath("//*[@class='player-header']//*[contains(@class,'stat')]")
    #print('Number of results', len(stats))
    datTime = driver.find_elements_by_xpath("//*[@class='report-info']//*[contains(@class,'time')]")
    print('Number of results', len(datTime))
    # create empty array to store data
    data = []

    data.append({datTime[0].text})
    data.append({data.append({"Name","Score","Score/Min","K/D","Kills","Deaths"})})
    #print(datTime[0].text)
    #print("Name\t\t\t\tScore\tScore/min\tK/D\tKills\tDeaths")
    # loop over results
    i=0
    for result in players:
        #print(result.text)
        data.append({result.text,stats[i].text,stats[i+1].text,stats[i+2].text,stats[i+3].text,stats[i+4].text})
        #print(result.text + "\t\t\t\t"+stats[i].text + "\t"+stats[i+1].text + "\t"+stats[i+2].text + "\t"+stats[i+3].text + "\t"+stats[i+4].text + "\t")
        i=i+5
    #close driver
    driver.quit()
    return data

#used
def getGameReportDataByPlayername(urlpage,playername,driver,sleeptime=3):
    import time
    # specify the url
    #urlpage = 'https://battlefieldtracker.com/bfv/gamereport/origin/1150102235045606528?handle=Baserape-Bob'
    print(urlpage)
    # get web page
    #driver.get(urlpage)
    # execute script to scroll down the page
    # sleep for 4s
    #time.sleep(sleeptime)
    # find elements by xpath
    stillLoading = True
    errCounter = 0
    while(stillLoading):
        try:
            elementPresent = EC.presence_of_element_located((By.XPATH, "//*[@class='player-header']//*[contains(@class,'name')]"))
            WebDriverWait(driver, sleeptime).until(elementPresent)
            stillLoading = False
        except TimeoutException:
            errCounter +=1
            print("[" + str(errCounter) +"] Timed out waiting for page to load")
            if(errCounter == 2):
                print("Trying to reload page: " + urlpage)
                driver.get(urlpage)
            if(errCounter >= 6):
                print("Skipping Gamereport: " + urlpage)
                break

    players = driver.find_elements_by_xpath("//*[@class='player-header']//*[contains(@class,'name')]")
    #print('Number of results', len(players))
    stats = driver.find_elements_by_xpath("//*[@class='player-header']//*[contains(@class,'stat')]")
    #print('Number of results', len(stats))
    reportTime = driver.find_elements_by_xpath("//*[@class='report-info']//*[contains(@class,'time')]")
    gameMode = driver.find_elements_by_xpath("//*[@class='report-info']//*[contains(@class,'mode')]")
    #print('Number of results', len(reportTime))
    # create empty array to store data
    data = list()


    #if (len(reportTime)>0):
    #    print(reportTime[0].text)
    #print("Name\t\t\t\tScore\tScore/min\tK/D\tKills\tDeaths\tmode")
    # loop over results
    i=0
    for result in players:
        #print(result.text)
        if(result.text == playername):
            #print("Player:"+str(result.text))
            data.append(reportTime[0].text)
            data.append(result.text)
            data.append(stats[i].text)
            data.append(stats[i + 1].text)
            data.append(stats[i + 2].text)
            data.append(stats[i + 3].text)
            data.append(stats[i + 4].text)
            data.append(gameMode[0].text)
            data.append(urlpage)
            #print("GameMode: " + gameMode[0].text)
            #print(result.text + "\t\t\t\t"+stats[i].text + "\t"+stats[i+1].text + "\t"+stats[i+2].text + "\t"+stats[i+3].text + "\t"+stats[i+4].text + "\t" + gameMode[0].text)
        i=i+5
    return data

