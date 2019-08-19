## The Old Switcheroo: Tiff and multipage tiff enabler

## About:
This addon swaps out ```.tif``` files and temporarily replaces it with a ```.png``` file during review.

Clicking on a multipage tiff will increment the page number, shift+clicking will allow you to jump to a specific page.

<img src="https://github.com/lovac42/TheOldSwitcheroo/blob/master/screenshots/boxing.gif?raw=true" />  

## Caveat:
You must run Anki from source. This addon uses the PILLOW library which can not run as an addon in Anki's virtual environment. More info here: https://stackoverflow.com/questions/55940735

## Cache:
PNG files are created in a folder called ```.cache``` inside this addon's folder. Please remember to clear this cache from time to time.


## Random:
Use attribute ```data-rand="n"``` in ```<img``` tag where ```n``` is the max number of pages available in the multipage tiff file.

