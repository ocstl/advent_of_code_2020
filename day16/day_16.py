#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from copy import deepcopy
from functools import reduce
import operator
import re

FIELD = re.compile(r"^([ \w]+): (\d+-\d+) or (\d+-\d+)")
TICKET = re.compile(r"^([,\d]+)")


def main(_args):
    # Use a dict to map each value to a possible field; the defaultdict is to
    # generate a new set for each new value.
    possible_fields = defaultdict(set)
    tickets = list()

    for line in open("input.txt", "r").readlines():
        m = FIELD.match(line)
        t = TICKET.match(line)
        if m:
            field = m.group(1)
            for s in m.groups()[1:]:
                min_value = int(s.split("-")[0])
                max_value = int(s.split("-")[1])
                for v in range(min_value, max_value + 1):
                    possible_fields[v].add(field)
        elif t:
            tickets.append([int(n) for n in t.group().split(",")])

    # The first ticket is mine, the rest are nearby tickets.
    my_ticket, tickets = tickets[0], tickets[1:]

    # Consider the validity of the nearby tickets you scanned. What is your
    # ticket scanning error rate?
    first_answer = sum(v for t in tickets
                       for v in t
                       if v not in possible_fields)
    print("The first answer is: " + str(first_answer))

    # Once you work out which field is which, look for the six fields on your
    # ticket that start with the word departure. What do you get if you multiply
    # those six values together?
    all_fields = set.union(*possible_fields.values())
    fields = [deepcopy(all_fields) for _ in range(len(my_ticket))]
    valid_tickets = (t for t in tickets if all(v in possible_fields for v in t))
    for ticket in valid_tickets:
        for v, f in zip(ticket, fields):
            f &= possible_fields[v]

    # For every set that has only one possibility, we can put it into a list for
    # the proper index, then eliminate from the remaining possibilities for the
    # others, until all fields have their proper place.
    field_order = [None] * len(my_ticket)
    while any(len(f) > 0 for f in fields):
        to_eliminate = set()
        for idx, f in enumerate(fields):
            if len(f) == 1:
                field_name = f.pop()
                to_eliminate.add(field_name)
                field_order[idx] = field_name

        for f in fields:
            f -= to_eliminate

    departure_values = (v for f, v in zip(field_order, my_ticket) if f.startswith("departure"))
    second_answer = reduce(operator.mul, departure_values)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
