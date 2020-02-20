#### papeScrape is a Python webscraper which downloads all of the images in a 4chan thread. I created it to download wallpapers from the [/wg/](http://boards.4chan.org/wg/catalog) board, but you can download images from a thread on any board.

## Setup/Usage:
* You will need BeautifulSoup and requests for this to work. Download them with the following: `apt-get install python3-bs4` and `pip install requests`
* Once you've done that, run the program with `python3 papeScrape.py` or `./papeScrape.py` if it's set as executable.
* Use the commands to add threads or check which jobs are still ongoing. You can download from multiple threads simultaneously, making it easier to mass download images!
* When you start a download, a board directory is created where `papeScrape.py` is. Within it will be directories fo

## Upcoming changes:
* The program is not fully immune to invalid inputs yet so you could crash it! I plan to catch all these exceptions to eliminate the risk of losing download processes.
* There may be more quality of life additions but the core functionality is there in a lightweight package.
