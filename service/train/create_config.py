import logging
from pathlib import Path
from random import randint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_images = Path('service/train/data/warlus/images')
fraction = 0.2
train_txt = Path('service/train/data/warlus/train.txt')
test_txt = Path('service/train/data/warlus/val.txt')


def counter() -> tuple[list[Path], int]:
    images = list(base_images.iterdir())
    return (images, len(images))


def create_txt(images: list[Path], test_num: int) -> None:
    train_list = []
    test_list = []
    for image in images:
        if randint(1, 2) == 1 and len(test_list) < test_num:
            test_list.append(f'{image}\n')
        else:
            train_list.append(f'{image}\n')
    make_file(train_list, test_list)
    logger.debug(test_list)


def make_file(train: list[str], test: list[str]) -> None:
    
    with open(train_txt, 'w') as config:
        config.writelines(train)

    with open(test_txt, 'w') as config:
        config.writelines(test)


def run():
    images, image_numbers = counter()
    
    test_num = round(image_numbers * fraction, 0)    

    logger.debug(image_numbers)

    create_txt(images, test_num)


run()
