import datetime


def frequency(page_name: str):
    if page_name.endswith("news.html"):
        return "weekly"
    else:
        return "monthly"


class SiteMapBuilder:

    def __init__(self):
        self.pages = []

    def add_page(self, page_name: str, last_modified: datetime):
        self.pages.append(
            {"page_name": page_name, "last_modified": last_modified})

    # def update_page(self, page_name: str, original_content: str, update_content: str):
    #     x = next(obj for obj in self.pages if obj["page_name"] == page_name)
    #     x["updated_content"] = update_content
    #     x["original_content"] = original_content

    def build_site_map(self):
        sitemap = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + "\n"
        sitemap = sitemap + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "\n"

        for page in self.pages:
            page["page_name"]
            sitemap = sitemap + "  <url>\n"
            sitemap = sitemap + '    <loc>https://www.hpyc.org.uk' + page["page_name"] + "</loc>\n"
            sitemap = sitemap + "    <priority>1.0</priority>\n"
            sitemap = sitemap + "    <changefreq>" + frequency(page["page_name"]) + "</changefreq>\n"
            sitemap = sitemap + "    <lastmod>" + page["last_modified"].strftime("%Y-%m-%d") + "</lastmod>\n"

            # if page["original_content"] == page["updated_content"]:
            #     print("same" + page["page_name"])
            # else:
            #     print("changed" + page["page_name"])
            #     print(page["original_content"])
            #     print(page["updated_content"])
            sitemap = sitemap + "  </url>\n"

        sitemap = sitemap + '</urlset>'
        return sitemap
