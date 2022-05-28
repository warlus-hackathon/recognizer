import logging
import json
from pathlib import Path
from typing import Any

import cv2

logger = logging.getLogger(__name__)

base_images = Path('service/train/data/warlus/images')
image_path = Path('service/images/31.jpg')
markup = Path('service/markup/31.txt')
new_path = Path('service/images/_31.jpg')
base_marks = Path('dataset/markup')

def get_size(file_name: Path) -> tuple[int, int]:
    image_path = Path(base_images, f'{file_name}.jpg')
    image = cv2.imread(str(image_path))
    logger.debug(file_name)
    return image.shape

def get_json(marks_path: Path) -> list[Path]:
    return [mark_file for mark_file in marks_path.iterdir()]

def photo_size():
    json_list = get_json(base_marks)
    for json_file in json_list:            
        size = (1, 1)
        name = json_file.stem
        if name == 'categories':
            continue
        size = get_size(name)[:2]
        return size

def draw_box(image_path: Path, boxes: list):
    ph_h, ph_w = photo_size()    
    image = cv2.imread(str(image_path))
    for box in boxes:        
        _, left_x, left_y, width, height = box.split(' ')
        left_x = int(round(float(left_x)*ph_w, 0))
        left_y = int(round(float(left_y)*ph_h))
        width = int(round(float(width)*ph_w))
        height = int(round(float(height)*ph_h))        
        left_bottom = (left_x, left_y)
        right_bottom = (left_x + width, left_y + height)
        print(f'left: {left_bottom}\nright: {right_bottom}')
        cv2.rectangle(image, left_bottom, right_bottom, (0, 255, 0), 3)
    cv2.imwrite(str(new_path), image)


def read_boxes(markup: Path) -> list[str]:
    with open(markup, 'r') as marks:        
        marks_list = marks.readlines()    
    return marks_list

def run():
    boxes = read_boxes(markup)    
    draw_box(image_path, boxes)

run()