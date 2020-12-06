#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(_args):
    # Groups are separated by a blank line, which is two consecutive newlines.
    # For ease of use, we turn each person's answers into a set of answers.
    groups = [[set(p) for p in group.splitlines()]
              for group in open("input.txt", "r").read().split("\n\n")]

    # For each group, count the number of questions to which anyone answered
    # "yes". What is the sum of those counts?
    first_answer = sum(len(set.union(*group)) for group in groups)
    print("The first answer is: " + str(first_answer))

    # For each group, count the number of questions to which everyone answered
    # "yes". What is the sum of those counts?
    second_answer = sum(len(set.intersection(*group)) for group in groups)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
