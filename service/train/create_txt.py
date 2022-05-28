import json
import logging
from pathlib import Path
from typing import Any, Optional

import cv2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_marks = Path('service/markup')
base_images = Path('service/train/data/warlus/images')
target_marks = Path('service/train/data/warlus/labels')


def get_json(marks_path: Path) -> list[Path]:
    return [mark_file for mark_file in marks_path.iterdir()]


def box_calculate(work_box: list[float], size: tuple[int, int]) -> Optional[str]:
    box = work_box[:4]
    logger.debug(box)
    #size = (1, 1, 1, 1)
    left_x = box[0] / size[1]
    left_y = box[1] / size[0]
    width = box[2] / size[1]
    height = box[3] / size[0]
    row = '1 {0} {1} {2} {3}\n'.format(left_x, left_y, width, height)
    if left_x < 0 or left_y < 0 or width < 0 or height < 0:
        row = None
    if left_x > 1 or left_y > 1 or width > 1 or height > 1:
        row = None
    return row


def prepare_data(marks: list[dict[str, Any]], size: tuple[int, int], name: Path):
    marks_list = []
    for mark in marks:
        if not mark.get('bbox', False):
            continue
        row = box_calculate(mark['bbox'], size)
        if not row:
            continue
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
