def to_seat_id(line):
    return int(''.join({'F': '0', 'B': '1', 'L': '0', 'R': '1'}.get(c) for c in line), 2)


def seat_ids():
    return [*map(to_seat_id, open('input/actual.txt').read().splitlines())]


def find_missing(l):
    return set(range(min(l), max(l))) - set(l)


print(next(iter(find_missing(seat_ids()))))
