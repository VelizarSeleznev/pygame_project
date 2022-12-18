from random import randint


class SplitRectangleError(Exception):
    pass


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class Rect:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self._area = None
        self._room = None

    @property
    def area(self):
        if self._area is None:
            self._area = self.width * self.height
        return self._area

    @property
    def room(self):
        if self._room is None:
            self._room = self.create_room()
        return self._room

    def create_room(self):
        padding = self.options['padding']
        min_wall_size = self.options['min_wall_size']
        min_walls_ratio = self.options['min_walls_ratio']
        min_area_percent = self.options['min_area_percent']

        x = randint(self.x + padding, self.x + int(self.width / 2))
        y = randint(self.y + padding, self.y + int(self.height / 2))

        width = randint(min_wall_size, self.x + self.width - x) - padding
        height = randint(min_wall_size, self.y + self.height - y) - padding

        if (height / width < min_walls_ratio or width / height < min_walls_ratio or
                width * height < min_area_percent * self.area):
            return self.create_room()

        return Rect(x, y, width, height, self.options)


def split_rect(rect, options):
    padding = options['padding']
    min_wall_size = options['min_wall_size']
    min_walls_ratio = options['min_walls_ratio']

    min_split_size = 2 * padding + min_wall_size

    # we don't want to split too small reactangle
    if rect.width < 2 * min_split_size or rect.height < 2 * min_split_size:
        raise SplitRectangleError()

    if randint(0, 1) == 0:  # split vertical
        r1 = Rect(
            rect.x, rect.y,
            randint(min_split_size, rect.width), rect.height,
            options
        )
        r2 = Rect(
            rect.x + r1.width, rect.y,
            rect.width - r1.width, rect.height,
            options
        )

        # retry if ratio is too small
        if r1.width / r1.height < min_walls_ratio or r2.width / r2.height < min_walls_ratio:
            return split_rect(rect, options)
    else:  # split horizontal
        r1 = Rect(
            rect.x, rect.y,
            rect.width, randint(min_split_size, rect.height),
            options
        )
        r2 = Rect(
            rect.x, rect.y + r1.height,
            rect.width, rect.height - r1.height,
            options
        )

        if r1.height / r1.width < min_walls_ratio or r2.height / r2.width < min_walls_ratio:
            return split_rect(rect, options)
    return r1, r2


def split_tree_of_rectangles(rect, step, options):
    tree = Node(rect)
    if step != 0:
        split = split_rect(rect, options)
        if split:
            tree.left = split_tree_of_rectangles(split[0], step - 1, options)
            tree.right = split_tree_of_rectangles(split[1], step - 1, options)
    return tree
