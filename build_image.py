#!/usr/bin/env python3


import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Union

# writing and encoding default config
ET.register_namespace("", "http://www.w3.org/2000/svg")

Number = Union[int, float]

images_url: str = ""
source_url: str = ""

if len(sys.argv) == 1:
    raise Exception("File directory is required")

images_url: str = Path(sys.argv[1])

if len(sys.argv) == 2:
    source_url = images_url
elif len(sys.argv) == 3 and sys.argv[2]:
    source_url = Path(sys.argv[2])


if not images_url.exists():
    raise Exception("Image with the given directory does not exists")


def images_manipulation(img_url: str = "", des_url: str = ""):
    print("")
    print("--------SVG Start---------")
    print(f"url={img_url}")
    try:
        image = SVG(img_url, des_url)

        width: float = float(image.viewBox["width"])
        height: float = float(image.viewBox["height"])

        new_height: int = int(image_height_calculation(width, height))

        ratio: float = height / width

        new_width: int = int(new_height / ratio)

        image.set_sizes(width=new_width, height=new_height)

        print(f"width: {new_width}, height: {new_height}")

        image.save()

        print(f"saved in: {image.destination_url}")

    except Exception as e:
        print(f"Something wrong with the image  {e}")

    print("--------SVG END---------")
    print("")


# https://codepen.io/danpaquette/pen/jXpbQK
def image_height_calculation(widht: float, height: float) -> float:
    height_base: int = 30
    scale_factor: float = 0.30
    image_ratio = height / widht
    return (image_ratio ** scale_factor) * height_base


def isNumber(elem: any) -> bool:
    return isinstance(elem, int) or isinstance(elem, float)


class SVG:
    def __init__(self, image_url: str = "", destination_url: str = ""):
        self.image_url = image_url
        self.destination_url = destination_url if destination_url else self.image_url
        self._elementParsed = ET.parse(self.image_url)
        self._element = ET.Element(self._elementParsed)
        self._root = self._elementParsed.getroot()
        self._view_box_parser()

    def save(self, destination_url: str = ""):
        destination_url = destination_url if destination_url else self.destination_url
        self._elementParsed.write(
            destination_url, encoding="utf-8", default_namespace=""
        )

    def _view_box_parser(self):
        self._viewbox_attr = self._root.attrib["viewBox"].split(" ")
        self._viewBox = {
            "x": self._viewbox_attr[0],
            "y": self._viewbox_attr[1],
            "width": self._viewbox_attr[2],
            "height": self._viewbox_attr[3],
        }

    def set_view_box(
        self,
        x: Number = None,
        y: Number = None,
        width: Number = None,
        height: Number = None,
    ):
        if isNumber(x):
            self._viewBox["x"] = str(x)

        if isNumber(y):
            self._viewBox["y"] = str(x)

        if isNumber(width):
            self._viewBox["width"] = str(width)

        if isNumber(height):
            self._viewBox["height"] = str(height)

        self._viewbox_attr = " ".join(self._viewBox.values())
        self._root.attrib["viewBox"] = self._viewbox_attr

    def set_sizes(self, width: Number = None, height: Number = None):
        self._root.attrib["width"] = str(width) if width else self.viewBox["widht"]
        self._root.attrib["height"] = str(height) if width else self.viewBox["height"]
        self._root.attrib["width"] += "px"
        self._root.attrib["height"] += "px"

    @property
    def viewBox(self):
        return self._viewBox


if __name__ == "__main__":
    images_manipulation(images_url, source_url)
