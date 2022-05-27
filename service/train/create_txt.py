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


def prepare_data(mark: Path):
    logger.debug(mark)


def create_file(name: Path, box: str) -> None:
    with open(name, 'w') as label:
        label.write(box)


def run():
    marks = get_json(base_marks)
    for mark in marks:
        
        prepare_data(mark)


run()
