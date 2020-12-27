#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter, namedtuple
import re

DIRECTIONS = re.compile(r"se|sw|ne|nw|e|w")
DIRECTION_VECTORS = {
    'e': (-1, 1, 0),
    'se': (-1, 0, 1),
    'sw': (0, -1, 1),
    'w': (1, -1, 0),
    'nw': (1, 0, -1),
    'ne': (0, 1, -1),
}


class Coordinates(namedtuple('Coordinates', ['x', 'y', 'z'])):
    def __add__(self, other):
        return Coordinates(self.x + other[0],
                           self.y + other[1],
                           self.z + other[2])


class Floor:
    def __init__(self, initial):
        self.plan = set()
        for line in initial:
            tile = Coordinates(0, 0, 0)
            for direction in DIRECTIONS.finditer(line):
                tile = tile + DIRECTION_VECTORS[direction.group()]

            try:
                self.plan.remove(tile)
            except KeyError:
                self.plan.add(tile)

    def count_black_tiles(self):
        return len(self.plan)

    def __iter__(self):
        return self

    def __next__(self):
        # Generate a count of the number of neighboring tiles that are black.
        black_tiles = Counter(
            tile + direction for tile in self.plan
            for direction in DIRECTION_VECTORS.values()
        )

        new_plan = set(
            tile for tile, neighbors in black_tiles.items()
            # If it has exactly 2 neighbours, it either stays or becomes black.
            # If it has only 1 neighbour, it remains black but does not flip.
            if neighbors == 2 or (neighbors == 1 and tile in self.plan)
        )

        self.plan = new_plan


def main(_args):
    # Go through the renovation crew's list and determine which tiles they need
    # to flip. After all of the instructions have been followed, how many tiles
    # are left with the black side up?
    floor = Floor(line for line in open("input.txt", "r").readlines())
    print("The first answer is: " + str(floor.count_black_tiles()))

    # How many tiles will be black after 100 days?
    for _ in range(100):
        next(floor)

    print("The second answer is: " + str(floor.count_black_tiles()))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
