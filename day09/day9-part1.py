from itertools import combinations


def valid(v, t):
    return not next((x for x in combinations(v, 2) if x[0] + x[1] == t), False)


def first_invalid(p, data):
    return data[next((x for x in range(p, len(data)) if valid(data[x - p:x], data[x])))]


print(first_invalid(25, [*map(int, open('input/actual.txt').read().splitlines())]))
