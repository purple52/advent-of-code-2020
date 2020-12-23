import re
from collections import Counter


class Food:
    def __init__(self, ingredients, allergens):
        self._ingredients = ingredients
        self._allergens = allergens

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def allergens(self):
        return self._allergens

    @staticmethod
    def from_line(line):
        m = re.match('([\\w ]+) \\(contains ([\\w, ]+)\\)', line)
        ingredients = set(m.group(1).split(' '))
        allergens = set(m.group(2).split(', '))
        return Food(ingredients, allergens)


def get_foods():
    return set(map(Food.from_line, open('input/actual.txt').read().splitlines()))


def ingredients_with_known_allergen(foods):
    all_allergens = set().union(*map(Food.allergens.fget, foods))
    all_ingredients = set().union(*map(Food.ingredients.fget, foods))
    ingredients = dict()
    while len(ingredients) < len(all_allergens):
        for allergen in all_allergens:
            foods_with_allergen = filter(lambda f: allergen in f.allergens, foods)
            possible_causes = \
                all_ingredients.intersection(*map(Food.ingredients.fget, foods_with_allergen)) - ingredients.keys()
            if len(possible_causes) == 1:
                ingredients[next(iter(possible_causes))] = allergen
    return ingredients


def main():
    foods = get_foods()

    dangerous_ingredients = ingredients_with_known_allergen(foods)

    safe_ingredient_counts = Counter(sum(map(lambda f: list(f.ingredients - dangerous_ingredients.keys()), foods), []))

    part_one_sum = sum(map(lambda c: c[1], safe_ingredient_counts.items()))
    print(f"Ingredient count: {part_one_sum}")

    part_two_list = ','.join(map(lambda i: i[0], sorted(dangerous_ingredients.items(), key=lambda x: x[1])))
    print(f"Dangerous ingredients: {part_two_list}")


if __name__ == "__main__": main()
