import logging
import json
from pathlib import Path
from typing import Any

import cv2

logger = logging.getLogger(__name__)

image_path = Path('service/images/11.jpg')
markup = Path('service/markup/11.json')


def draw_box(image_path: Path, box: list[int]):
    print(box)
    image = cv2.imread(str(image_path))
    
    cv2.rectangle(image, (, b), (a + width, b + height), (0, 255, 0), 3)


def read_boxes(markup: Path) -> list[dict[str, Any]]:
    with open(markup, 'r') as marks:
        marks_dict = json.loads(marks.read())
    return marks_dict

def run():
    marks = read_boxes(markup)
    box = marks[0]['bbox']
    draw_box(image_path, box)

run()