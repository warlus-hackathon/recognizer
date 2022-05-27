import logging
import json
from pathlib import Path
from typing import Any


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_marks = Path('service/markup')
base_images = Path('service/images')
target_marks = Path('service/train/data/warlus/labels')


def get_json(marks_path: Path) -> list[Path]:
    return [mark_file for mark_file in marks_path.iterdir()]


def prepare_data(marks: list[dict[str, Any]], size: tuple[int, int], name: Path):
    marks_list = []
    for mark in marks:
        logger.debug(f'{mark}\n')
        if not mark.get('bbox', False):
            continue        
        row = ', '.join(list(map(str, mark['bbox'][:4])))
        row = f'1 {row}\n'
        marks_list.append(row)
    logger.debug(marks_list)
    create_file(name, marks_list)


def create_file(name: Path, rows: list[str]) -> None:
    new_name = Path(target_marks, f'{name}.txt')
    with open(new_name, 'w') as label:
        label.writelines(rows)


def run():
    json_list = get_json(base_marks)
    for json_file in json_list:
        with open(json_file, 'r') as j_file:
            marks = json.loads(j_file.read())
            size = (1, 1)
            name = json_file.stem
            prepare_data(marks, size, name)


run()
