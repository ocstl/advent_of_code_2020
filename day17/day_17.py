#!/usr/bin/env python
# -*- coding: utf-8 -*-
ACTIVE = '#'
INACTIVE = '.'


class PocketDimension:
    def __init__(self, initial_state):
        self.cycle = 0
        self.state = [[[tile == ACTIVE for tile in line.strip()] for line in initial_state.readlines()]]

    def __iter__(self):
        return self

    def __next__(self):
        l_z = len(self.state)
        l_y = len(self.state[0])
        l_x = len(self.state[0][0])
        new_state = [[[
            (self.active_cube(x, y, z) and self.count_neighbours(x, y, z) in (3, 4))
            or self.count_neighbours(x, y, z) == 3 for x in range(-1, l_x + 1)
        ] for y in range(-1, l_y + 1)
        ] for z in range(-1, l_z + 1)]

        self.state = new_state
        self.cycle += 1

        return self

    def __str__(self):
        return '\n\n'.join('\n'.join(''.join(ACTIVE if x else INACTIVE for x in y)
                                     for y in z)
                           for z in self.state)

    def active_cube(self, x, y, z):
        if x < 0 or y < 0 or z < 0:
            return False

        try:
            return self.state[z][y][x]
        except IndexError:
            return False

    def count_neighbours(self, x, y, z):
        return sum(coord for dim_slice in self.state[max(z - 1, 0):z + 2]
                   for line in dim_slice[max(y - 1, 0):y + 2]
                   for coord in line[max(x - 1, 0):x + 2])

    def count_active_cubes(self):
        return sum(sum(sum(x for x in y) for y in z) for z in self.state)


class PocketDimension4D:
    def __init__(self, initial_state):
        self.cycle = 0
        self.state = [[[[tile == ACTIVE for tile in line.strip()] for line in initial_state.readlines()]]]

    def __iter__(self):
        return self

    def __next__(self):
        l_w = len(self.state)
        l_z = len(self.state[0])
        l_y = len(self.state[0][0])
        l_x = len(self.state[0][0][0])
        new_state = [[[[
            (self.active_cube(x, y, z, w) and self.count_neighbours(x, y, z, w) in (3, 4))
            or self.count_neighbours(x, y, z, w) == 3 for x in range(-1, l_x + 1)
        ] for y in range(-1, l_y + 1)
        ] for z in range(-1, l_z + 1)
        ] for w in range(-1, l_w + 1)]

        self.state = new_state
        self.cycle += 1

        return self

    def __str__(self):
        return '\n\n'.join('\n\n'.join('\n'.join(''.join(ACTIVE if x else INACTIVE for x in y)
                                                 for y in z)
                                       for z in w)
                           for w in self.state)

    def active_cube(self, x, y, z, w):
        if x < 0 or y < 0 or z < 0 or w < 0:
            return False

        try:
            return self.state[w][z][y][x]
        except IndexError:
            return False

    def count_neighbours(self, x, y, z, w):
        return sum(coord for dim_slice in self.state[max(w - 1, 0):w + 2]
                   for surface in dim_slice[max(z - 1, 0):z + 2]
                   for line in surface[max(y - 1, 0):y + 2]
                   for coord in line[max(x - 1, 0):x + 2])

    def count_active_cubes(self):
        return sum(sum(sum(sum(x for x in y) for y in z) for z in w) for w in self.state)


def main(_args):

    # Starting with your given initial configuration, simulate six cycles.
    # How many cubes are left in the active state after the sixth cycle?
    dimension = PocketDimension(open("input.txt", "r"))
    for _ in range(6):
        next(dimension)

    first_answer = dimension.count_active_cubes()
    print("The first answer is: " + str(first_answer))

    # Starting with your given initial configuration, simulate six cycles in a
    # 4-dimensional space. How many cubes are left in the active state after
    # the sixth cycle?
    dimension_part2 = PocketDimension4D(open("input.txt", "r"))
    for _ in range(6):
        next(dimension_part2)

    second_answer = dimension_part2.count_active_cubes()
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
