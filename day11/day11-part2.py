def neighbours(seats, x, y):
    def occupants(d):
        cx = x + d[0]
        cy = y + d[1]
        while 0 <= cy < len(seats) and 0 <= cx < len(seats[cy]):
            if seats[cy][cx] == '#':
                return 1
            elif seats[cy][cx] == 'L':
                return 0
            else:
                cx += d[0]
                cy += d[1]
        return 0

    return sum(map(occupants, [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]))


def apply_rules(seats):
    new_seats = [[None] * len(seats[0]) for _ in range(len(seats))]
    for y in range(0, len(seats)):
        for x in range(0, len(seats[y])):
            new_seats[y][x] = {
                '.': lambda: '.',
                'L': lambda: '#' if neighbours(seats, x, y) == 0 else 'L',
                '#': lambda: 'L' if neighbours(seats, x, y) >= 5 else '#'
            }.get(seats[y][x])()
    return sum(r.count('#') for r in seats) if new_seats == seats else apply_rules(new_seats)


print(apply_rules([*map(list, open('input/actual.txt').read().splitlines())]))
