import os
from PIL import Image


def rgb(tile_sign):
    if tile_sign in "03456":
        return 118, 165, 204
    if tile_sign == '1':
        return 74, 103, 127
    if tile_sign == '2':
        return 224, 231, 255
    return 0, 0, 0


def create_preview(mappath, width, height, zoom=1):
    im = None
    img_data = []
    im = Image.new('RGB', (width, height))

    with open(mappath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = list(line.strip('\n'))
            img_data = img_data + list(map(rgb, line))

    im.putdata(img_data)
    im = im.resize((int(width * zoom), int(height * zoom)), Image.ANTIALIAS)

    head, ext = os.path.splitext(mappath)
    new_img_path = '{}{}'.format(head, '.png')
    im.save(new_img_path)
