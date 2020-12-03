#!/usr/bin/env python
# -*- coding: utf-8 -*-
TREE = '#'
OPEN = '.'


def main(_args):
    tree_map = [line.strip() for line in open("input.txt", "r").readlines()]
    # Since the map repeats horizontally, we can simply use a remainder to get the character at the proper index.
    horizontal_length = len(tree_map[0])

    def number_trees(horizontal_step, vertical_step):
        return sum(line[(idx * horizontal_step) % horizontal_length] == TREE
                   for idx, line in enumerate(tree_map[::vertical_step]))

    # Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you
    # encounter?
    first_answer = number_trees(3, 1)
    print("The first answer is: " + str(first_answer))

    # What do you get if you multiply together the number of trees encountered on each of the listed slopes?
    second_answer = (number_trees(1, 1)
                     * number_trees(3, 1)
                     * number_trees(5, 1)
                     * number_trees(7, 1)
                     * number_trees(1, 2))
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
