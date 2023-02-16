from os import walk
from html.parser import HTMLParser

class LayoutParser(HTMLParser):

    def __init__(self, hpyc_content):
        HTMLParser.__init__(self)
        self.hpyc_content = hpyc_content
        self.hpyc_tag = False
        self.combined = []

    def handle_starttag(self, tag, attrs):
        if (tag == 'hpyc-content'):
            self.hpyc_tag = True
        else:
            self.combined.append("<" + tag )
            for attr in attrs:
                self.combined.append(' ' + attr[0]+ '=')
                self.combined.append('"'+ attr[1]+'"')
            self.combined.append(">" )

    def handle_endtag(self, tag):
        if tag == 'hpyc-content' and self.hpyc_tag:
            self.hpyc_tag = False
            self.combined.append(self.hpyc_content)
        else:
            self.combined.append("</" + tag + ">")

    def handle_data(self, data):
        if not self.hpyc_tag:
            self.combined.append(data)

    def processed(self):
        return ''.join(self.combined)

class ContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.hpyc_tag = False
        self.hpyc_content = []

    def handle_starttag(self, tag, attrs):
        if tag == 'hpyc-content' and not self.hpyc_tag:
            self.hpyc_tag = True
        else:
            self.hpyc_content.append("<" + tag )
            for attr in attrs:
                self.hpyc_content.append(' ' + attr[0]+ '=')
                self.hpyc_content.append('"'+ attr[1]+'"')
            self.hpyc_content.append(">" )

    def handle_endtag(self, tag):
        if tag == 'hpyc-content' and self.hpyc_tag:
            self.hpyc_tag = False
        else:
            self.hpyc_content.append("</" + tag + ">")

    def handle_data(self, data):
        if self.hpyc_tag:
            self.hpyc_content.append(data)

    def content(self):
        return ''.join(self.hpyc_content)


files = []
for (dirpath, dirnames, filenames) in walk("templates"):
    files.extend(filenames)
    break

# read the layout file
layout = ''
with open("templates/layout.html" , "r") as f:
    layout = ''.join(f.readlines())

print (layout)

for i in files:
    #print(i)
    if i != 'layout.html' and i != 'layout2.html':
        #print(i)
        with open("templates/" + i, "r") as f:
            content_parser = ContentParser()
            content_parser.feed(''.join(f.readlines()))
            #print(content)
            #print(content_parser.content())
            layout_parser = LayoutParser(content_parser.content())
            layout_parser.feed(layout)
            print(layout_parser.processed())
            with open( "p" + i, "w") as saved:
                saved.write(layout_parser.processed())



