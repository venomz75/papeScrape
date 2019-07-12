#### papeScrape is a basic Python webscraper which downloads all the images in a 4chan thread. As the name may suggest; the initial intention was to download wallpapers from it's [/wg/](http://boards.4chan.org/wg/catalog) board.

## Current features:
* Selection of boards
* Selection of threads within chosen board
* Download all images in a thread, one thread at a time

## Known bugs:
* Thread topics with invalid directory characters e.g. "/" will cause the creation of directory and consequentially download no images.

## Planned changes:
* Improve naming for threads with no subject.
* Add selection of boards by tag or name (wg or Wallpapers/General).
* Add selection of threads by post number or topic.
* Add an image count to the threads.
* Add capability for multiple concurrent thread downloads.
* Add command based interaction with the program.
