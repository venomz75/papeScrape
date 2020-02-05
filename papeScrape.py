#!/usr/bin/python3
from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import distutils.util
import threading
import urllib
import json
import re
import os

#globals
arrayBoards, arrayThreads = [], []  #primary storage of board/thread data   
cacheBoards, cacheThreads = [], []  #reserve storage of board/thread data   
currentJobs = []                    #stores daemon/board/thread data of an ongoing download job
command, tagSelection = "", ""      #user input strings

def main():    

    print("""
                               _____                          
        ____  ____ _____  ___ / ___/______________ _____  ___ 
       / __ \/ __ `/ __ \/ _ \\\\__ \/ ___/ ___/ __ `/ __ \/ _ \\
      / /_/ / /_/ / /_/ /  __/__/ / /__/ /  / /_/ / /_/ /  __/
     / .___/\__,_/ .___/\___/____/\___/_/   \__,_/ .___/\___/ 
    /_/         /_/                             /_/           

             A 4chan imagescraper written by venomz75
             
    """)
    print("Use \"help\" for a list of commands")

def addJob():
    #webscraping functions split by webpage accessed
    board = scrapeBoards(nsfw)
    thread = scrapeThreads(board)
    images = scrapeImages(board, thread) 

    #daemonises image download
    downloadProcess = threading.Thread(target=downloadImages, args=(images,), daemon=True) 
    downloadProcess.start()

    #stores all data related to the daemon and wipes primary board/thread data
    job = [downloadProcess,arrayBoards[board],arrayThreads[thread]]
    arrayBoards.clear(); arrayThreads.clear()
    currentJobs.append(job)

    #monitor daemon confirms end of download daemon
    monitorProcess = threading.Thread(target=monitorJob, args=(job,), daemon=True)
    monitorProcess.start()


def monitorJob(job):
    #waits for download daemon to finish before removing it's information from currentJobs array
    while job[0].is_alive():
        pass
    currentJobs.remove(job)


def listJobs():
    #lists download daemons currently in progress
    for i in range(len(currentJobs)):
        print("/"+currentJobs[i][1][0]+"/"+currentJobs[i][2][0]+": "+currentJobs[i][2][1])


def linkToSoup(url):
    #webscrape procedure
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup


def nsfwFilter():
    #prompts the user for their preference on nsfw content
    nsfwSelection = distutils.util.strtobool(input("\n4chan will contain mature/offensive content. Show NSFW boards? (y/n): ")); print(" ")
    return nsfwSelection


def scrapeBoards(nsfwSelection):
    #loads list of boards
    if cacheBoards:
        usecacheBoards = distutils.util.strtobool(input("\nUse existing board list? (y/n): "))

        if usecacheBoards:
            for i in range(len(cacheBoards)):
                print("/"+cacheBoards[i][0]+"/ "+(" "*(4-len(cacheBoards[i][0])))+cacheBoards[i][1])
                arrayBoards.append(cacheBoards[i])

            tagSelection = input("\nChoose your board: ")
            i=0

            while cacheBoards[i][0] != tagSelection:
                i += 1

            print("\nParsing /"+cacheBoards[i][0]+"/, please wait...\n")
            boardSelection = i    
            return int(boardSelection)
    #(re)generate board list
    cacheBoards.clear()
    soup = linkToSoup("http://www.4chan.org/")
    boardLinks = []; boardNames = []; boardTags = [] 
    for a in soup.find_all("a", {"class": "boardlink", "href": True}):
        if len(a["href"]) < 30:
            boardLinks.append(a["href"])
            slash1 = a["href"].index("/", 2) + 1; slash2 = a["href"].rindex("/")
            tag = a["href"][slash1:slash2] 
            boardTags.append(tag)

        if a.text:
            boardNames.append(a.text)

    for i in range(len(boardLinks)):
        arrayBoards.append([boardTags[i],boardNames[i],boardLinks[i]])
        arrayBoards.sort(key=lambda x:x[0])

    if not nsfwSelection:
        for i in reversed(range(len(arrayBoards))):
            if "4channel" not in arrayBoards[i][2]:
                del(arrayBoards[i])

    for i in range(len(arrayBoards)):
        print("/"+arrayBoards[i][0]+"/ "+(" "*(4-len(arrayBoards[i][0])))+arrayBoards[i][1])
        cacheBoards.append(arrayBoards[i])

    tagSelection = input("\nChoose your board: ")

    i=0
    while arrayBoards[i][0] != tagSelection:
        i += 1

    print("\nParsing /"+arrayBoards[i][0]+"/, please wait...\n") 
    boardSelection = i    
    return int(boardSelection)


