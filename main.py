#!/usr/bin/env python3
"""make.fun news-image-20261121 entry point.

The competition harness runs this program with no network and expects it
to write the day's news image to /output/entry.png, byte-identical on
every run. The image is baked into this repository as entry.png by
draw_page.py, so this program simply copies it into place.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)


if __name__ == "__main__":
    main()
