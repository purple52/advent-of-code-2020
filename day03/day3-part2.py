from operator import mul
from functools import reduce


def tree_count(lines, dx, dy):
    return [*map(lambda y: has_tree(lines[y], dx, dy, y), range(0, len(lines), dy))].count(True)


def has_tree(line, dx, dy, y):
    return line[(int(y / dy) * dx) % len(line)] == '#'


def multiply_tree_counts(slopes):
    lines = open('input/actual.txt').read().splitlines()
    return reduce(mul, map(lambda slope: tree_count(lines, slope[0], slope[1]), slopes))


print(multiply_tree_counts([[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]))
