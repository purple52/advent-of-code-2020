def tree_count(dx):
    lines = open('input/actual.txt').read().splitlines()
    return [*map(lambda y_line: has_tree(dx, y_line[0], y_line[1]), enumerate(lines))].count(True)


def has_tree(dx, y, line):
    return line[(y * dx) % len(line)] == '#'


print(tree_count(3))
