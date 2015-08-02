# boogiepdf

A bunch of quick and *dirty* event based classes to help parse the InkML (http://www.w3.org/TR/InkML/) in the PDFs generated by BoogiBoard Sync 9.7  
http://myboogieboard.com/products/boogie-board-sync-9.html

## Requirements 
  * python 2.7 
    * (Will port to python 3 when I get time. Currently different behaviour of pdfrw in python3 are causing issues) 
  * pdfrw module https://pypi.python.org/pypi/pdfrw/

## How to use 

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
