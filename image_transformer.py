from PIL import Image, ImageDraw, ImageFilter
from os import walk, makedirs

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

        # cropping top/bottom
        cropped_height = img_height / ratio
        cropping = (img_height - cropped_height) / 2
        return pil_img.crop((0, cropping, img_width, img_height - cropping))
    else:
        # cropping sides
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))


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
                    tail = parent[len("content/images/square/"):]
                    output_dir = "./images/square/" + tail
                    try:
                        makedirs(output_dir)
                    except OSError as e:
                        1 == 1  # do nothing

                    self.crop_to_square(file, output_dir, path, 200, "small")
                    self.crop_to_square(file, output_dir, path, 512, "normal")

    @staticmethod
    def crop_to_square(file, output_dir, path, size, suffix):
        output_file = output_dir + "/" + path.stem + "-" + suffix + path.suffix
        with open(file, "r") as f:
            print("Processing content in: " + file + " as a square image to " + output_file)
            crop_best_square(Image.open(file)) \
                .resize((size, size), Image.LANCZOS) \
                .save(output_file, quality=95)


ImagePipeline(".", ".").run()

# crop_best_square(Image.open('test_content/images/discover-sailing.png')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('discover-sailing-square.png', quality=95)
#
# crop_best_square(Image.open('test_content/images/pubquiz.jpeg')) \
#     .resize((thumb_width, thumb_width), Image.LANCZOS) \
#     .save('pubquiz-square.jpeg', quality=95)
