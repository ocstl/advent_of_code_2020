#!/usr/bin/env python
# -*- coding: utf-8 -*-


MODULUS = 20201227
SUBJECT_NUMBER = 7


def get_loop_size(public_key):
    current = 1
    loop_size = 0
    while current != public_key:
        loop_size += 1
        current = (current * SUBJECT_NUMBER) % MODULUS

    return loop_size


def main(_args):
    public_keys = [int(d) for d in open("input.txt", "r").readlines()]

    # What encryption key is the handshake trying to establish?
    card_loop_size = get_loop_size(public_keys[0])
    first_answer = pow(public_keys[1], card_loop_size, MODULUS)

    print("The first answer is: " + str(first_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
