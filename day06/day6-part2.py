from itertools import groupby
from operator import __not__
from string import ascii_lowercase


def extract_answer_counts():
    groups = [list(y) for x, y in groupby(open('input/actual.txt').read().splitlines(), __not__) if not x]
    return map(lambda g: len(set(ascii_lowercase).intersection(*g)), groups)


print(sum(extract_answer_counts()))


