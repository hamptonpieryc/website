from os import walk
from hpyc_transformers import ContentPageTransformer, BioPanelTransformer
from html_transformer import Transformer, TransformingParser
from pathlib import Path
from utils import make_dirs
from sitemap_builder import SiteMapBuilder

import shutil
import os
import datetime
import traceback


class Pipeline:
    """ The pipeline that runs all tne the necessary HTML transforms and image manipulation"""

    def __init__(self, input_dir: str, output_dir: str,
                 transformers: [Transformer] = [ContentPageTransformer(), BioPanelTransformer()]):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transformers = transformers
        self.sitemap_builder = SiteMapBuilder()

    def run(self):
        print("running the pipeline")
        with open(self.input_dir + '/content/layout.html', "r") as f:
            layout = ''.join(f.readlines())
        print("layout.html is " + str(len(layout)) + " characters")

        skipped_files = {'openday.html','404.html'}
        failed = False

        files = []
        for (dirpath, dirnames, filenames) in walk(self.input_dir + '/content'):
            for f in filenames:
                if "/content/images/" not in dirpath:
                    files.append(dirpath + "/" + f)

        for i in files:
            try:
                with open(i, "r") as f:
                    # standardise filename
                    page_name, page_path = self.stanrdardise_names(i)

                    if i.endswith(".html") and not (page_name in skipped_files):
                        print("Processing content in: " + i)

                        # record this file in the sitemap builder
                        create_time = os.path.getctime(i)
                        create_date = datetime.datetime.fromtimestamp(create_time)
                        raw = ''.join(f.readlines())
                        self.sitemap_builder.add_page(page_path + page_name, create_date)

                        # nested = NestedTransform(outer_tag='nested', transforms=[FooTransform(), BarTransform()])
                        buffer = []
                        parser = TransformingParser(buffer, self.transformers)
                        parser.feed(raw)

                        make_dirs(self.output_dir + page_path)
                        output_file = self.output_dir + page_path + page_name

                        processed = layout.replace("REPLACE-ME!", ''.join(buffer))

                        with open(output_file, "w") as saved:
                            saved.write(processed)

                        if page_name == "index.html":
                            landing_pages = ["instagram", "facebook", "kentonline"]
                            make_dirs(self.output_dir + "/landing")
                            for l in landing_pages:
                                output_file = self.output_dir + page_path + "landing/" + l + ".html"
                                with open(output_file, "w") as saved:
                                    saved.write(processed)

                    elif i.startswith("./content/docs/") or (page_name in skipped_files):
                        make_dirs(self.output_dir + page_path)
                        output_file = self.output_dir + page_path + page_name
                        print("Copying file to: " + output_file)
                        shutil.copy2(i, output_file)  # complete target filename given

            except Exception as ex:
                print("Oops!.")
                # print(str(ex))
                tb = traceback.format_exc()
                self.write_error_page(i, tb)
                failed = True

        sitemap = self.sitemap_builder.build_site_map()
        with open(self.output_dir + "/sitemap.xml", "w") as f:
            f.write(sitemap)

        if failed:
            print("One or more errors were detected - please see the logs for details")
            raise OSError("One or more errors were detected - please see the logs for details")

    def stanrdardise_names(self, i):
        path = Path(i)
        parent = str(path.parent)
        tail = parent[len("content/"):] if self.input_dir == '.' else parent[
                                                                      len(self.input_dir + "/content/"):]
        tail = "/" if tail == "" else "/" + tail + "/"
        page_name = path.stem + path.suffix
        return page_name, tail

    def write_error_page(self, i, error_message):
        try:
            print("will write out an error page")
            page_name, page_path = self.stanrdardise_names(i)
            output_file = self.output_dir + page_path + page_name
            with open(output_file, "w") as saved:
                saved.write(error_message)

        except Exception as ex:
            print("ignoring: " + str(ex))
