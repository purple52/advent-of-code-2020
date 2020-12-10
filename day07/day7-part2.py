from re import match
from re import findall


def parse(line):
    return match('^[a-z]+ [a-z]+', line).group(), dict((n, int(i)) for i, n in findall('(\\d+) ([a-z]+ [a-z]+)', line))


def bags_in(name, rules):
    return sum(map(lambda k: (rules[name][k] * (bags_in(k, rules) + 1)), rules[name]))


print(bags_in('shiny gold', dict(map(parse, open('input/actual.txt').read().splitlines()))))
