from itertools import groupby
from operator import __not__


def extract_answer_counts():
    groups = [list(y) for x, y in groupby(open('input/actual.txt').read().splitlines(), __not__) if not x]
    return map(lambda g: len(set().union(*g)), groups)


print(sum(extract_answer_counts()))
