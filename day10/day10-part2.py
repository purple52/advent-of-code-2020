from itertools import groupby
from operator import sub
from math import prod


def diffs():
    adapters = [0] + sorted(map(int, open('input/example.txt').read().splitlines()))
    return map(sub, adapters[1:] + [adapters[-1] + 3], adapters[:])


def perms():
    return prod(map(lambda n: int((n - 1) * n / 2) + 1, [len(list(y)) for x, y in groupby(diffs()) if x != 3]))


print(perms())
