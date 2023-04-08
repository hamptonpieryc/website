Hampton Pier YC Website
=======================

Source code for the Hampton Pier Yacht Club website.
A test deployment is at https://hamptonpier.club

# Prerequisites

So far this has only been tested on OSX (Mac)

## Mac

* [GIT](https://github.com/git-guides/install-git)
* An IDE such 
    * [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
    * [Intellij](https://www.jetbrains.com/idea/)
    * [HTML IDEs](https://www.interviewbit.com/blog/html-ides/)




## Windows

TODO

# Changing Content

Note, to view the updated content see `Deploying` below.

## Editing text

The text for each page is held in the `content` folder. To update simply edit the text.

## Content Blocks

## Adding pages 
Todo

## Adding images
Todo

# Deploying 

## Locally

Run `./build.sh` (this will convert content pages into full HTML) and then open  `home.html` in a browser

## To the public site 

Each push to GitHub will automatically build and deploy using a feature of GitHub called `Actions`. 
This may take a minute or two. Click [here](https://github.com/hamptonpieryc/website/actions) 
to check on progress.  


## Tech Notes 

Just some useful tech links:

* https://picturepan2.github.io/spectre/
* https://www.canva.com/colors/color-wheel/
* https://app.haikei.app/
* https://www.windguru.cz/help.php?sec=distr
* https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
* https://experienceleague.adobe.com/docs/target/using/experiences/vec/mobile-viewports.html
* https://stock.adobe.com/uk/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k=sinking+boat&order=relevance&safe_search=1&limit=100&search_page=1&search_type=usertyped&acp=&aco=sinking+boat&get_facets=0
* https://developers.google.com/maps/documentation/javascript/adding-a-google-map#key
* 

Python3 is also required but comes preinstalled on OSX


https://www.geeksforgeeks.org/how-to-install-pil-on-macos/
python3 -m pip install --upgrade Pillow
https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
