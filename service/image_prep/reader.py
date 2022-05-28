import logging
import json
from pathlib import Path
from typing import Any

import cv2

logger = logging.getLogger(__name__)

images = Path('service/image_prep/images/11_0_2.jpg')
markup = Path('service/image_prep/labels/11_0_2.txt')
marked_img = Path('service/image_prep/marked_img/_11_0_2.jpg')


def draw_box(image_path: Path, boxes: list):
    image = cv2.imread(str(image_path))    
    ph_h, ph_w = image.shape[:2]    
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
    cv2.imwrite(str(marked_img), image)


def read_boxes(markup: Path) -> list[str]:
    with open(markup, 'r') as marks:        
        marks_list = marks.readlines()    
    return marks_list

def run():
    boxes = read_boxes(markup)    
    draw_box(images, boxes)

run()