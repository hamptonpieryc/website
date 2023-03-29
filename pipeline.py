from os import walk
from hpyc_transformers import ContentPageTransformer
from html_transformer import Transformer, TransformingParser
from pathlib import Path
from utils import make_dirs
import shutil



class Pipeline:
    """ The pipeline that runs all tne the necessary HTML transforms and image manipulation"""

    def __init__(self, input_dir: str, output_dir: str, transformers: [Transformer] = [ContentPageTransformer()]):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.transformers = transformers

    def run(self):
        print("running the pipeline")
        with open(self.input_dir + '/layout.html', "r") as f:
            layout = ''.join(f.readlines())
        print("layout.html is " + str(len(layout)) + " characters")

        files = []
        for (dirpath, dirnames, filenames) in walk(self.input_dir + '/content'):
            for f in filenames:
                if "/content/images/" not in dirpath:
                    files.append(dirpath + "/" + f)

        for i in files:
            with open(i, "r") as f:
                if i.endswith(".html"):
                    print("Processing content in: " + i)
                    raw = ''.join(f.readlines())

                    # nested = NestedTransform(outer_tag='nested', transforms=[FooTransform(), BarTransform()])
                    buffer = []
                    parser = TransformingParser(buffer, self.transformers)
                    parser.feed(raw)

                    path = Path(i)
                    parent = str(path.parent)
                    tail = parent[len("content/"):] if self.input_dir == '.' else parent[len(self.input_dir + "/content/"):]
                    tail = "/" if tail == "" else "/" + tail + "/"
                    make_dirs(self.output_dir + tail)
                    output_file = self.output_dir + tail + path.stem + path.suffix

                    with open(output_file, "w") as saved:
                        processed = layout.replace("REPLACE-ME!", ''.join(buffer))
                        saved.write(processed)
                elif i.endswith(".pdf"):
                    path = Path(i)
                    parent = str(path.parent)
                    tail = parent[len("content/"):] if self.input_dir == '.' else parent[
                                                                                   len(self.input_dir + "/content/"):]
                    tail = "/" if tail == "" else "/" + tail + "/"
                    make_dirs(self.output_dir + tail)
                    output_file = self.output_dir + tail + path.stem + path.suffix
                    shutil.copy2(i, output_file)  # complete target filename given

