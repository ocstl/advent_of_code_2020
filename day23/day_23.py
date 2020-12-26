#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain

INPUT = "469217538"


class CrabCup:
    def __init__(self, cups, slice_size=3):
        self.cups = {cup1: cup2 for cup1, cup2 in zip(cups, cups[1:] + [cups[0]])}
        self.smallest = min(cups)
        self.largest = max(cups)
        self.current = cups[0]
        self.slice_size = slice_size

    def __iter__(self):
        return self

    def __next__(self):
        # Get the cups to be picked up.
        picked_up = []
        for _ in range(self.slice_size):
            picked_up.append(self.cups[picked_up[-1] if picked_up else self.current])

        # Find the target.
        target = next(i for i in
                      chain(reversed(range(self.smallest, self.current)),
                            reversed(range(self.current, self.largest + 1)))
                      if i not in picked_up)

        # The current cup should point to the cup pointed at by the last picked
        # up cup; that cup should point to the one that was pointed at by the
        # target cup; and the target cup should point to the first cup that was
        # picked up.
        self.cups[self.current], self.cups[picked_up[-1]], self.cups[target] = (
            self.cups[picked_up[-1]], self.cups[target], self.cups[self.current]
        )

        self.current = self.cups[self.current]

    def cup_order(self, start=1):
        cups = [start]
        while len(cups) < len(self.cups):
            cups.append(self.cups[cups[-1]])

        return cups

    def clockwise_cup(self, cup):
        return self.cups[cup]


def main(_args):
    cups = [int(d) for d in INPUT]
    # Using your labeling, simulate 100 moves. What are the labels on the cups
    # after cup 1?
    game = CrabCup(cups)
    for turn in range(100):
        next(game)

    first_answer = ''.join(str(cup) for cup in game.cup_order() if cup != 1)
    print("The first answer is: " + first_answer)

    # Determine which two cups will end up immediately clockwise of cup 1.
    # What do you get if you multiply their labels together?
    million_cups = cups + list(range(max(cups) + 1, 1000001))
    game = CrabCup(million_cups)
    for turn in range(10000000):
        next(game)

    first_cup = game.clockwise_cup(1)
    second_cup = game.clockwise_cup(first_cup)
    second_answer = first_cup * second_cup
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
