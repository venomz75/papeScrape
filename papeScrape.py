#!/usr/bin/python3

#import libraries
import urllib
import requests
import json
import re
import os
from bs4 import BeautifulSoup

#initialise variables
filepath = os.getcwd()
start = "http://www.4chan.org/"
data = requests.get(start)
soup = BeautifulSoup(data.text, 'html.parser')
boardLinks = []
boardNames = []
boardTags = []


for a in soup.find_all("a", {"class": "boardlink", "href": True}):
    if len(a["href"]) < 30:
        boardLinks.append(a["href"])
    if a.text:
        boardNames.append(a.text)

for i in boardLinks:
    boardTag = i[7:]
    boardIndex = boardTag.index("/")
    boardTag = boardTag[boardIndex+1:]
    boardIndex = boardTag.index("/")
    boardTag = boardTag[0:boardIndex]
    boardTags.append(boardTag)


for i in range(len(boardLinks)):
    print(str(i).zfill(2)+") /"+boardTags[i]+"/ - "+boardNames[i])
boardSelection = input("\nChoose your board: ")
try:
    boardSelection = int(boardSelection)
except ValueError:
    print("\nInvalid input!")
else:
    if boardSelection > 69 or boardSelection < 0:
        print("\nInvalid input!")
    else:
        print("\nParsing /"+boardTags[boardSelection]+"/, please wait...\n")


threadLinks = []
threadSubjects = []
threadNumbers = []

for i in range(11):
    page = "http:"+boardLinks[boardSelection]+str(i)
    data = requests.get(page)
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
try:
    threadSelection = int(threadSelection)
except ValueError:
    print("\nInvalid input!")
else:
    if threadSelection > 149 or boardSelection < 0:
        print("\nInvalid input!")
    else:
        print("\nDownloading images from thread #"+threadNumbers[threadSelection]+" on /"+boardTags[boardSelection]+"/, please wait...")


thread = threadLinks[threadSelection]
data = requests.get(thread)
soup = BeautifulSoup(data.text, 'html.parser')
opText = soup.find("blockquote", {"class": "postMessage"}).text

threadSubjects[threadSelection] = re.sub('[^A-Za-z0-9]+', '', threadSubjects[threadSelection])
newdir = boardTags[boardSelection]+"/"+threadSubjects[threadSelection]
print(newdir)

try:
    os.mkdir(newdir)
except OSError:
    #exits if directory cannot be created
    print("\nFailed to create directory "+newdir)
    print("\nExiting papeScrape...\n")
else:
    print("\nCreated directory "+newdir+" successfully")
    
    #saves OP message as a text file which is useful if the OP doesn't have a thread subject
    textFile = open(filepath+"/"+newdir+"/"+"op.txt", "w")
    textFile.write(opText)
    textFile.close()
    print("\nSaved OP message as "+newdir+"/"+"op.txt\n")

    #collects all of the images into an array
    results = []
    for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
        results.append(a["href"])

    #saves and prints confirmation of each image saved
    for i in results:
        urllib.request.urlretrieve("http:"+i, filepath+"/"+newdir+"/"+i[19:])
        print("Downloaded "+i[19:])
    print("\nAll images downloaded.")

    print("\nExiting papeScrape...\n")

#[x]add board (wg,e,x,g etc.) detector
#[x]add board browser
#[x]add sitewide browser
#[]add filename regex filtering to eliminate "/" etc from folder name
#[]add op in no subject threads on listing
#[]add image count
#[]add no subject thread numbering
#[]add concurrent download capability
#[]add commands
#[]add main loop