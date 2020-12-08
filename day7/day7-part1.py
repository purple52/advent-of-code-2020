from re import match
from re import findall


def parse(line):
    return match('^[a-z]+ [a-z]+', line).group(), findall('\\d+ ([a-z]+ [a-z]+)', line)


def contains(item, rules):
    def find(r): return item in rules[r] or any(map(find, rules[r]))

    return map(find, rules)


print(sum(contains('shiny gold', dict(map(parse, open('input/actual.txt').read().splitlines())))))
