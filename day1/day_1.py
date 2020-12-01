#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import reduce
from itertools import combinations
from operator import mul


def main(_args):
    # Find the two entries that sum to 2020; what do you get if you multiply them together?
    expense_report = list(map(int, open("input.txt", "r").read().split()))

    # Since the expense report is relatively small, testing all combinations is reasonable.
    # Alternatively, we could use a sorted list and eat away at both side until we find a matching pair.
    first_answer = reduce(mul, next(x for x in combinations(expense_report, 2) if sum(x) == 2020))
    print("The first answer is: " + str(first_answer))

    # In your expense report, what is the product of the three entries that sum to 2020?
    # Again, given the small length of the list, testing all combinations is reasonable.
    # The alternative is a bit more complicated, but we could use two sorted lists, one the regular one and the other
    # containing the pairs.
    second_answer = reduce(mul, next(x for x in combinations(expense_report, 3) if sum(x) == 2020))
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
