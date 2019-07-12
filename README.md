papeScrape is a basic Python webscraper which downloads all of the images within a thread. It is still under development so it is not as feature rich as I'd like it to be at the moment (but it still works).

Current features:
    *Select a board => select a thread => folder is created and images begin to save.

Known bugs:
    *Thread topics with the following: /"*? will cause the creation of a directory to fail, thus saving no images. This should be fixed soon as the solution is very easy to implement.

Planned changes:
    *Improve naming for threads with no subject.
    *Add selection of boards by tag or name (wg or Wallpapers/General).
    *Add selection of threads by post number or topic.
    *Add an image count to the threads.
    *Add capability for multiple concurrent thread downloads.
    *Add command based interaction with the program.
