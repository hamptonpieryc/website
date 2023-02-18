from os import walk
from html.parser import HTMLParser


# process the layout file
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
            self.combined.append("<" + tag)
            for attr in attrs:
                self.combined.append(' ' + attr[0] + '=')
                self.combined.append('"' + attr[1] + '"')
            self.combined.append(">")

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


#
# A base parser that can look for a specified tag
#
class BaseParser(HTMLParser):
    def __init__(self, tag_name, content_buffer):
        HTMLParser.__init__(self)
        self.tag_found = False
        self.tag_name = tag_name
        self.content_buffer = content_buffer

    def handle_starttag(self, tag, attrs):
        if tag == self.tag_name and not self.tag_found:
            self.tag_found = True
        else:
            self.content_buffer.append("<" + tag)
            for attr in attrs:
                self.content_buffer.append(' ' + attr[0] + '=')
                self.content_buffer.append('"' + attr[1] + '"')
            self.content_buffer.append(">")

    def handle_endtag(self, tag):
        if tag == self.tag_name and not self.tag_found:
            self.tag_found = False
        else:
            self.content_buffer.append("</" + tag + ">")

    def handle_data(self, data):
        if self.tag_found:
            self.content_buffer.append(data)


# process a <hpyc-top-panel> tag
class TopPanelParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, 'hpyc-top-panel', content_buffer)

    def handle_data(self, data):
        if self.tag_found:
            self.content_buffer.append(data)
            print('processing hpyc-top-panel content')


# process a <hpyc-content> tag
class ContentParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, 'hpyc-content', content_buffer)

    def handle_data(self, data):
        if self.tag_found:
            self.content_buffer.append(data)


# read the layout file
layout = ''
with open("templates/layout.html", "r") as f:
    layout = ''.join(f.readlines())
print("layout.html is " + str(len(layout)) + " characters")

files = []
for (dirpath, dirnames, filenames) in walk("content"):
    files.extend(filenames)
    break

for i in files:
    with open("content/" + i, "r") as f:
        content_buffer = []
        content_parser = ContentParser(content_buffer)
        content_parser.feed(''.join(f.readlines()))
        processed = ''.join(content_buffer)
        print("Processing content file:" + i + ", with " + str(len(processed)) + " characters")
        layout_parser = LayoutParser(processed)
        layout_parser.feed(layout)
        with open(i, "w") as saved:
            saved.write(layout_parser.processed())
