from os import makedirs


def make_dirs(dir_name):
    try:
        makedirs(dir_name)
    except OSError as e:
        1 == 1  # do nothing
