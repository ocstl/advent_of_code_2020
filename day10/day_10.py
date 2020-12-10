#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from functools import lru_cache

OUTLET_JOLTAGE = 0


def main(_args):
    adapters = sorted(int(joltage) for joltage in open("input.txt", "r").readlines())
    built_in_joltage = max(adapters) + 3

    # Find a chain that uses all of your adapters to connect the charging outlet
    # to your device's built-in adapter and count the joltage differences
    # between the charging outlet, the adapters, and your device. What is the
    # number of 1-jolt differences multiplied by the number of 3-jolt
    # differences?
    counter = Counter(input_joltage - output_joltage
                      for output_joltage, input_joltage
                      in zip([OUTLET_JOLTAGE, *adapters], [*adapters, built_in_joltage]))

    first_answer = counter[1] * counter[3]
    print("The first answer is: " + str(first_answer))

    # What is the total number of distinct ways you can arrange the adapters to
    # connect the charging outlet to your device?
    @lru_cache(built_in_joltage)
    def ways(joltage):
        if joltage + 3 == built_in_joltage:
            return 1
        elif joltage + 3 > built_in_joltage:
            return 0
        else:
            # We can reach between 1 and 3 (inclusive) joltages higher.
            return sum(ways(joltage + diff) for diff in range(1, 4) if joltage + diff in adapters)

    # Alternatively, we could use a dict or a defaultdict to build from the
    # largest adapters back to the smallest, then sum up the "reachable"
    # adapters.
    second_answer = ways(OUTLET_JOLTAGE)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
