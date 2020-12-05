#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
TOKEN_RULES = [
    ("byr", r"(?<=byr:)\d{4}\b"),
    ("iyr", r"(?<=iyr:)\d{4}\b"),
    ("eyr", r"(?<=eyr:)\d{4}\b"),
    ("hgt", r"(?<=hgt:)(\d{2}in|\d{3}cm)\b"),
    ("hcl", r"(?<=hcl:\#)[0-9a-f]{6}\b"),
    ("ecl", r"(?<=ecl:)(amb|blu|brn|gry|grn|hzl|oth)\b"),
    ("pid", r"(?<=pid:)\d{9}\b")
]
TOKENS_REGEX = re.compile("|".join("(?P<{}>{})".format(*token) for token in TOKEN_RULES))


def valid_passport_part1(passport):
    # The 'cid' field is optional.
    return all(field == 'cid' or field in passport for field in FIELDS)


def valid_passport_part2(passport):
    tokens = TOKENS_REGEX.finditer(passport)

    # The 'cid' field is optional. Remove fields as we find them (with a correct value), then check if all fields have
    # been covered (fields should be empty).
    fields = set(field for field in FIELDS if field != "cid")

    for token in tokens:
        field = token.lastgroup
        # I really wish Python had a `match` statement.
        if field == "byr" and 1920 <= int(token.group()) <= 2002:
            fields.remove(field)
        elif field == "iyr" and 2010 <= int(token.group()) <= 2020:
            fields.remove(field)
        elif field == "eyr" and 2020 <= int(token.group()) <= 2030:
            fields.remove(field)
        elif field == "hgt":
            value = token.group()
            if value[-2:] == "cm" and 150 <= int(value[0:-2]) <= 193:
                fields.remove(field)
            elif value[-2:] == "in" and 59 <= int(value[0:-2]) <= 76:
                fields.remove(field)
            else:
                break
        # For the remaining fields, we already filter the values with the regex.
        elif field == "hcl":
            fields.remove(field)
        elif field == "ecl":
            fields.remove(field)
        elif field == "pid":
            fields.remove(field)
        else:
            break

    return not fields


def main(_args):
    # Passports are separated by a blank line, which is just two consecutive
    # newlines.
    passports = open("input.txt", "r").read().split("\n\n")

    # Count the number of valid passports - those that have all required fields.
    # Treat cid as optional. In your batch file, how many passports are valid?
    first_answer = sum(valid_passport_part1(passport) for passport in passports)
    print("The first answer is: " + str(first_answer))

    # Count the number of valid passports - those that have all required fields
    # and valid values. Continue to treat cid as optional. In your batch file,
    # how many passports are valid?
    second_answer = sum(valid_passport_part2(passport) for passport in passports)
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
