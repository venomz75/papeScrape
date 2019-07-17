#### papeScrape is a basic Python webscraper which downloads all of the images in a 4chan thread. As the name may suggest; the initial intention was to download wallpapers from it's [/wg/](http://boards.4chan.org/wg/catalog) board.

## Current features:
* Include or exclude NSFW boards
* Browse and choose any thread from any board
* Use commands to add or list active download jobs, and prematurely exit the application gracefully
* Files from a thread saved in it's own directory, including the OP.

## Planned changes:
### Content:
* Add the option to manually paste a URL to allow the user to avoid having to wait for the webscraping
* Add the option to download all images from a board
### Commands:
* If a board is selected more than once, instantly allow the user to choose another thread rather than having to wait for the program to parse the board once again
* Add a refresh command to allow the user to force the program to parse previous boards again.
* Add a cancel job command to allow the user to stop a job prematurely
### Misc:
* Add an image count when listing threads
* General text formatting improvements
### Upon full feature implementation:
* Improve efficiency and reduce time complexity
* Test various inputs/outputs, remove any bugs or unwanted behaviour
