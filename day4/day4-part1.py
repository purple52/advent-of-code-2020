from itertools import groupby


def line_to_dict(line):
    return dict(s.split(':') for s in line.split(' '))


def extract_passports(lines):
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    return [*map(lambda group: line_to_dict(" ".join(group)), grouped_lines)]


def is_valid(passport):
    return all(field in passport.keys() for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])


def valid_passports():
    passports = extract_passports(open('input/actual.txt').read().splitlines())
    return [*map(is_valid, passports)].count(True)


print(valid_passports())
