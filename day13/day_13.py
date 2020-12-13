#!/usr/bin/env python
# -*- coding: utf-8 -*-
OUT_OF_SERVICE = 'x'


def extended_euclidean_algorithm(a, b):
    # Returns (b, x0, y0) such that a * x0 + b * y0 = g, where g is the greatest
    # common divisor.
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1

    return b, x0, y0


def main(_args):
    with open("input.txt", "r") as f:
        departure_time = int(f.readline())
        buses = f.readline().split(',')

    # What is the ID of the earliest bus you can take to the airport multiplied
    # by the number of minutes you'll need to wait for that bus?
    # If we use the remainder directly, we'll get how many minutes since it
    # last departed; using the negative departure time will yield the correct
    # number of minutes to wait.
    wait_time, bus = min((-departure_time % int(bus), int(bus))
                         for bus in buses if bus != OUT_OF_SERVICE)
    first_answer = wait_time * bus
    print("The first answer is: " + str(first_answer))

    # What is the earliest timestamp such that all of the listed bus IDs depart
    # at offsets matching their positions in the list?
    bus_offsets = ((-idx % int(bus), int(bus))
                   for idx, bus in enumerate(buses) if bus != OUT_OF_SERVICE)

    # For a two equations system with n1 and n2 coprime:
    # x = a1 (mod n1)
    # x = a2 (mod n2)
    #
    # We can find the value x by:
    # x = a1m2n2 + a2m1n1
    #
    # where m1 and m2 are given by the extended Euclidean algorithm.
    #
    # This yields a new equivalence relation (a, n) to build a two equations
    # system with the next equivalence relation (bus).
    a1, n1 = 0, 1
    for a2, n2 in bus_offsets:
        g, m1, m2 = extended_euclidean_algorithm(n1, n2)
        a1 = a1 * m2 * n2 + a2 * m1 * n1 % (n1 * n2)
        n1 = n1 * n2

    second_answer = a1 % n1
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
