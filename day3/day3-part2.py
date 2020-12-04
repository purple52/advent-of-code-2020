from operator import mul
from functools import reduce


def tree_count(lines, dx, dy):
    return [*map(lambda y_line: has_tree(y_line[1], dx, dy, y_line[0]), enumerate(lines))].count(True)


def has_tree(line, dx, dy, y):
    return y % dy == 0 and line[(int(y / dy) * dx) % len(line)] == '#'


def multiply_tree_counts(slopes):
    lines = open('input/actual.txt').read().splitlines()
    return reduce(mul, map(lambda slope: tree_count(lines, slope[0], slope[1]), slopes))


print(multiply_tree_counts([[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]))
