import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_images = Path('service/train/data/warlus/images')
fraction = 10
train_txt = Path('service/train/data/warlus/train.txt')
test_txt = Path('service/train/data/warlus/val.txt')


def counter() -> tuple[list[Path], int]:
    images = list(base_images.iterdir())
    return (images, len(images))


def create_txt(images: list[Path], images_num: int, train_num: int) -> None:
    train_list = []
    test_list = []
    for num, image in enumerate(images):
        if num < train_num:
            train_list.append(f'{image}\n')
        else:
            test_list.append(f'{image}\n')
    make_file(train_list, test_list)
    logger.debug(test_list)



def make_file(train: list[str], test: list[str]) -> None:
    
    with open(train_txt, 'w') as config:
        config.writelines(train)

    with open(test_txt, 'w') as config:
        config.writelines(test)


def run():
    images, image_numbers = counter()
    
    test_num = image_numbers // fraction
    train_num = image_numbers - test_num

    logger.debug(image_numbers)

    create_txt(images, image_numbers, train_num)


run()
