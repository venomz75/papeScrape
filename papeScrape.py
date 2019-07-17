#!/usr/bin/python3
from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import distutils.util
import threading
import urllib
import json
import re
import os

boardList = [] #[wg, "Wallpapers/General", "URL"]
threadList = [] #[534341, "Space papes", "URL"]
currentJobs = [] #[process, [wg, "Wallpapers/General", "URL"],[534341, "Space papes", "URL"]]
command = ""

def addJob():
    board = scrapeBoards(nsfw)
    thread = scrapeThreads(board)
    images = scrapeImages(board, thread) 
    downloadProcess = threading.Thread(target=downloadImages, args=(images,), daemon=True) 
    downloadProcess.start()
    job = [downloadProcess,boardList[board],threadList[thread]]
    boardList.clear(); threadList.clear()
    currentJobs.append(job)
    monitorProcess = threading.Thread(target=monitorJob, args=(job,), daemon=True)
    monitorProcess.start()

def monitorJob(job):
    while job[0].is_alive():
        pass
    currentJobs.remove(job)

def listJobs():
    for i in range(len(currentJobs)):
        print("/"+currentJobs[i][1][0]+"/"+currentJobs[i][2][0]+": "+currentJobs[i][2][1])

def linkToSoup(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

def nsfwFilter():
    nsfwSelection = distutils.util.strtobool(input("\nShow NSFW boards? (y/n): ")); print(" ")
    return nsfwSelection

def scrapeBoards(nsfwSelection):
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
        boardList.append([boardTags[i],boardNames[i],boardLinks[i]])
        boardList.sort(key=lambda x:x[0])

    if not nsfwSelection:
        for i in reversed(range(len(boardList))):
            if "4channel" not in boardList[i][2]:
                del(boardList[i])

    for i in range(len(boardList)):
        print("/"+boardList[i][0]+"/ "+(" "*(4-len(boardList[i][0])))+boardList[i][1])
    tagSelection = input("\nChoose your board: ")

    i=0
    while boardList[i][0] != tagSelection:
        i += 1
    print("\nParsing /"+boardList[i][0]+"/, please wait...\n") 
    boardSelection = i    
    return int(boardSelection)
    
def scrapeThreads(boardSelection):
    threadLinks = []; threadSubjects = []; threadNumbers = [] 
    for i in range(11):
        soup = linkToSoup("http:"+boardList[boardSelection][2]+str(i))
        for div in soup.find_all("div", {"class": "thread"}):
            threadNumbers.append(div["id"][1:])
            threadLinks.append("http:"+boardList[boardSelection][2]+"thread/"+div["id"][1:])
        for div in soup.find_all("div", {"class": "postInfo desktop"}):
            for span in div.find_all("span", {"class": "subject"}):
                if not span.text:
                    threadSubjects.append("No subject")
                else:
                    threadSubjects.append(span.text)

    for i in range(len(threadLinks)):
        threadList.append([threadNumbers[i],threadSubjects[i],threadLinks[i]])
        threadList.sort(key=lambda x:x[0])

    for i in range(len(threadList)):
        print (str(i).zfill(3)+") "+threadList[i][0]+" - "+threadList[i][1])

    threadSelection = input("\nChoose your thread: ")
    return int(threadSelection)

def scrapeImages(boardSelection, threadSelection):
    try:
        threadSelection = int(threadSelection)
    except ValueError:
        print("\nInvalid input!")
    else:
        if threadSelection > 149 or threadSelection < 0:
            print("\nInvalid input!")
        else:
            print("\nDownloading images from thread #"+threadList[threadSelection][0]+" on /"+boardList[boardSelection][0]+"/, please wait...")
    
    soup = linkToSoup(threadList[threadSelection][2])

    filename = threadList[threadSelection][1]+threadList[threadSelection][0] if threadList[threadSelection][1] == "No subject" else threadList[threadSelection][1]
    newdir = os.getcwd()+"/"+boardList[boardSelection][0]+"/"+re.sub('[^A-Za-z0-9]+', '', filename+"/")
    print(newdir)

    try:
        if os.path.isdir(os.getcwd()+"/"+boardList[boardSelection][0]):
            os.mkdir(newdir)  
        else:
            os.mkdir(boardList[boardSelection][0])
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
    for i in range(len(imageList)):
        urllib.request.urlretrieve(imageList[i][0], imageList[i][1])

nsfw = False
print("""
                           _____                          
    ____  ____ _____  ___ / ___/______________ _____  ___ 
   / __ \/ __ `/ __ \/ _ \\\\__ \/ ___/ ___/ __ `/ __ \/ _ \\
  / /_/ / /_/ / /_/ /  __/__/ / /__/ /  / /_/ / /_/ /  __/
 / .___/\__,_/ .___/\___/____/\___/_/   \__,_/ .___/\___/ 
/_/         /_/                             /_/           
                    Written by Adam Gibbs

Use "help" for a list of commands along with their function.""")
while command != "exit":
    command = input("\nAwaiting command:")

    if command == "add":
        addJob()
    
    if command == "list":
        listJobs()

    if command == "nsfw":
        nsfw = nsfwFilter()

    if command == "help":
        print("\nadd: Start a new thread download\nlist: Lists current jobs\nnsfw: Prompts user to enable or disable the NSFW filter\nhelp: Lists commands and their functions\nexit: Quits the application(downloads in progress will be stopped)")