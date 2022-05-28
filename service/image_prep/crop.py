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
            coords = iou_check(box, part_sizes)
            if coords:
                rows.append(coords)
        if rows:
            save_txt(name, rows, save_path, part_num)
            return True
        return False


def iou_check(work_box, part_coords):    
    b_left, b_top, b_width, b_height = work_box
    b_right = b_left + b_width  
    b_bottom = b_top + b_height
    box_sizes = (b_left, b_top, b_right, b_bottom)

    b_area = b_width * b_height
    iou = get_iou(part_coords, box_sizes)
    if iou and iou > b_area * 0.5:        
        left, top, right, bottom = part_coords
        part_sizes = [right - left, bottom - top]
        rel_left = b_left - left if b_left > left else 0
        rel_top = b_top - top if b_top > top else 0
        rel_coords = scale_coords([rel_left, rel_top, b_width, b_height], part_sizes)        
        return rel_coords    


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
    post_txt = Path('service/train/data/warlus/labels')
    images = get_images(get_imgs)    
    for name, image in images:       
        json_path = Path(get_jsons, f'{name}.json')         
        parts_sizes = get_crop_sizes(image)
        for part in parts_sizes:
            created = create_txt(json_path, post_txt, part, name, image)
            if created:
                pass
                # save_imgs(image, part, post_crop_imgs, name)            


if __name__ == '__main__':
    main()
