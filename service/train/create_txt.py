import json
import logging
from pathlib import Path
from typing import Any

import cv2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_marks = Path('dataset/markup')
base_images = Path('service/train/data/warlus/images')
target_marks = Path('service/train/data/warlus/labels')


def get_json(marks_path: Path) -> list[Path]:
    return [mark_file for mark_file in marks_path.iterdir()]


def box_calculate(work_box: list[float], size: tuple[int, int]) -> str:
    box = work_box[:4]
    print(box)
    ph_h, ph_w = size
    left_x = box[0] / ph_w
    left_y = box[1] / ph_h
    width = box[2] / ph_w
    height = box[3] / ph_h    
    return '0 {0} {1} {2} {3}\n'.format(left_x, left_y, width, height)


def prepare_data(marks: list[dict[str, Any]], size: tuple[int, int], name: Path):
    marks_list = []
    for mark in marks:
        if not mark.get('bbox', False):
            continue
        row = box_calculate(mark['bbox'], size)
        marks_list.append(row)
    create_file(name, marks_list)


def create_file(name: Path, rows: list[str]) -> None:
    new_name = Path(target_marks, f'{name}.txt')
    with open(new_name, 'w') as label:
        label.writelines(rows)


def get_size(file_name: Path) -> tuple[int, int]:
    image_path = Path(base_images, f'{file_name}.jpg')
    image = cv2.imread(str(image_path))
    logger.debug(file_name)
    return image.shape


def run():
    json_list = get_json(base_marks)
    for json_file in json_list:
        with open(json_file, 'r') as j_file:
            marks = json.loads(j_file.read())
            size = (1, 1)
            name = json_file.stem
            if name == 'categories':
                continue
            size = get_size(name)[:2]
            prepare_data(marks, size, name)


run()
