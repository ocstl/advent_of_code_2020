#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


RULE = re.compile(r"^(\d+): (.*)")


def define_rules(rules):
    rules_dict = dict()
    for rule in rules.splitlines():
        m = RULE.match(rule)
        rule_number = int(m.group(1))
        try:
            rules_dict[rule_number] = [[int(x.strip()) for x in y.split(" ")] for y in m.group(2).split(" | ")]
        # The previous will fail for the basic blocks ("a" and "b").
        except ValueError:
            rules_dict[rule_number] = m.group(2).strip("\"")

    return rules_dict


def build_rule(ruleset, rule_number):
    def sub_rule(nbr):
        rule = ruleset[nbr]
        if not isinstance(rule, list):
            return rule

        return "(" + "|".join("".join(sub_rule(r) for r in alternative) for alternative in rule) + ")"

    return sub_rule(rule_number)


def main(_args):
    rules, messages = open("input.txt", "r").read().split("\n\n", 1)
    ruleset = define_rules(rules)

    # How many messages completely match rule 0?
    rule_0 = re.compile("^" + build_rule(ruleset, 0) + "$")
    first_answer = sum(rule_0.match(message) is not None for message in messages.splitlines())
    print("The first answer is: " + str(first_answer))

    # After updating rules 8 and 11, how many messages completely match rule 0?
    #
    # The update is:
    #   8: 42 | 42 8
    #   11: 42 31 | 42 11 31
    #
    # So the rules are now recursive. There is no recursivity in Python's "re"
    # module, so we'll have to make do.
    #
    # Since "0: 8 11", this essentially means that we need to match 42 more
    # often than 31 (once for rule 8, afterwards (42 (42 31) 42) and so on),
    # and that we need to match 31 at least once.
    rule_42 = build_rule(ruleset, 42)
    rule_31 = build_rule(ruleset, 31)

    all_rules = []
    # This is overkill.
    for c in range(1, max(len(message) for message in messages.splitlines())):
        quantifier = "{" + str(c) + "}"
        new_rule = "^" + rule_42 + "+" + rule_42 + quantifier + rule_31 + quantifier + "$"
        all_rules.append(re.compile(new_rule))

    second_answer = sum(any(r.match(message) is not None for r in all_rules) for message in messages.splitlines())
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
