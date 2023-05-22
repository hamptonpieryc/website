import datetime


class SiteMapBuilder:

    def __init__(self):
        self.pages = []

    def add_page(self, page_name: str, last_modified: datetime):
        print(page_name)
