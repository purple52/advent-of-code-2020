from re import match


def is_valid(line):
    (minimum, maximum, letter, password) = match('(\\d+)-(\\d+) (\\w): (.+)', line).groups()
    return int(minimum) <= password.count(letter) <= int(maximum)


def valid_passwords():
    entries = open('input/actual.txt').read().splitlines()
    return list(map(is_valid, entries)).count(True)


print(str(valid_passwords()))
