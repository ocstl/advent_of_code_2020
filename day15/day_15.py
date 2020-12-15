#!/usr/bin/env python
# -*- coding: utf-8 -*-
PUZZLE_INPUT = "2,0,6,12,1,3"


def nth_number_spoken(nth):
    # Indices start at 1, so we have to offset everything a little bit.
    numbers = [int(x) for x in PUZZLE_INPUT.split(",")]
    last_number = numbers.pop()
    start_idx = len(numbers) + 1
    numbers = {x: idx + 1 for idx, x in enumerate(numbers)}

    for idx in range(start_idx, nth):
        try:
            last_idx = numbers[last_number]
        except KeyError:
            last_idx = idx

        numbers[last_number] = idx
        last_number = idx - last_idx

    return last_number


def main(_args):
    # Given your starting numbers, what will be the 2020th number spoken?
    print("The first answer is: " + str(nth_number_spoken(2020)))

    # Given your starting numbers, what will be the 30000000th number spoken?
    print("The second answer is: " + str(nth_number_spoken(30000000)))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
