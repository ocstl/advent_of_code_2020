#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

READ_INST = re.compile(r"^(\w*)")
READ_MASK = re.compile(r"^mask = (\w*)")
READ_MEM = re.compile(r"^mem\[(?P<address>\d*)\] = (?P<value>\d*)")


class DockingProgramMemory:
    def __init__(self):
        # 36 bits for each number and 2**36 possible memory locations demands
        # way too much space.
        self.memory = dict()
        # We can use two bitmasks, one to set the required bits to 1 with an OR
        # and one to set the required bits to 0 with an AND.
        self.bitmask_set = 0
        self.bitmask_clear = 2**36 - 1

    def initialize(self, program):
        for line in program:
            inst = READ_INST.match(line).group()
            if inst == 'mask':
                self.set_bitmask(line)
            elif inst == 'mem':
                self.set_memory(line)
            else:
                raise ValueError

    def set_bitmask(self, line):
        bitmask = READ_MASK.findall(line)[0]
        # We'll use an OR, so set everything but the 1s to 0 (0s are already 0).
        self.bitmask_set = int(bitmask.replace('X', '0'), 2)
        # We'll use an AND, so set everything but the 0s to 1 (1s are already 1).
        self.bitmask_clear = int(bitmask.replace('X', '1'), 2)

    def set_memory(self, line):
        address, value = READ_MEM.findall(line)[0]
        self.memory[address] = (int(value) | self.bitmask_set) & self.bitmask_clear


class DecoderChipVersion2:
    def __init__(self):
        # 36 bits for each number and 2**36 possible memory locations demands
        # way too much space.
        self.memory = dict()
        # Any 1 in the bitmask should overwrite the address, so we can use an OR.
        self.bitmask_set = 0
        # For the X's, we can build a number of bitmasks to XOR against.
        self.bitmask_xor = [0]

    def initialize(self, program):
        for line in program:
            inst = READ_INST.match(line).group()
            if inst == 'mask':
                self.set_bitmask(line)
            elif inst == 'mem':
                self.set_memory(line)
            else:
                raise ValueError

    def set_bitmask(self, line):
        bitmask = READ_MASK.findall(line)[0]
        self.bitmask_set = int(bitmask.replace('X', '0'), 2)
        self.bitmask_xor = [0]
        # Essentially, starting with 0, we create new bitmasks for every X we
        # encounter.
        # For example, if the first X is at the 0th digit, this will yield:
        # [0] + [0 ^ 1] = [0, 1].
        # If the 1th digit is then also an X, we'll get:
        # [0, 1] + [0 ^ 2, 1 ^ 3] = [0, 1, 2, 3].
        # And so on.
        for idx, d in enumerate(reversed(bitmask)):
            if d == 'X':
                self.bitmask_xor += [2**idx ^ b for b in self.bitmask_xor]

    def set_memory(self, line):
        address, value = READ_MEM.findall(line)[0]
        masked_address = int(address) | self.bitmask_set
        # Apply every bitmask for the X's.
        for bitmask in self.bitmask_xor:
            self.memory[masked_address ^ bitmask] = int(value)


def main(_args):
    # Execute the initialization program. What is the sum of all values left in
    # memory after it completes?
    part1 = DockingProgramMemory()
    part1.initialize(open("input.txt", "r").readlines())
    first_answer = sum(part1.memory.values())
    print("The first answer is: " + str(first_answer))

    # Execute the initialization program using an emulator for a version 2
    # decoder chip. What is the sum of all values left in memory after it
    # completes?
    part2 = DecoderChipVersion2()
    part2.initialize(open("input.txt", "r").readlines())
    second_answer = sum(part2.memory.values())
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
