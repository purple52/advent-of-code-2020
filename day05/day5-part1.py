def to_seat_id(line):
    return int(''.join({'F': '0', 'B': '1', 'L': '0', 'R': '1'}.get(c) for c in line), 2)


def seat_ids():
    return [*map(to_seat_id, open('input/actual.txt').read().splitlines())]


print(max(seat_ids()))
