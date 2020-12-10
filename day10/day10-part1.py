from math import prod
from operator import sub
from collections import Counter


def differences():
    adapters = [0] + sorted(map(int, open('input/example.txt').read().splitlines()))
    return Counter(map(sub, adapters[1:] + [adapters[-1] + 3], adapters[:]))


print(prod(differences().values()))

