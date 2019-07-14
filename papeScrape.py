#!/usr/bin/python3

from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import distutils.util
import urllib
import json
import re
import os

boardList = [] #[wg, "Wallpapers/General", "URL"]
threadList = [] #[534341, "Space papes", "URL"]

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

    threadList[threadSelection][1] += threadList[threadSelection][0] if threadList[threadSelection][1] == "No subject" else threadList[threadSelection][1]
    newdir = os.getcwd()+"/"+boardList[boardSelection][0]+"/"+re.sub('[^A-Za-z0-9]+', '', threadList[threadSelection][1])+"/"

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
        print("\nCreated directory "+newdir+" successfully")
        textFile = open(newdir+"op.txt", "w"); textFile.write(soup.find("blockquote", {"class": "postMessage"}).text); textFile.close()  
        print("\nSaved OP message as "+newdir+"op.txt\n")

        for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
            urllib.request.urlretrieve("http:"+a["href"], newdir+a["href"][19:])
            print("Downloaded "+a["href"][19:])

        print("\nAll images downloaded.")
        print("\nExiting papeScrape...\n")


nsfw = nsfwFilter()
board = scrapeBoards(nsfw)
thread = scrapeThreads(board)
scrapeImages(board, thread)