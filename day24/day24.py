from functools import reduce


class Vector:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __add__(self, other):
        return Vector(other.dx + self.dx, other.dy + self.dy)

    def __str__(self):
        return f"({self.dx},{self.dy})"

    def __key(self):
        return (self.dx, self.dy)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.__key() == other.__key()
        return NotImplemented


class Instructions:
    def __init__(self, line):
        self.line = line

    def __iter__(self):
        pos = 0
        while pos < len(self.line):
            if self.line[pos] in Directions:
                yield Directions[self.line[pos]]
                pos += 1
            else:
                yield Directions[self.line[pos:pos + 2]]
                pos += 2


Directions = {
    'e': Vector(2, 0),
    'w': Vector(-2, 0),
    'se': Vector(1, 1),
    'sw': Vector(-1, 1),
    'nw': Vector(-1, -1),
    'ne': Vector(1, -1)
}


class Floor:
    def __init__(self, instructions):
        self.black_tiles = set()
        for line in instructions:
            tile = reduce(Vector.__add__, Instructions(line))
            if tile in self.black_tiles:
                self.black_tiles.discard(tile)
            else:
                self.black_tiles.add(tile)

    def daily_flip(self):
        black_tiles_to_flip = set()
        white_tiles_checked = set()
        white_tiles_to_flip = set()
        for tile in self.black_tiles:
            c_i = 0
            for i in Directions:
                a_i = tile + Directions[i]
                if a_i in self.black_tiles:
                    c_i += 1
                else:
                    if a_i not in white_tiles_checked:
                        c_j = 0
                        for j in Directions:
                            a_j = a_i + Directions[j]
                            if a_j in self.black_tiles:
                                c_j += 1
                        if c_j == 2:
                            white_tiles_to_flip.add(a_i)
            if c_i == 0 or c_i > 2:
                black_tiles_to_flip.add(tile)
        for tile in black_tiles_to_flip:
            self.black_tiles.discard(tile)
        for tile in white_tiles_to_flip:
            self.black_tiles.add(tile)


def main():
    lines = open('input/actual.txt').read().splitlines()
    floor = Floor(lines)
    print(f"Initial count: {len(floor.black_tiles)}")
    for _ in range(100):
        floor.daily_flip()
    print(f"Final count: {len(floor.black_tiles)}")
    exit()


if __name__ == "__main__": main()
