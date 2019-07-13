#!/usr/bin/python3

from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import distutils.util
import urllib
import json
import re
import os

boardTotal = []
boardLinks = []
boardNames = []
boardTags = []
threadLinks = []
threadSubjects = []
threadNumbers = []

def nsfwFilter():
    nsfwSelection = distutils.util.strtobool(input("\nShow NSFW boards? (y/n)"))
    return nsfwSelection

def scrapeBoards(nsfwSelection):
    data = requests.get("http://www.4chan.org/")
    soup = BeautifulSoup(data.text, 'html.parser')

    for a in soup.find_all("a", {"class": "boardlink", "href": True}):
        if len(a["href"]) < 30:
            boardLinks.append(a["href"])
            tag = a["href"][7:]
            boardIndex = tag.index("/")
            tag = tag[boardIndex+1:]
            boardIndex = tag.index("/")
            tag = tag[0:boardIndex]
            boardTags.append(tag)
        if a.text:
            boardNames.append(a.text)

    for i in range(len(boardLinks)):
        boardTotal.append([boardTags[i],boardNames[i],boardLinks[i]])
        boardTotal.sort(key=lambda x:x[0])

    if not nsfwSelection:
        for i in reversed(range(len(boardTotal))):
            if "4channel" not in boardTotal[i][2]:
                del(boardTotal[i])

    for i in range(len(boardTotal)):
        print(str(i).zfill(2)+" /"+boardTotal[i][0]+"/ "+(" "*(4-len(boardTotal[i][0])))+boardTotal[i][1])
    boardSelection = input("\nChoose your board: ")
    boardSelection = int(boardSelection)
    return boardSelection 

def scrapeThreads(boardSelection):
    try:
        boardSelection = int(boardSelection)
    except ValueError:
        print("\nInvalid input!")
    else:
        if boardSelection > 69 or boardSelection < 0:
            print("\nInvalid input!")
        else:
            print("\nParsing /"+boardTags[boardSelection]+"/, please wait...\n")    

    for i in range(11):
        data = requests.get("http:"+boardLinks[boardSelection]+str(i))
        soup = BeautifulSoup(data.text, 'html.parser')
        for div in soup.find_all("div", {"class": "thread"}):
            threadNumbers.append(div["id"][1:])
        for div in soup.find_all("div", {"class": "postInfo desktop"}):
            for span in div.find_all("span", {"class": "subject"}):
                if not span.text:
                    threadSubjects.append("No subject")
                else:
                    threadSubjects.append(span.text)

    for i in range(len(threadSubjects)):
        threadLinks.append("http:"+boardLinks[boardSelection]+"thread/"+threadNumbers[i])
        print (str(i)+") "+threadNumbers[i]+" - "+threadSubjects[i])

    threadSelection = input("\nChoose your thread: ")
    threadSelection = int(threadSelection)
    return threadSelection



def scrapeImages(boardSelection, threadSelection):
    try:
        threadSelection = int(threadSelection)
    except ValueError:
        print("\nInvalid input!")
    else:
        if threadSelection > 149 or threadSelection < 0:
            print("\nInvalid input!")
        else:
            print("\nDownloading images from thread #"+threadNumbers[threadSelection]+" on /"+boardTags[boardSelection]+"/, please wait...")
    
    data = requests.get(threadLinks[threadSelection])
    soup = BeautifulSoup(data.text, 'html.parser')
    filepath = os.getcwd()

    if threadSubjects[threadSelection] == "No subject":
        threadSubjects[threadSelection] = threadSubjects[threadSelection]+threadNumbers[threadSelection]
    threadSubjects[threadSelection] = re.sub('[^A-Za-z0-9]+', '', threadSubjects[threadSelection])
    newdir = filepath+"/"+boardTags[boardSelection]+"/"+threadSubjects[threadSelection]+"/"

    try:
        if os.path.isdir(filepath+"/"+boardTags[boardSelection]):
            os.mkdir(newdir)  
        else:
            os.mkdir(boardTags[boardSelection])
            os.mkdir(newdir)
    except OSError:
        print("\nFailed to create directory "+newdir)
        print("\nExiting papeScrape...\n")
    else:
        print("\nCreated directory "+newdir+" successfully")
        opText = soup.find("blockquote", {"class": "postMessage"}).text
        textFile = open(newdir+"op.txt", "w")
        textFile.write(opText)
        textFile.close()
        print("\nSaved OP message as "+newdir+"op.txt\n")

        results = []
        for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
            results.append(a["href"])

        for i in results:
            urllib.request.urlretrieve("http:"+i, newdir+i[19:])
            print("Downloaded "+i[19:])
        print("\nAll images downloaded.")
        print("\nExiting papeScrape...\n")


nsfw = nsfwFilter()
board = scrapeBoards(nsfw)
thread = scrapeThreads(board)
scrapeImages(board, thread)