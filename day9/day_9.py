#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque


PREAMBLE_LENGTH = 25


def main(_args):
    inputs = [int(line) for line in open("input.txt", "r").readlines()]

    # The first step of attacking the weakness in the XMAS data is to find the
    # first number in the list (after the preamble) which is not the sum of two
    # of the 25 numbers before it. What is the first number that does not have
    # this property?
    first_answer = 0
    preamble = deque(inputs[:PREAMBLE_LENGTH], PREAMBLE_LENGTH)
    for number in inputs[PREAMBLE_LENGTH:]:
        if not any(number - p in preamble for p in preamble):
            first_answer = number
            break
        else:
            preamble.append(number)

    print("The first answer is: " + str(first_answer))

    # What is the encryption weakness in your XMAS-encrypted list of numbers?
    numbers = iter(inputs)
    contiguous_numbers = deque()
    s = sum(contiguous_numbers)

    # Recreate a sliding window using a `deque`.
    while s != first_answer:
        if s < first_answer:
            contiguous_numbers.append(next(numbers))
        elif s > first_answer:
            contiguous_numbers.popleft()

        s = sum(contiguous_numbers)

    second_answer = min(contiguous_numbers) + max(contiguous_numbers)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
