#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import re


TOKENS = (
    ("NUMBER",  r"\d+"),
    ("OPERATOR", r"[*+]{1}"),
    ("LEFT_PAREN", r"\("),
    ("RIGHT_PAREN", r"\)"),
)
TOKENIZER = re.compile("|".join("(?P<{}>{})".format(kind, exp) for kind, exp in TOKENS))


def parse(expression, operator_precedence):
    operators = []
    rpn = []

    for token in TOKENIZER.finditer(expression.replace(" ", "")):
        kind = token.lastgroup
        value = token.group()

        if kind == "NUMBER":
            rpn.append(value)
        elif kind == "OPERATOR":
            while (operators
                    and operators[-1] != "("
                    and operator_precedence[value] <= operator_precedence[operators[-1]]):
                rpn.append(operators.pop())

            operators.append(value)
        elif kind == "LEFT_PAREN":
            operators.append(value)
        elif kind == "RIGHT_PAREN":
            while operators[-1] != "(":
                rpn.append(operators.pop())

            operators.pop()

    while operators:
        rpn.append(operators.pop())

    return rpn


def evaluate(expression, operator_precedence=None):
    # Parse the expression into Reverse Polish notation, to make it easier.
    rpn = parse(expression, operator_precedence or defaultdict(int))

    values = []
    for elem in rpn:
        if elem == "+":
            rhs = values.pop()
            values[-1] += rhs
        elif elem == "*":
            rhs = values.pop()
            values[-1] *= rhs
        else:
            values.append(int(elem))

    return values.pop()


def main(_args):
    expressions = [line.strip() for line in open("input.txt", "r").readlines()]

    # Before you can help with the homework, you need to understand it yourself.
    # Evaluate the expression on each line of the homework; what is the sum of
    # the resulting values?
    first_answer = sum(evaluate(line) for line in expressions)
    print("The first answer is: " + str(first_answer))

    # What do you get if you add up the results of evaluating the homework
    # problems using these new rules?
    second_answer = sum(evaluate(line, {"+": 1, "*": 0}) for line in expressions)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
