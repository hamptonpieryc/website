from os import walk
from html.parser import HTMLParser

# from PIL import Image, ImageDraw, ImageFilter
#
# im = Image.open("images/image1.jpeg")
# print(im.format, im.size, im.mode)


#
# A base parser that can look for specified tags
# Normally a class should just override handle_captured
#
class BaseParser(HTMLParser):
    def __init__(self, tag_names, content_buf):
        HTMLParser.__init__(self)
        self.capture_mode = False
        self.tag_names = tag_names
        self.current_tag = ''
        self.capture_buffer = []
        self.content_buffer = content_buf

    def handle_starttag(self, tag, attrs):
        # trigger when one of our expected tags is found
        if tag in self.tag_names and not self.capture_mode:
            self.capture_mode = True
            self.current_tag = tag
            return

        if self.capture_mode and not tag == self.current_tag:
            self.capture_buffer.append("<" + tag)
            for attr in attrs:
                self.capture_buffer.append(' ' + attr[0] + '=')
                self.capture_buffer.append('"' + attr[1] + '"')
            self.capture_buffer.append(">")
        else:
            self.content_buffer.append("<" + tag)
            for attr in attrs:
                self.content_buffer.append(' ' + attr[0] + '=')
                self.content_buffer.append('"' + attr[1] + '"')
            self.content_buffer.append(">")

    def handle_endtag(self, tag):
        if self.capture_mode and not tag == self.current_tag:
            self.capture_buffer.append("</" + tag + ">")

        if tag == self.current_tag and self.capture_mode:
            self.capture_mode = False
            self.handle_captured(self.current_tag, self.capture_buffer)
            self.current_tag = ''

    def handle_data(self, data):
        if self.capture_mode:
            self.capture_buffer.append(data)
        else:
            self.content_buffer.append(data)

    def handle_captured(self, tag_name, captured):
        self.content_buffer.extend(captured)


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


# process a <hpyc-top-panel> tag
class TopPanelParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, 'hpyc-top-panel', content_buffer)

    def handle_data(self, data):
        if self.tag_found:
            self.content_buffer.append(data)
            print('processing hpyc-top-panel content')


class PanelParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, ['hpyc-top-panel', 'hpyc-content-panel'], content_buffer)


# process a <hpyc-content> tag
class ContentParser(BaseParser):
    def __init__(self, content_buffer):
        BaseParser.__init__(self, 'hpyc-content', content_buffer)

    def handle_captured(self, tag_name, captured):
        #print('processing tag:' + tag_name + '-' + ''.join(captured))
        super().handle_captured(tag_name, captured)

    # def handle_data(self, data):
    #     if self.capture_mode:
    #         print('processing hpyc-content tag:' + data)
    #         self.content_buffer.append(data)


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


# for i in files:
#     with open("content2/" + i, "r") as f:
#         content_buffer = []
#         content_parser = ContentParser(content_buffer)
#         content_parser.feed(''.join(f.readlines()))
#         processed = ''.join(content_buffer)
#         print("Processing content file:" + i + ", with " + str(len(processed)) + " characters")
#         layout_parser = LayoutParser(processed)
#         layout_parser.feed(layout)
#         with open(i, "w") as saved:
#             saved.write(layout_parser.processed())

