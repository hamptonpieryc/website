from PIL import Image, ImageDraw, ImageFont
from os import walk
import shutil
from utils import make_dirs
from pathlib import Path


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_letterbox(pil_img, ratio):
    img_width, img_height = pil_img.size
    if img_height * ratio > img_width:
        # cropping top/bottom (too high)
        cropped_height = img_height / ratio
        cropping = int((img_height - cropped_height) / 2)
        return pil_img.crop((0, cropping, img_width, img_height - cropping))
    else:
        # cropping sides (too wide)
        cropped_width = img_height * ratio
        cropping = int((img_width - cropped_width) / 2)
        return pil_img.crop((cropping, 0, img_width - cropping, img_height))


def crop_best_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_best_letterbox(pil_img):
    return crop_center(pil_img, min(pil_img.size) * 4, min(pil_img.size))


class ImagePipeline:
    """ The pipeline that runs all tne the necessary image transforms and image manipulation"""

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        print("running the pipeline")

        files = []
        for (dirpath, dirnames, filenames) in walk(self.input_dir + '/content/images'):
            for f in filenames:
                files.append(dirpath + "/" + f)

        for file in files:
            path = Path(file)
            if path.suffix == ".jpeg" or path.suffix == ".png":
                parent = str(path.parent)
                if parent.startswith("content/images/square/"):
                    self.crop_to_square(file, path, 200, "-small")
                    self.crop_to_square(file, path, 512, "")
                elif parent.startswith("content/images/letterbox/"):
                    self.crop_to_letterbox(file, path, 640, "-small")
                    self.crop_to_letterbox(file, path, 1024, "")
                    self.crop_to_letterbox(file, path, 2048, "-large")
                else:
                    parent = str(path.parent)
                    tail = parent[len("content/images/"):]
                    make_dirs(self.output_dir + "/images/" + tail)
                    output_file = self.output_dir + "/images/" + tail + "/" + path.stem + path.suffix
                    print("Copying image: " + file + " to " + output_file)
                    shutil.copy2(file, output_file)  # complete target filename given

    def crop_to_square(self, file, path, size, suffix):
        parent = str(path.parent)
        tail = parent[len("content/images/square/"):]
        make_dirs(self.output_dir + "/images/square/" + tail)
        output_file = self.output_dir + "/images/square/" + tail + "/" + path.stem + suffix + path.suffix
        with open(file, "r") as f:
            print("Processing content in: " + file + " as a square image to " + output_file)
            crop_best_square(Image.open(file)) \
                .resize((size, size), Image.LANCZOS) \
                .save(output_file, quality=95)
            im = Image.open(output_file)
            image_editable = ImageDraw.Draw(im)
            image_editable.text(xy=(15, 15), text="size=" + str(size))
            im.save(output_file)

    def crop_to_letterbox(self, file, path, size, suffix):
        parent = str(path.parent)
        tail = parent[len("content/images/letterbox/"):]
        make_dirs(self.output_dir + "/images/letterbox/" + tail)
        output_file = self.output_dir + "/images/letterbox/" + tail + "/" + path.stem + suffix + path.suffix
        with open(file, "r") as f:
            print("Processing content in: " + file + " as a letterbox image to " + output_file)
            crop_letterbox(Image.open(file), 3) \
                .resize((size, int(size / 3)), Image.LANCZOS) \
                .save(output_file, quality=95)
            im = Image.open(output_file)
            image_editable = ImageDraw.Draw(im)
            image_editable.text(xy=(15, 15), text="size=" + str(size))
            im.save(output_file)


ImagePipeline(".", "site").run()

# crop_best_square(Image.open('test_content/images/discover-sailing.png')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('discover-sailing-square.png', quality=95)
#
# crop_best_square(Image.open('test_content/images/pubquiz.jpeg')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('pubquiz-square.jpeg', quality=95)
