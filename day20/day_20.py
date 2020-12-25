#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from functools import reduce
import operator
import re


SEA_MONSTER = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


def count_sea_monsters(image):
    # Scan through each line for possible matches, offsetting the indexes of the
    # matches. The intersection of all three sets of matches (offset) yields
    # every sea monster that can be found.
    head = re.compile(r"(?=..................#.)")
    body = re.compile(r"(?=#....##....##....###)")
    legs = re.compile(r"(?=.#..#..#..#..#..#...)")

    head_matches = set()
    body_matches = set()
    legs_matches = set()

    for line_idx, line in enumerate(image):
        for m in head.finditer(line):
            head_matches.add((line_idx, m.start()))
        for b in body.finditer(line):
            body_matches.add((line_idx - 1, b.start()))
        for l in legs.finditer(line):
            legs_matches.add((line_idx - 2, l.start()))

    return len(head_matches.intersection(body_matches).intersection(legs_matches))


class Tile:
    def __init__(self, data):
        lines = data.splitlines()
        self.number = int(lines[0][5:9])
        self.image = [line.strip() for line in lines[1:]]

    def border_less_image(self):
        return [''.join(line[1:-1]) for line in self.image[1:-1]]

    def borders(self):
        return {
            'top': self.top_border(),
            'bottom': self.bottom_border(),
            'left': self.left_border(),
            'right': self.right_border(),
        }

    def top_border(self):
        return self.image[0]

    def bottom_border(self):
        return self.image[-1]

    def left_border(self):
        return ''.join(line[0] for line in self.image)

    def right_border(self):
        return ''.join(line[-1] for line in self.image)

    def align_top_border(self, border):
        while self.top_border() != border:
            if self.top_border()[::-1] == border:
                self.flip_left_right()
            else:
                self.rotate_clockwise()

    def align_left_border(self, border):
        while self.left_border() != border:
            if self.left_border()[::-1] == border:
                self.flip_upside_down()
            else:
                self.rotate_clockwise()

    def flip_upside_down(self):
        self.image = self.image[::-1]

    def flip_left_right(self):
        self.image = [line[::-1] for line in self.image]

    def rotate_clockwise(self):
        self.image = [''.join(line) for line in zip(*self.image[::-1])]

    def rotate_counter_clockwise(self):
        self.image = [''.join(line) for line in zip(*self.image)][::-1]

    def __str__(self):
        return "\n".join(self.image)


def main(_args):
    tiles = [Tile(data) for data in open("input.txt", "r").read().split("\n\n") if data]

    # Assemble the tiles into an image. What do you get if you multiply together
    # the IDs of the four corner tiles?
    borders_map = defaultdict(list)
    for tile in tiles:
        for border in tile.borders().values():
            if border[::-1] in borders_map:
                borders_map[border[::-1]].append(tile)
            else:
                borders_map[border].append(tile)

    # Corner will only share two borders. Sides will have one. So, we can find
    # all the borders that belong to only one tile.
    singles = [border for border, t in borders_map.items() if len(t) == 1]
    corners = [tile for tile in tiles
               if 2 == sum(border in singles or border[::-1] in singles
                           for border in tile.borders().values()) == 2]
    first_answer = reduce(operator.mul, (tile.number for tile in corners))
    print("The first answer is: " + str(first_answer))

    # How many # are not part of a sea monster?
    # Start with a corner, which we can declare as top-left. Then it's only a
    # matter of aligning the remaining tiles.
    top_left = corners[0]
    if max(len(borders_map[top_left.top_border()]),
           len(borders_map[top_left.top_border()[::-1]])) == 2:
        top_left.flip_upside_down()

    if max(len(borders_map[top_left.left_border()]),
           len(borders_map[top_left.left_border()[::-1]])) == 2:
        top_left.flip_left_right()

    left_most = top_left
    ordered_tiles = []
    while left_most:
        bottom_border = left_most.bottom_border()
        line = []
        current = left_most

        # Prep the next line, not forgetting to align the tiles first.
        bottom_tiles = borders_map[bottom_border] + borders_map[bottom_border[::-1]]
        try:
            left_most = next(tile for tile in bottom_tiles if tile != left_most)
            left_most.align_top_border(current.bottom_border())
        except StopIteration:
            left_most = None

        # Add tiles to this line, aligning them at each step.
        while current:
            right_border = current.right_border()
            line.append(current)
            right_tiles = borders_map[right_border] + borders_map[right_border[::-1]]
            try:
                current = next(tile for tile in right_tiles if tile != current)
                current.align_left_border(right_border)
            except StopIteration:
                current = None

        ordered_tiles.append(line)

    # I'm getting lazy.
    image = []
    for idx in range(len(ordered_tiles)):
        image.extend(list(((''.join(a for a in line)
                            for line in zip(*[tile.border_less_image()
                                              for tile in ordered_tiles[idx]])))))

    # Iterate through the different orientations until we are able to find sea
    # monsters.
    sea_monsters = count_sea_monsters(image) + count_sea_monsters(image[::-1])
    while sea_monsters == 0:
        image = [''.join(line) for line in zip(*image[::-1])]
        sea_monsters = count_sea_monsters(image) + count_sea_monsters(image[::-1])

    # We're assuming that the sea monster do not overlap in this case.
    second_answer = ''.join(image).count('#') - sea_monsters * ''.join(SEA_MONSTER).count('#')
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
