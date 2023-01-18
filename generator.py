import os
import random

from tree import (
    Rect,
    split_tree_of_rectangles,
    SplitRectangleError
)
from preview import create_preview

MAP_ARRAY = []


def update_rooms(node):
    if node is None:
        return

    if node.is_leaf:
        room = node.data.room

        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                MAP_ARRAY[y][x] = "1"
        for y in range(room.y, room.y + room.height):
            if MAP_ARRAY[y][room.x - 1] == "0":
                MAP_ARRAY[y][room.x - 1] = "3"
            if MAP_ARRAY[y][room.x + room.width] == "0":
                MAP_ARRAY[y][room.x + room.width] = "4"
        for x in range(room.x, room.x + room.width):
            if MAP_ARRAY[room.y - 1][x] == "0":
                MAP_ARRAY[room.y - 1][x] = "5"
            if MAP_ARRAY[room.y + room.height][x] == "0":
                MAP_ARRAY[room.y + room.height][x] = "6"
    else:
        # create path between leaf's centers (nodes not rooms!)
        l1 = node.left.data
        l2 = node.right.data

        c1 = (l1.x + int(l1.width / 2), l1.y + int(l1.height / 2))
        c2 = (l2.x + int(l2.width / 2), l2.y + int(l2.height / 2))

        if c1[0] == c2[0]:
            x = c1[0]
            for y in range(c1[1], c2[1]):
                if MAP_ARRAY[y][x - 1] not in "12":
                    if MAP_ARRAY[y][x - 1] in "4":
                        MAP_ARRAY[y][x - 1] = "|"
                    elif MAP_ARRAY[y][x - 1] in "5":
                        MAP_ARRAY[y][x - 1] = "J"
                    elif MAP_ARRAY[y][x - 1] in "6":
                        MAP_ARRAY[y][x - 1] = "7"
                    else:
                        MAP_ARRAY[y][x - 1] = "3"
                if MAP_ARRAY[y][x + 1] not in "12":
                    if MAP_ARRAY[y][x + 1] in "3":
                        MAP_ARRAY[y][x + 1] = "|"
                    elif MAP_ARRAY[y][x + 1] in "5":
                        MAP_ARRAY[y][x + 1] = "L"
                    elif MAP_ARRAY[y][x + 1] in "6":
                        MAP_ARRAY[y][x + 1] = "Г"
                    else:
                        MAP_ARRAY[y][x + 1] = "4"
                MAP_ARRAY[y][x] = "2"
        if c1[1] == c2[1]:
            y = c1[1]
            for x in range(c1[0], c2[0]):
                if MAP_ARRAY[y - 1][x] not in "12":
                    if MAP_ARRAY[y - 1][x] in "3":
                        MAP_ARRAY[y - 1][x] = "J"
                    elif MAP_ARRAY[y - 1][x] in "4":
                        MAP_ARRAY[y - 1][x] = "L"
                    elif MAP_ARRAY[y - 1][x] in "6":
                        MAP_ARRAY[y - 1][x] = "-"
                    else:
                        MAP_ARRAY[y - 1][x] = "5"
                if MAP_ARRAY[y + 1][x] not in "12":
                    if MAP_ARRAY[y + 1][x] in "3":
                        MAP_ARRAY[y + 1][x] = "7"
                    elif MAP_ARRAY[y + 1][x] in "4":
                        MAP_ARRAY[y + 1][x] = "Г"
                    elif MAP_ARRAY[y + 1][x] in "5":
                        MAP_ARRAY[y + 1][x] = "-"
                    else:
                        MAP_ARRAY[y + 1][x] = "6"
                MAP_ARRAY[y][x] = "2"
    flag = True
    while flag:
        try:
            update_rooms(node.left)
        except RecursionError:
            print('*', end='')
        finally:
            flag = False
    flag = True
    while flag:
        try:
            update_rooms(node.right)
        except RecursionError:
            print('*', end='')
        finally:
            flag = False


def create_map(m_w=50, m_h=50, options=None):
    if options is None:
        options = {
            'padding': 1,
            'min_wall_size': 2,
            'min_walls_ratio': 0.4,
            'min_area_percent': 0.3
        }
    default_options = options.copy()

    map_width = m_w
    map_height = m_h

    splits = 5

    maps_path = './maps'
    map_format = 'level{}.map'

    wrap_rect = Rect(0, 0, map_width, map_height, default_options)
    tree = None
    while tree is None:
        try:
            tree = split_tree_of_rectangles(wrap_rect, splits, default_options)
        except SplitRectangleError:
            print('.', end='')

    for y in range(0, map_height):
        row = []
        for x in range(0, map_width):
            row.append("0")
        MAP_ARRAY.append(row)

    update_rooms(tree)

    while True:
        a = random.randrange(0, len(MAP_ARRAY) - 1)
        b = random.randrange(0, len(MAP_ARRAY[0]) - 1)
        if MAP_ARRAY[a][b] == "1":
            MAP_ARRAY[a][b] = "@"
            break

    while True:
        a = random.randrange(0, len(MAP_ARRAY) - 1)
        b = random.randrange(0, len(MAP_ARRAY[0]) - 1)
        if MAP_ARRAY[a][b] == "1":
            MAP_ARRAY[a][b] = "#"
            break

    if not os.path.exists(maps_path):
        os.mkdir(maps_path)

    maps_files = [
        f for f in os.listdir(maps_path)
        if f.endswith('.map') and os.path.isfile(os.path.join(maps_path, f))
    ]
    maps_count = len(maps_files)

    new_map_path = os.path.join(maps_path, map_format.format(maps_count + 1))
    with open(new_map_path, 'w') as map_file:
        for r in MAP_ARRAY:
            for t in r:
                map_file.write(t)
            map_file.write('\n')

    create_preview(new_map_path, map_width, map_height, 2)

    print('\nSuccess: new map ({}x{}): {}'.format(map_width, map_height, new_map_path))
    print('Saved maps: {}'.format(maps_count + 1))
    return maps_count + 1
