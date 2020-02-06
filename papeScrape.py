#!/usr/bin/python3
from bs4 import BeautifulSoup   #pip install beautifulsoup4
import requests                 #pip install requests
import json
import os


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
    print("""
MENU
1) Manually input board and thread number.
2) Browse threads on a board.
3) Print ongoing jobs.
4) Quit
    """)
    stop = False
    while stop == False:
        selection = int(input("Select an option number: "))

        if selection == 1: manualMode()
        elif selection == 2: browseMode()
        elif selection == 3: print("Monitor jobs not yet implemented.")
        elif selection == 4: print("Quitting!"); stop = True
        else: print("Invalid input! Use a number from (1-4).")

def scrape(url):
    try:
        return BeautifulSoup(requests.get(url).text, "html.parser")
    except:
        print("Invalid URL!")

#Option 1: Manually enter a board and thread(post) number.
def manualMode():
    boardChoice = input("Board tag (e.g. wg): ")
    threadChoice = input("Thread number: ")
    url = "http://boards.4chan.org/" +boardChoice+ "/thread/" +threadChoice
    soup = scrape(url)
    if soup.find_all("h2"):
        print("404!")
    else:
        print(soup)

    exit()

#Option 2: Browse a board's threads.
def browseMode():
    boardChoice = input("Board tag (e.g. wg): ")
    url = "http://boards.4chan.org/"+boardChoice+"/catalog"
    soup = scrape(url)
    script = soup.select("script")[2].get_text()
    script2 = script[script.index("var catalog"):script.index("var style_group")]
    script3 = script2[script2.index("{"):script2.rindex(";")]
    dictionary = json.loads(script3)

    for thread in dictionary["threads"]:
        subject = "No subject" if not dictionary["threads"][thread]["sub"] else dictionary["threads"][thread]["sub"]
        print(thread+" - "+subject+" - I:"+str(dictionary["threads"][thread]["i"])+" R:"+str(dictionary["threads"][thread]["r"]))
    exit()


#Define entry point
if __name__ == '__main__':
    main()

