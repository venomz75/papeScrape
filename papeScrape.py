#!/usr/bin/python3
from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import urllib
import json
import os
import re


#Entry point to the program.
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
    menu()


#The main point of user choice and interaction.
def menu():
    stop = False
    while stop == False:
        print("""
MENU
1) Manually input board and thread number.
2) Browse threads on a board.
3) Print ongoing jobs.
4) Quit
        """)

        try:
            selection = int(input("Select an option number: "))
        except:
            print("Invalid input! Use a number from (1-4).")
        else:
            if selection == 1: manualMode()
            elif selection == 2: browseMode()
            elif selection == 3: urllib.request.urlretrieve("http://i.4cdn.org/wg/1581243426506.png", "1.png")
            elif selection == 4: print("Quitting!"); stop = True


#Option 1: Manually enter a board and thread(post) number.
def manualMode():
    boardChoice = input("Board tag (e.g. wg): ")
    threadChoice = input("Thread number: ")
    url = "http://boards.4chan.org/" +boardChoice+ "/thread/" +threadChoice
    soup = scrape(url)
    if soup.find_all("h2"):
        print("ERROR")
    else:
        download(url)


#Option 2: Browse a board's threads.
def browseMode():
    boardChoice = input("Board tag (e.g. wg): ")
    url = "http://boards.4chan.org/"+boardChoice+"/catalog"
    soup = scrape(url)
    script = soup.select("script")[2].get_text()
    script2 = script[script.index("var catalog"):script.index("var style_group")]
    script3 = script2[script2.index("{"):script2.rindex(";")]
    dictionary = json.loads(script3)
    threadIndex = []
    index = 0

    for thread in dictionary["threads"]:
        subject = "No subject" if not dictionary["threads"][thread]["sub"] else dictionary["threads"][thread]["sub"]
        threadIndex.append(thread)
        print(str(index)+": "+thread+" - "+subject+" - I:"+str(dictionary["threads"][thread]["i"])+" R:"+str(dictionary["threads"][thread]["r"]))
        index += 1
    
    threadChoice = input("Choose a thread: ")
    threadURL = "http://boards.4chan.org/" +boardChoice+ "/thread/" +threadIndex[int(threadChoice)]
    threadJSON = dictionary["threads"][threadIndex[int(threadChoice)]]
    boardDir = "/"+boardChoice+"/"
    threadDir = re.sub('[^A-Za-z0-9]+', '', threadIndex[int(threadChoice)]+"_"+threadJSON["sub"]) + "/" if threadJSON["sub"] else re.sub('[^A-Za-z0-9]+', '', threadIndex[int(threadChoice)]+"_"+threadJSON["teaser"]) + "/"
    if not os.path.isdir(os.getcwd()+boardDir):
        createDir(boardDir)
    createDir(boardDir + threadDir)
    download(threadURL, os.getcwd()+"/"+boardDir+"/"+threadDir)


def download(url, filepath):
    soup = scrape(url)
    print (url)
    print (filepath)

    if not soup.find_all("a", {"class": "fileThumb", "href": True}):
        print("ERROR")
        return
    
    imgNumber = 1
    for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
        print("http:"+a["href"])
        print(filepath+a["href"][a["href"].rindex("/")+1:])
        urllib.request.urlretrieve("http:"+a["href"], filepath+a["href"][a["href"].rindex("/")+1:])
        imgNumber += 1

def createDir(newdir):
    filepath = os.getcwd()+newdir
    try:
        os.mkdir(filepath)
    except OSError:
        print("\nFailed to create directory "+filepath)
        print("\nExiting papeScrape...\n")
    else:
        print("\nCreated directory "+newdir+".")


#General webpage scrape function
def scrape(url):
    try:
        return BeautifulSoup(requests.get(url).text, "html.parser")
    except:
        print("Invalid URL!")


#Define entry point
if __name__ == '__main__':
    main()