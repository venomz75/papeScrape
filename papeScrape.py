#!/usr/bin/python3

import urllib
import requests
import json
import re
import os
from bs4 import BeautifulSoup #pip install beautifulsoup4

boardLinks = []
boardNames = []
boardTags = []
threadLinks = []
threadSubjects = []
threadNumbers = []

def scrapeBoards():
    data = requests.get("http://www.4chan.org/")
    soup = BeautifulSoup(data.text, 'html.parser')

    for a in soup.find_all("a", {"class": "boardlink", "href": True}):
        if len(a["href"]) < 30:
            boardLinks.append(a["href"])
        if a.text:
            boardNames.append(a.text)

    for i in boardLinks:
        tag = i[7:]
        boardIndex = tag.index("/")
        tag = tag[boardIndex+1:]
        boardIndex = tag.index("/")
        tag = tag[0:boardIndex]
        boardTags.append(tag)

    for i in range(len(boardLinks)):
        print(str(i).zfill(2)+") /"+boardTags[i]+"/ - "+boardNames[i])
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
    newdir = boardTags[boardSelection]+"/"+threadSubjects[threadSelection]+"/"

    try:
        os.mkdir(boardTags[boardSelection])
        os.mkdir(newdir)
    except OSError:
        print("\nFailed to create directory "+newdir)
        print("\nExiting papeScrape...\n")
    else:
        print("\nCreated directory "+newdir+" successfully")
        opText = soup.find("blockquote", {"class": "postMessage"}).text
        textFile = open(filepath+"/"+newdir+"op.txt", "w")
        textFile.write(opText)
        textFile.close()
        print("\nSaved OP message as "+newdir+"op.txt\n")

        results = []
        for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
            results.append(a["href"])

        for i in results:
            urllib.request.urlretrieve("http:"+i, filepath+"/"+newdir+i[19:])
            print("Downloaded "+i[19:])
        print("\nAll images downloaded.")
        print("\nExiting papeScrape...\n")



board = scrapeBoards()
thread = scrapeThreads(board)
scrapeImages(board, thread)

#[]add alphabetical sorting
#[]add image count
#[]add no subject thread numbering
#[]add concurrent download capability
#[]add commands
#[]add main loop