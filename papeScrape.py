#!/usr/bin/python3
from bs4 import BeautifulSoup   #apt-get install python3-bs4
import requests                 #pip install requests
from collections import OrderedDict
import threading
import urllib
import json
import os
import re

#TO ADD
#
#When quitting, check if there are any ongoing downloads, if so prompt the user to confirm their choice.
#Add an images downloaded/total images counter to the monitoring of threads.
#Swap options 1 and 2
#Sort the JSON of threads by image count ascending (bottom is seen due to large output, usually large image counts are desired)

activeThreads = [] #Used to store active download threads

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

=====MENU=====
1) Browse threads on a board.
2) Print ongoing jobs.
3) Quit
        """)

        try:
            selection = int(input("Select an option number: "))
        except:
            print("Invalid input! Use a number from (1-3).")
        else:
            if selection == 1: browseMode()
            elif selection == 2: checkActive()
            elif selection == 3: print("Quitting!"); stop = True


#Option 1: Browse a board's threads.
def browseMode():
    #Initial webscrape and filtering of catalog DOM
    boardChoice = input("Board tag (e.g. wg): ")
    url = "http://boards.4chan.org/"+boardChoice+"/catalog"
    soup = scrape(url)
    script = soup.select("script")[2].get_text()
    script2 = script[script.index("var catalog"):script.index("var style_group")]
    script3 = script2[script2.index("{"):script2.rindex(";")]
    dictionary = json.loads(script3, object_pairs_hook=OrderedDict)
    threadIndex = []
    index = 0

    #Parse JSON for thread objects and print them
    print("\n=====THREADS ON /"+boardChoice+"/=====")
    for thread in dictionary["threads"]:
        threadIndex.append(thread)
           
    threadIndex.sort(key=int)

    for thread in threadIndex:
        subject = "No subject" if not dictionary["threads"][thread]["sub"] else dictionary["threads"][thread]["sub"] 
        print(str(index)+": "+thread+" - "+subject+" - I:"+str(dictionary["threads"][thread]["i"])+" R:"+str(dictionary["threads"][thread]["r"]))
        index += 1

    #User chooses a thread from the listed objects using the prior index
    threadChoice = input("Choose a thread: ")
    #Prepare thread download by assembling target URL and directory name
    threadURL = "http://boards.4chan.org/" +boardChoice+ "/thread/" +threadIndex[int(threadChoice)]
    threadJSON = dictionary["threads"][threadIndex[int(threadChoice)]]
    boardDir = "/"+boardChoice+"/"
    threadDir = re.sub('[^A-Za-z0-9_]+', '', threadIndex[int(threadChoice)]+"_"+threadJSON["sub"]) + "/" if threadJSON["sub"] else re.sub('[^A-Za-z0-9]+', '', threadIndex[int(threadChoice)]+"_"+threadJSON["teaser"]) + "/"
    if not os.path.isdir(os.getcwd()+boardDir):
        createDir(boardDir)
    createDir(boardDir + threadDir)
    #Create and start download thread
    downloadThread = createThread(download, [threadURL, os.getcwd()+"/"+boardDir+"/"+threadDir])
    downloadThread.start()
    #Store data about the thread and create a monitor job with it
    threadData = [downloadThread, boardChoice, threadIndex[int(threadChoice)], str(threadJSON["i"])]
    activeThreads.append(threadData)
    monitorThread = createThread(monitor, [threadData])
    monitorThread.start()


def checkActive():
    print("\n=====ONGOING DOWNLOADS=====")
    for i in range(len(activeThreads)):
        print("/"+activeThreads[i][1]+"/"+activeThreads[i][2]+" - "+activeThreads[i][3]+" images")


#Checks if a download thread is still alive and waits until it ends before removing it from the activeThreads array
def monitor(threadData):
    while threadData[0].is_alive():
        pass
    activeThreads.remove(threadData)


#Downloads images from thread URL
def download(url, filepath):
    soup = scrape(url)

    if not soup.find_all("a", {"class": "fileThumb", "href": True}):
        print("ERROR")
        return
    
    for a in soup.find_all("a", {"class": "fileThumb", "href": True}):
        urllib.request.urlretrieve("http:"+a["href"], filepath+a["href"][a["href"].rindex("/")+1:])


#Create thread for given function and arguments, used to tidy up and further abstract code
def createThread(func, args):
    thread = threading.Thread(target=func, args=(args), daemon=True)
    return thread


#Create given directory
def createDir(newdir):
    filepath = os.getcwd()+newdir
    try:
        os.mkdir(filepath)
    except OSError:
        print("\nFailed to create directory "+filepath)
        print("\nExiting papeScrape...\n")
    else:
        print("\nCreated directory "+newdir+".")


#Scrape a given webpage into soup object
def scrape(url):
    try:
        return BeautifulSoup(requests.get(url).text, "html.parser")
    except:
        print("Invalid URL!")


#Define entry point
if __name__ == '__main__':
    main()