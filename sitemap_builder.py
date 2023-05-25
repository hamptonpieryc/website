import datetime


def frequency(page_name: str):
    if page_name.endswith("news"):
        return "weekly"
    else:
        return "monthly"


def removesuffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text


def included_page(page_name):
    if page_name.endswith("layout"):
        return False
    if page_name.endswith("example"):
        return False
    if "/landing/" in page_name:
        return False
    return True


class SiteMapBuilder:

    def __init__(self):
        self.pages = []

    def add_page(self, page_name: str, last_modified: datetime):
        self.pages.append(
            {"page_name": page_name, "last_modified": last_modified})

    def build_site_map(self):
        sitemap = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + "\n"
        sitemap = sitemap + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "\n"

        for page in self.pages:
            page_name = removesuffix(page["page_name"], ".html")
            if included_page(page_name):
                sitemap = sitemap + "  <url>\n"
                sitemap = sitemap + '    <loc>https://www.hpyc.org.uk' + page_name + "</loc>\n"
                sitemap = sitemap + "    <priority>1.0</priority>\n"
                sitemap = sitemap + "    <changefreq>" + frequency(page_name) + "</changefreq>\n"
                sitemap = sitemap + "    <lastmod>" + page["last_modified"].strftime("%Y-%m-%d") + "</lastmod>\n"
                sitemap = sitemap + "  </url>\n"

        sitemap = sitemap + '</urlset>'
        return sitemap
