# boogiepdf

A couple of exporters from BoogieBoard InkML (embedded in the PDF) to Gimp and Krita

A bunch of quick and *dirty* event based classes to help parse the InkML (http://www.w3.org/TR/InkML/) in the PDFs generated by BoogiBoard Sync 9.7
http://myboogieboard.com/products/boogie-board-sync-9.html

## Requirements 
* python 2.7 
  * (Will port to python 3 when I get time. Currently different behaviour of pdfrw in python3 are causing issues) 
* pdfrw module https://pypi.python.org/pypi/pdfrw/
  * To install on Ubuntu or Debian run the below command
    * sudo apt-get install python-pdfrw
  * On other platforms, if you have access to the "pip" command:
    * sudo pip install pdfrw

## How to use 

### Krita Exporter
* Launch a terminal or command prompt
* Run the following command at the command line, substituting filenames for your own:
   * cd DirectoryWhereYouClonedOrUnzippedThisProject
   * python boogiePdfToKritaRec.py DirectoryWhereYouHaveYourBoogieBoardPdfs/BB_somenum.pdf > yourtitle.krarec
* Open Krita
* create a document of width 7000 and height 4500 
* navigate to Tools&gt;Macros&gt;Open and play
* select yourtitle.krarec and press open


### Gimp Plugin
* warning :
  * it is currently very slow. 
* Installing 
  * copy the files file-boogieboardpdfinkml-load.py, boogiePdf.py and boogieInk.py to yourhomefolder/gimp-2.8/plugins/ folder or /usr/lib/gimp/2.0/plugins or the plugins
* Using
  * start gimp (if already running, you will need to terminate it first) 
  * choose a good brush for painting and set an appropriate brush 
  * fire the open dialog and choose the BoogieBoard pdf that you want to import (don't click open yet)
  * in the filetype filter (the dropdown that says "All Images" choose "BoogieBoard PDF InkML"
  * click open
  * wait
    * for a really long time .. really really long time
    * for some more time
      Or
    * If you just want to have some fun, keep changing brush and colors when it imports .. 
  * tada! your image is open

### Modules in your own application
* Import the boogiePdf and boogieInk modules
* Extend the boogieInk.BoogieInkParser class as shown in boogiePdf_tester.py 
  *  The parser is event based: that is, for different events, you define different functions in your extended class
* Instantiate the boogiePdf.BoogiePDFParser class passing the PDF filename to the constructor
* call the parse function of the instantiated BoogiePDFParser passing your new *extended* BoogieInkParser
  * You may pass True or False to the "simple" parameter which affects whether it calls "simpleTracePointParser" or "trackedTracePointParser"
* Alternatively you could use only boogieInk which does not depend on pdfrw, but you will have to extract the InkML yourself.


## Warning
* This module is "quick and dirty" and is written specifically for BoogieBoard Sync 9.7 , especially the version I use (which one? I still wonder). It is highly unlikely that it will work with any other InkML. 
* The pen state calculations are not yet tested. I am writing these classes to write even more quick and dirty classes/plugins for gimp and Krit.a
* It does *not* complain if you do not pass it an extended BoogieInkParser. So don't end up confusing yourself. 
* The GIMP Plugin is extremely slow right now 
