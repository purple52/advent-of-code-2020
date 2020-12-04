from re import match
from itertools import groupby


def line_to_dict(line):
    return dict(s.split(':') for s in line.split(' '))


def extract_passports(lines):
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    return [*map(lambda group: line_to_dict(' '.join(group)), grouped_lines)]


def is_valid_height(height):
    m = match('^(\\d+)(cm|in)$', height)
    return bool(m) and {
        'cm' : 150 <= int(m.group(1)) <= 193,
        'in' : 59 <= int(m.group(1)) <= 76
    }.get(m.group(2), False)


rules = {
    'byr': lambda v: v is not None and len(v) == 4 and 1920 <= int(v) <= 2002,
    'iyr': lambda v: v is not None and len(v) == 4 and 2010 <= int(v) <= 2020,
    'eyr': lambda v: v is not None and len(v) == 4 and 2020 <= int(v) <= 2030,
    'hgt': lambda v: v is not None and is_valid_height(v),
    'hcl': lambda v: v is not None and bool(match('^#([0-9a-f]){6}$', v)),
    'ecl': lambda v: v is not None and bool(match('^(amb|blu|brn|gry|grn|hzl|oth)$', v)),
    'pid': lambda v: v is not None and bool(match('^\\d{9}$', v)),
    'cid': lambda v: True
}


def is_valid(passport):
    return [*map(lambda f: rules.get(f)(passport.get(f)), rules.keys())].count(False) == 0


def valid_passports():
    passports = extract_passports(open('input/actual.txt').read().splitlines())
    return [*map(is_valid, passports)].count(True)


print(valid_passports())
