#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


COLOUR_NAME = re.compile(r"^.*(?= bags contain)")
SUB_BAGS = re.compile(r"((\d) (.*?) (?=bag))")


class Bag:
    def __init__(self, s):
        self.name = COLOUR_NAME.search(s).group()
        self.bags = [(int(item.group(2)), item.group(3)) for item in SUB_BAGS.finditer(s)]

    def __contains__(self, item):
        return any(item == bag for (_, bag) in self.bags)


def main(_args):
    bags = [Bag(s) for s in open("input.txt", "r").readlines()]

    # How many bag colors can eventually contain at least one shiny gold bag?
    # (The list of rules is quite long; make sure you get all of it.)
    to_search = [bag for bag in bags if "shiny gold" in bag]
    found = set()

    while to_search:
        new_bag = to_search.pop()
        found.add(new_bag.name)
        to_search.extend((bag for bag in bags if new_bag.name in bag and bag.name not in found))

    first_answer = len(found)
    print("The first answer is: " + str(first_answer))

    # How many individual bags are required inside your single shiny gold bag?
    #
    # Turn the list into a dictionary to speed up lookups.
    bags_dict = dict((b.name, b.bags) for b in bags)
    to_search = bags_dict["shiny gold"]
    second_answer = 0

    while to_search:
        (c, new_bag_name) = to_search.pop()
        second_answer += c
        to_search.extend((c * sub_bag_count, sub_bag_name)
                         for (sub_bag_count, sub_bag_name) in bags_dict[new_bag_name])

    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
