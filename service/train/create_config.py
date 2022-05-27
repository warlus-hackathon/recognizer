import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


base_images = Path('service/images')
fraction = 10
train_txt = Path('service/train/data/warlus/train.txt')
test_txt = Path('service/train/data/warlus/val.txt')


def counter() -> int:
    images = list(base_images.iterdir())
    return (images, len(images))


def create_txt(images: list[Path], image_num: int, train_num: int) -> None:
    


def run():
    images, image_numbers = counter()
    
    test_num = image_numbers // fraction
    train_num = image_numbers - test_num

    logger.debug(image_numbers)


run()
