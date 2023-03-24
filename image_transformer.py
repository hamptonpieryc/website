from PIL import Image, ImageDraw, ImageFont
from os import walk, makedirs

from pathlib import Path


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


# xxxxxxxxxxxxxx
# xxxxxxxxxxxxxx
# xxxxxxxxxxxxxx
#
# xxxxxx
# xxxxxx
# xxxxxx

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


# def crop_best_letterbox(pil_img):
#     pil_img.size
#     return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


# thumb_width = 200
# crop_best_square(Image.open('content/images/square/looking-to-join/kayak.jpeg')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('images/kayak-square-200.jpeg', quality=95)
#
# thumb_width = 600
# crop_best_square(Image.open('content/images/square/looking-to-join/kayak.jpeg')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('images/kayak-square-600.jpeg', quality=95)
#
# crop_letterbox(Image.open('content/images/square/looking-to-join/kayak.jpeg'), 4) \
#     .save('images/kayak-letterbox-800.jpeg', quality=95)


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

    def crop_to_square(self, file, path, size, suffix):
        parent = str(path.parent)
        tail = parent[len("content/images/square/"):]
        self.make_dirs(self.output_dir + "/images/square/" + tail)
        output_file = self.output_dir + "/images/square/" + tail + "/" + path.stem + suffix + path.suffix
        with open(file, "r") as f:
            print("Processing content in: " + file + " as a square image to " + output_file)
            crop_best_square(Image.open(file)) \
                .resize((size, size), Image.LANCZOS) \
                .save(output_file, quality=95)

    def crop_to_letterbox(self, file, path, size, suffix):
        parent = str(path.parent)
        tail = parent[len("content/images/letterbox/"):]
        self.make_dirs(self.output_dir + "/images/letterbox/" + tail)
        output_file = self.output_dir + "/images/letterbox/" + tail + "/" + path.stem + suffix + path.suffix
        with open(file, "r") as f:
            print("Processing content in: " + file + " as a letterbox image to " + output_file)
            crop_letterbox(Image.open(file), 3) \
                .resize((size, int(size / 3)), Image.LANCZOS) \
                .save(output_file, quality=95)
            title_text = "size=" + str(size)
            im = Image.open(output_file)
            # font = ImageFont.truetype("arial.ttf", 20)

            image_editable = ImageDraw.Draw(im)
            image_editable.text(xy=(15, 15), text=title_text)
            im.save(output_file)

    @staticmethod
    def make_dirs(dir_name):
        try:
            makedirs(dir_name)
        except OSError as e:
            1 == 1  # do nothing


ImagePipeline(".", ".").run()

# crop_best_square(Image.open('test_content/images/discover-sailing.png')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('discover-sailing-square.png', quality=95)
#
# crop_best_square(Image.open('test_content/images/pubquiz.jpeg')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('pubquiz-square.jpeg', quality=95)
