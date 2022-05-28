import json
import os
from pathlib import Path

from PIL import Image

from iou import get_iou


def get_crop_sizes(image):
    width, height = image.size    
    sizes = []
    w, h = 416, 416
    cols = round(width / w)
    rows = round(height / h)    
    for col in range(cols):
        for row in range(rows):
            left = col * w
            top = row * h
            right = left + w
            bottom = top + h            
            sizes.append([(col, row), (left, top, right, bottom)])
    return sizes
    

def save_imgs(image, part, post_path, name):  
    part_num, sizes = part         
    crop_image = image.crop(sizes)        
    crop_image.save(
        post_path + '{0}_{1}_{2}.jpg'.format(name, part_num[1], part_num[0]),            
        quality=100,
    )


def get_images(path):
    images = []
    for fullpath in path.iterdir():        
        if os.path.isfile(fullpath):
            image = Image.open(fullpath)
            images.append([fullpath.stem, image])
    return images


def create_txt(json_file, save_path, part, name, image_size):
    part_num, part_sizes = part      
    with open(json_file, 'r') as j_file:
        marks = json.loads(j_file.read())
        rows = []
        for mark in marks:
            box = mark['bbox'][:4]
            if iou_check(box, part_sizes):
                rows.append(scale_coords(box, image_size.size))        
        if rows:
            save_txt(name, rows, save_path, part_num)
            return True
        return False


def iou_check(work_box, part_sizes):    
    b_left, b_top, b_width, b_height = work_box    
    box_sizes = (b_left, b_top, b_left + b_width, b_top + b_height)

    b_area = b_width * b_height
    iou = get_iou(part_sizes, box_sizes)
    if iou and iou > b_area * 0.5:
        return True    


def scale_coords(work_box: list[float], sizes: tuple[int, int]) -> str:    
    ph_w, ph_h = sizes
    left, top, right, bottom = work_box    
    left_x = left / ph_w
    left_y = top / ph_h
    width = right / ph_w
    height = bottom / ph_h    
    return '0 {0} {1} {2} {3}\n'.format(left_x, left_y, width, height)


def save_txt(name: str, rows: list[str], save_path: Path, part_num) -> None:
    new_name = Path(save_path, '{0}_{1}_{2}.txt'.format(name, part_num[1], part_num[0])) 
    with open(new_name, 'w') as label:
        label.writelines(rows)


def main():
    get_imgs = Path('dataset/images/')
    get_jsons = Path('dataset/markup/')
    post_crop_imgs = 'service/image_prep/images/'    
    post_txt = Path('service/image_prep/labels')
    images = get_images(get_imgs)    
    for name, image in images:       
        json_path = Path(get_jsons, f'{name}.json')         
        parts_sizes = get_crop_sizes(image)
        for part in parts_sizes:
            created = create_txt(json_path, post_txt, part, name, image)
            if created:
                save_imgs(image, part, post_crop_imgs, name)            


if __name__ == '__main__':
    main()