def scrapeThreads(boardSelection):
    threadLinks = []; threadSubjects = []; threadNumbers = []
    #load list of threads
    if cacheThreads:
        usecacheThreads = distutils.util.strtobool(input("\nUse existing thread list? (y/n): "))
        if usecacheThreads:
            for i in range(len(cacheThreads)):
                if tagSelection in cacheThreads[i][0]:
                    print (str(i).zfill(3)+") "+cacheThreads[i][1][0]+" - "+cacheThreads[i][1][1])
                    arrayThreads.append(cacheThreads[i][1])
            threadSelection = input("\nChoose your thread: ")
            return int(threadSelection)

    #(re)generate threads
    cacheThreads.clear()
    for i in range(11):
        soup = linkToSoup("http:"+arrayBoards[boardSelection][2]+str(i))
        for div in soup.find_all("div", {"class": "thread"}):
            threadNumbers.append(div["id"][1:])
            threadLinks.append("http:"+arrayBoards[boardSelection][2]+"thread/"+div["id"][1:])
        for div in soup.find_all("div", {"class": "postInfo desktop"}):
            for span in div.find_all("span", {"class": "subject"}):
                if not span.text:
                    threadSubjects.append("No subject")
                else:
                    threadSubjects.append(span.text)

    for i in range(len(threadLinks)):
        arrayThreads.append([threadNumbers[i],threadSubjects[i],threadLinks[i]])
        arrayThreads.sort(key=lambda x:x[0])

    for i in range(len(arrayThreads)):
        print (str(i).zfill(3)+") "+arrayThreads[i][0]+" - "+arrayThreads[i][1])
        cacheThreads.append([arrayBoards[boardSelection][0],arrayThreads[i]])
    threadSelection = input("\nChoose your thread: ")
    return int(threadSelection)


def scrapeImages(boardSelection, threadSelection):
    #store image data in array
    try:
        threadSelection = int(threadSelection)
    except ValueError:
        print("\nInvalid input!")
    else:
        if threadSelection > 149 or threadSelection < 0:
            print("\nInvalid input!")
        else:
            print("\nDownloading images from thread #"+arrayThreads[threadSelection][0]+" on /"+arrayBoards[boardSelection][0]+"/, please wait...")
    
    soup = linkToSoup(arrayThreads[threadSelection][2])

    filename = arrayThreads[threadSelection][1]+arrayThreads[threadSelection][0] if arrayThreads[threadSelection][1] == "No subject" else arrayThreads[threadSelection][1]
    newdir = os.getcwd()+"/"+arrayBoards[boardSelection][0]+"/"+re.sub('[^A-Za-z0-9]+', '', filename+"/")

    try:
        if os.path.isdir(os.getcwd()+"/"+arrayBoards[boardSelection][0]):
            os.mkdir(newdir)  
        else:
            os.mkdir(arrayBoards[boardSelection][0])
            os.mkdir(newdir)
    except OSError:
        print("\nFailed to create directory "+newdir)
        print("\nExiting papeScrape...\n")
    else:
        print("\nCreated directory "+newdir+" successfully, downloading images...")
        textFile = open(newdir+"/op.txt", "w"); textFile.write(soup.find("blockquote", {"class": "postMessage"}).text); textFile.close()  

        imageList = []
        for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
            slash = a["href"].rindex("/")
            url = "http:"+a["href"] 
            filepath = newdir+a["href"][slash:]
            imageList.append([url, filepath])

        return imageList


def downloadImages(imageList):
    #download images in image array
    for i in range(len(imageList)):
        urllib.request.urlretrieve(imageList[i][0], imageList[i][1])


#entry point
print("""
                           _____                          
    ____  ____ _____  ___ / ___/______________ _____  ___ 
   / __ \/ __ `/ __ \/ _ \\\\__ \/ ___/ ___/ __ `/ __ \/ _ \\
  / /_/ / /_/ / /_/ /  __/__/ / /__/ /  / /_/ / /_/ /  __/
 / .___/\__,_/ .___/\___/____/\___/_/   \__,_/ .___/\___/ 
/_/         /_/                             /_/           

         A 4chan imagescraper written by venomz75
             
""")
print("Use \"help\" for a list of commands")

nsfw = nsfwFilter()
while command != "exit":
    command = input("\nAwaiting command:")

    if command == "add":
        addJob()
        
    if command == "jobs":
        listJobs()

    if command == "nsfw":
        nsfw = nsfwFilter()

    if command == "help":
        print("\nbrowse: Choose a thread to scrape by selecting a board and thread\nadd: Manually paste a thread URL without browsing boards and threads\njobs: Lists current jobs\nnsfw: Prompts user to enable or disable the NSFW filter\nhelp: Returns this menu\nexit: Quits the application(downloads in progress will be stopped)")


