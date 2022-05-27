import logging
import json
from pathlib import Path
from typing import Any

import cv2

logger = logging.getLogger(__name__)

image_path = Path('service/images/17.jpg')
markup = Path('service/markup/17.json')
new_path = Path('service/images/_17.jpg')


def draw_box(image_path: Path, boxes: list[int]):

    image = cv2.imread(str(image_path))
    for in_box in boxes:
        box = in_box['bbox']
        print(box)
        center_x, center_y, height, width, const = box
        left_bottom = (int(center_x), int(center_y))
        right_bottom = (int(center_x + height), int(center_y + width))
        print(f'left: {left_bottom}\nright: {right_bottom}')
        cv2.rectangle(image, left_bottom, right_bottom, (0, 255, 0), 3)
    cv2.imwrite(str(new_path), image)


def read_boxes(markup: Path) -> list[dict[str, Any]]:
    with open(markup, 'r') as marks:
        marks_dict = json.loads(marks.read())
    return marks_dict

def run():
    marks = read_boxes(markup)
    box = marks
    draw_box(image_path, box)

run()