#!/usr/bin/env python
# -*- coding: utf-8 -*-
FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'

DIRECTIONS = (
    (-1, -1),   (0, -1),    (1, -1),
    (-1, 0),                (1, 0),
    (-1, 1),    (0, 1),     (1, 1),
)


class DirectionalCursor:
    def __init__(self, x, y, direction):
        self.x, self.y, self.d_x, self.d_y = x, y, direction[0], direction[1]

    def __iter__(self):
        return self

    def __next__(self):
        self.x += self.d_x
        self.y += self.d_y
        return self


class WaitingAreaPart1:
    def __init__(self, layout):
        self.layout = layout

    def __iter__(self):
        return self

    def __next__(self):
        new_layout = [''.join(self.update_seat(x, y) for x in range(len(self.layout[0])))
                      for y in range(len(self.layout))]
        if new_layout == self.layout:
            raise StopIteration
        else:
            self.layout = new_layout

        return self

    def __str__(self):
        return '\n'.join(self.layout)

    def update_seat(self, x, y):
        if self.layout[y][x] == FLOOR:
            return FLOOR
        elif self.layout[y][x] == EMPTY_SEAT:
            return OCCUPIED_SEAT if self.occupied_adjacent_seats(x, y) == 0 else EMPTY_SEAT
        elif self.layout[y][x] == OCCUPIED_SEAT:
            # While the rule is 4 or more, we are simplifying by counting
            # the "target" seat, which is occupied.
            return EMPTY_SEAT if self.occupied_adjacent_seats(x, y) >= 5 else OCCUPIED_SEAT

    def occupied_adjacent_seats(self, x, y):
        return ''.join(line[max(x - 1, 0):x + 2]
                       for line in self.layout[max(y - 1, 0):y + 2]).count(OCCUPIED_SEAT)

    def occupied_seats(self):
        return ''.join(self.layout).count(OCCUPIED_SEAT)


class WaitingAreaPart2:
    SCORE = {OCCUPIED_SEAT: 1, EMPTY_SEAT: 0}

    def __init__(self, layout):
        self.layout = layout
        self.layout_height = len(layout)
        self.layout_width = len(layout[0])

    def __iter__(self):
        return self

    def __next__(self):
        new_layout = [''.join(self.update_seat(x, y) for x in range(len(self.layout[0])))
                      for y in range(len(self.layout))]
        if new_layout == self.layout:
            raise StopIteration
        else:
            self.layout = new_layout

        return self

    def __str__(self):
        return '\n'.join(self.layout)

    def update_seat(self, x, y):
        if self.layout[y][x] == FLOOR:
            return FLOOR
        elif self.layout[y][x] == EMPTY_SEAT:
            return OCCUPIED_SEAT if self.occupied_visible_seats(x, y) == 0 else EMPTY_SEAT
        elif self.layout[y][x] == OCCUPIED_SEAT:
            # While the rule is 4 or more, we are simplifying by counting
            # the "target" seat, which is occupied.
            return EMPTY_SEAT if self.occupied_visible_seats(x, y) >= 5 else OCCUPIED_SEAT

    def occupied_visible_seats(self, x, y):
        occupied = 0
        for direction in DIRECTIONS:
            cursor = DirectionalCursor(x, y, direction)
            for position in cursor:
                if (position.x < 0
                        or position.y < 0
                        or position.x >= self.layout_width
                        or position.y >= self.layout_height):
                    break
                try:
                    seat = self.layout[position.y][position.x]
                except IndexError:
                    break

                if seat in self.SCORE:
                    occupied += self.SCORE[seat]
                    break

        return occupied

    def occupied_seats(self):
        return ''.join(self.layout).count(OCCUPIED_SEAT)


def main(_args):
    layout = [line.strip() for line in open("input.txt", "r").readlines()]

    # Simulate your seating area by applying the seating rules repeatedly until
    # no seats change state. How many seats end up occupied?
    waiting_area = WaitingAreaPart1(layout)
    w = None
    for w in waiting_area:
        pass

    first_answer = w.occupied_seats()
    print("The first answer is: " + str(first_answer))

    # Given the new visibility method and the rule change for occupied seats
    # becoming empty, once equilibrium is reached, how many seats end up
    # occupied?
    waiting_area = WaitingAreaPart2(layout)
    for w in waiting_area:
        pass

    second_answer = w.occupied_seats()
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
