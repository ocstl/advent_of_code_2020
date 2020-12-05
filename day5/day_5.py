#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To convert the characters of a boarding pass into binary digits.
BINARY_CONVERTER = str.maketrans("BFRL", "1010")


class BoardingPass:
    def __init__(self, boarding_pass):
        s = boarding_pass.translate(BINARY_CONVERTER)
        self.row = int(s[0:7], 2)
        self.column = int(s[7:10], 2)

    def seat_id(self):
        return self.row * 8 + self.column


def main(_args):
    passes = [BoardingPass(line.strip())
              for line in open("input.txt", "r").readlines()]

    # As a sanity check, look through your list of boarding passes. What is the
    # highest seat ID on a boarding pass?
    first_answer = max(p.seat_id() for p in passes)
    print("The first answer is: " + str(first_answer))

    # Your seat wasn't at the very front or back, though; the seats with IDs +1
    # and -1 from yours will be in your list.
    # What is the ID of your seat?
    seat_ids = [p.seat_id() for p in passes]
    second_answer = (set(seat_id - 1 for seat_id in seat_ids)
                     .intersection((seat_id + 1 for seat_id in seat_ids))
                     .difference(seat_ids)
                     .pop())
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
