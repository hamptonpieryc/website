Hampton Pier YC Website
=======================

Source code for the Hampton Pier Yacht Club website.
A test deployment is at https://hamptonpieryc.github.io/website/home.html

# Prerequisites

So far this has only been tested on OSX (Mac)

## Mac

* [GIT](https://github.com/git-guides/install-git)
* An IDE such 
    * [Visual Studio](https://visualstudio.microsoft.com/vs/community/)
    * [Intellij](https://www.jetbrains.com/idea/)
    * [HTML IDEs](https://www.interviewbit.com/blog/html-ides/)

Python3 is also required but comes preinstalled on OSX

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

## Useful tools

* https://picturepan2.github.io/spectre/
* https://www.canva.com/colors/color-wheel/
* https://app.haikei.app/



https://www.geeksforgeeks.org/how-to-install-pil-on-macos/
python3 -m pip install --upgrade Pillow
https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
