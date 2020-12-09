#!/usr/bin/env python
# -*- coding: utf-8 -*-


def detect_loop(program):
    instruction_pointer = 0
    accumulator = 0
    program_length = len(program)
    visited_instructions = set()

    while (instruction_pointer not in visited_instructions
           and instruction_pointer < program_length):
        visited_instructions.add(instruction_pointer)
        opcode, value = program[instruction_pointer].split()

        if opcode == 'nop':
            instruction_pointer += 1
        elif opcode == 'acc':
            accumulator += int(value)
            instruction_pointer += 1
        elif opcode == 'jmp':
            instruction_pointer += int(value)
        else:
            raise ValueError(opcode)

    return instruction_pointer < program_length, accumulator


def part2(program):
    # Be aware that this function will modify the program to make it work.
    result = 0

    # Switch one instruction at a time until we get a program that reaches the end.
    for idx in range(len(program)):
        if 'nop' in program[idx]:
            program[idx] = program[idx].replace('nop', 'jmp')
            (found_loop, result) = detect_loop(program)
            # If we find a loop, reverse the change and move on. Otherwise, end here.
            if found_loop:
                program[idx] = program[idx].replace('jmp', 'nop')
            else:
                break
        elif 'jmp' in program[idx]:
            program[idx] = program[idx].replace('jmp', 'nop')
            (found_loop, result) = detect_loop(program)
            # If we find a loop, reverse the change and move on. Otherwise, end here.
            if found_loop:
                program[idx] = program[idx].replace('nop', 'jmp')
            else:
                break

    return result


def main(_args):
    program = [line for line in open("input.txt", "r").readlines()]

    # Run your copy of the boot code. Immediately before any instruction is
    # executed a second time, what value is in the accumulator?
    first_answer = detect_loop(program)[1]
    print("The first answer is: " + str(first_answer))

    # Fix the program so that it terminates normally by changing exactly one jmp
    # (to nop) or nop (to jmp). What is the value of the accumulator after the
    # program terminates?
    second_answer = part2(program)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
