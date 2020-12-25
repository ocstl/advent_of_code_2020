#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


RECIPE = re.compile(r"^(?P<ingredients>[\s\w]*) \(contains (?P<allergens>[\s\w,]*)\)$")


class Recipe:
    def __init__(self, line):
        d = RECIPE.match(line).groupdict()
        self.ingredients = [ingredient.strip() for ingredient in d["ingredients"].split(' ')]
        self.allergens = [allergen.strip() for allergen in d["allergens"].split(",")]


def main(_args):
    recipes = [Recipe(line) for line in open("input.txt", "r").readlines()]

    # Find all possible allergens and all possible ingredients.
    allergens = set(allergen for recipe in recipes for allergen in recipe.allergens)
    ingredients = set(ingredient for recipe in recipes for ingredient in recipe.ingredients)

    # Start with all possible ingredients. Given that for any allergen mentioned
    # in a recipe the ingredient HAS to be present, we can winnow out the
    # impossible matches.
    allergen_ingredient = {
        allergen: set(ingredients) for allergen in allergens
    }
    for recipe in recipes:
        for allergen in recipe.allergens:
            allergen_ingredient[allergen] &= set(recipe.ingredients)

    # We still have multiple matches in some cases. Since each ingredient can
    # contain at most one allergen, we can progressively eliminate the multiple
    # matches. For example, if we 2 ingredients that match 'wheat', but we know
    # that one of these two ingredient contains 'fish', only the second one can
    # contain 'wheat'.
    confirmed_links = dict()
    while allergen_ingredient:
        for allergen, ingredients in allergen_ingredient.items():
            if len(ingredients) == 1:
                ingredient = ingredients.pop()
                confirmed_links[ingredient] = allergen
                del allergen_ingredient[allergen]

                # Eliminate this new ingredient from the remaining matches.
                for ingredient_list in allergen_ingredient.values():
                    ingredient_list.discard(ingredient)

                break

    # Determine which ingredients cannot possibly contain any of the allergens
    # in your list. How many times do any of those ingredients appear?
    first_answer = sum(ingredient not in confirmed_links for recipe in recipes
                       for ingredient in recipe.ingredients)
    print("The first answer is: " + str(first_answer))

    # Time to stock your raft with supplies. What is your canonical dangerous
    # ingredient list?
    second_answer = ','.join(sorted(confirmed_links.keys(),
                                    key=lambda ingredient: confirmed_links[ingredient]))
    print("The second answer is: " + second_answer)


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
