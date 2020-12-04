from re import match


def is_valid(line):
    (minimum, maximum, letter, password) = match('(\\d+)-(\\d+) (\\w): (.+)', line).groups()
    return len(password) >= int(maximum) and (
                (password[int(minimum) - 1] == letter) != bool(password[int(maximum) - 1] == letter))


def valid_passwords():
    entries = open('input/actual.txt').read().splitlines()
    return [*map(is_valid, entries)].count(True)


print(str(valid_passwords()))
