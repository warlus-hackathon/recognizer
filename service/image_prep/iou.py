from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

# returns None if rectangles don't intersect
def area(a, b):  
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return float(dx*dy)


def get_iou(part_sizes, box_sizes):
    left, top, right, bottom = part_sizes
    ra = Rectangle(left, top, right, bottom)
    b_left, b_top, b_right, b_bottom = box_sizes
    rb = Rectangle(b_left, b_top, b_right, b_bottom)
    return area(ra, rb)
