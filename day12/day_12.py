#!/usr/bin/env python
# -*- coding: utf-8 -*-

DIRECTIONS = 'NESW'
VECTORS = dict(zip(DIRECTIONS,
                   ((0, -1), (1, 0), (0, 1), (-1, 0))))


class Ship:
    def __init__(self):
        self.x, self.y = 0, 0
        self.direction = 'E'

    def manhattan_distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def execute_instruction(self, instruction):
        inst = instruction[0]
        amount = int(instruction[1:])

        if inst in VECTORS:
            self.move(VECTORS[inst], amount)
        elif inst == 'F':
            self.move(VECTORS[self.direction], amount)
        elif inst == 'R':
            self.turn_right(amount // 90)
        elif inst == 'L':
            self.turn_left(amount // 90)
        else:
            raise ValueError(instruction)

    def move(self, direction, amount):
        self.x += direction[0] * amount
        self.y += direction[1] * amount

    def turn_right(self, amount):
        self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) + amount) % len(DIRECTIONS)]

    def turn_left(self, amount):
        self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) - amount) % len(DIRECTIONS)]


class ShipWaypoint:
    def __init__(self):
        self.x, self.y = 0, 0
        self.waypoint = (10, -1)

    def manhattan_distances(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def execute_instruction(self, instruction):
        inst = instruction[0]
        amount = int(instruction[1:])

        if inst in VECTORS:
            self.move_waypoint(VECTORS[inst], amount)
        elif inst == 'F':
            self.move(amount)
        elif inst == 'R':
            self.rotate_waypoint_right(amount // 90)
        elif inst == 'L':
            self.rotate_waypoint_left(amount // 90)
        else:
            raise ValueError(instruction)

    def move_waypoint(self, direction, amount):
        self.waypoint = (self.waypoint[0] + amount * direction[0],
                         self.waypoint[1] + amount * direction[1])

    def move(self, amount):
        self.x += self.waypoint[0] * amount
        self.y += self.waypoint[1] * amount

    def rotate_waypoint_right(self, amount):
        for _ in range(amount):
            # This is equivalent to rotating a complex number.
            self.waypoint = (-1 * self.waypoint[1], self.waypoint[0])

    def rotate_waypoint_left(self, amount):
        for _ in range(amount):
            # This is equivalent to rotating a complex number.
            self.waypoint = (self.waypoint[1], -1 * self.waypoint[0])


def main(_args):
    # It might be a good idea to use complex numbers instead, but let's try with
    # integers.
    instructions = [line.strip() for line in open("input.txt", "r").readlines()]

    # Figure out where the navigation instructions lead. What is the Manhattan
    # distance between that location and the ship's starting position?
    ship = Ship()
    for inst in instructions:
        ship.execute_instruction(inst)

    first_answer = ship.manhattan_distance(0, 0)
    print("The first answer is: " + str(first_answer))

    # Figure out where the navigation instructions actually lead. What is the
    # Manhattan distance between that location and the ship's starting position?
    ship2 = ShipWaypoint()
    for inst in instructions:
        ship2.execute_instruction(inst)

    second_answer = ship2.manhattan_distances(0, 0)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
