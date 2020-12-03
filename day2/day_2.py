#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

PATTERN = re.compile(r"^(\d*)-(\d*) (\w): (\w*)$")


def part1(line):
    # The specified character should appear between MIN_COUNT and MAX_COUNT
    # number of times in the password.
    min_count, max_count, char, password = PATTERN.findall(line)[0]
    return int(min_count) <= password.count(char) <= int(max_count)


def part2(line):
    # The character should appear at the first or second index in the password,
    # but not both. Since indexes start at 1, we need to offset them.
    idx1, idx2, char, password = PATTERN.findall(line)[0]
    return (password[int(idx1) - 1] == char) ^ (password[int(idx2) - 1] == char)


def main(_args):
    # How many passwords are valid according to their policies?
    first_answer = sum(part1(line) for line in open("input.txt", "r").readlines())
    print("The first answer is: " + str(first_answer))

    # How many passwords are valid according to the new interpretation of the policies?
    second_answer = sum(part2(line) for line in open("input.txt", "r").readlines())
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
