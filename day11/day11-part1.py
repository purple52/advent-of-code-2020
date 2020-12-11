def neighbours(seats, x, y):
    def occupants(d):
        return seats[y + d[0]][x + d[1]] == '#' if (0 <= y + d[0] < len(seats)) and (0 <= x + d[1] < len(seats[y + d[0]])) else 0

    return sum(map(occupants, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]))


def apply_rules(seats):
    new_seats = [[None] * len(seats[0]) for _ in range(len(seats))]
    for y in range(0, len(seats)):
        for x in range(0, len(seats[y])):
            new_seats[y][x] = {
                '.': lambda: '.',
                'L': lambda: '#' if neighbours(seats, x, y) == 0 else 'L',
                '#': lambda: 'L' if neighbours(seats, x, y) >= 4 else '#'
            }.get(seats[y][x])()
    return sum(r.count('#') for r in seats) if new_seats == seats else apply_rules(new_seats)


print(apply_rules([*map(list, open('input/actual.txt').read().splitlines())]))
