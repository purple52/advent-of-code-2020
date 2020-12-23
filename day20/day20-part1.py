from itertools import groupby
from math import sqrt
from re import match

import numpy


class Orientation:
    def __init__(self, flipped, rotation):
        self.flipped = flipped
        self.rotation = rotation


Unmatched = -1
Orientations = [Orientation(False, 0), Orientation(False, 1), Orientation(False, 2), Orientation(False, 3),
                Orientation(True, 0), Orientation(True, 1), Orientation(True, 2), Orientation(True, 3)]


class Box:
    def __init__(self, tiles):
        self.tiles = set(tiles)
        self.size = int(sqrt(len(self.tiles)))
        self.tile_size = tiles[0].size()

    def contents(self):
        return self.tiles

    def is_unmatched(self, edge):
        matches = set()
        for t in self.tiles:
            for f in t.faces():
                if (edge == f) or (edge == f[::-1]):
                    matches.add(t.tile_id)
        return len(matches) <= 1

    def take_matching_piece(self, required_edges):
        for tile in self.tiles:
            for o in Orientations:
                matching_edges = 0
                for i, edge in enumerate(tile.faces(o)):
                    if required_edges[i] == Unmatched:
                        if self.is_unmatched(edge):
                            matching_edges += 1
                    elif required_edges[i] is not None:
                        if required_edges[i] == edge:
                            matching_edges += 1
                    else:
                        matching_edges += 1
                if matching_edges == 4:
                    self.tiles.remove(tile)
                    return PlacedTile(tile, o)


class Tile:
    def __init__(self, tile_id, data):
        self.tile_id = tile_id
        self.raw_data = numpy.array(data)

    def size(self):
        return len(self.raw_data)

    def faces(self, orientation=Orientation(False, 0)):
        a = self.raw_data.copy()
        if orientation.flipped:
            a = numpy.fliplr(a)
        a = numpy.rot90(a, orientation.rotation)
        top = a[0].tolist()
        bottom = a[-1].tolist()[::-1]
        left = a[:, 0].tolist()[::-1]
        right = a[:, -1].tolist()
        return [top, left, bottom, right]

    def data(self, orientation):
        a = self.raw_data.copy()
        if orientation.flipped:
            a = numpy.fliplr(a)
        a = numpy.rot90(a, orientation.rotation)
        return a

    @staticmethod
    def from_lines(lines):
        tile = Tile(int(match('Tile (\\d+):', lines[0]).group(1)),
                    [*map(lambda line: list(map(lambda c: c == '#', line)), lines[1:])])
        return tile


class Table:
    def __init__(self, box):
        self.box = box
        self.size = box.size
        self.tiles = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.spaces = self.size * self.size

    def place_tile(self, placed_tile, x, y):
        print(
            f"Placing {placed_tile.tile.tile_id} at {x},{y} rotated by {placed_tile.orientation.rotation} flipped={placed_tile.orientation.flipped}")
        self.tiles[y][x] = placed_tile
        self.spaces -= 1

    def is_complete(self):
        return self.spaces == 0

    def tile_at(self, x, y):
        return self.tiles[y][x]

    def get_required_edge_for(self, x, y, direction):
        offsets = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        required_edge = None
        if (direction == 0 and y == 0) or (direction == 1 and x == 0) or (direction == 2 and y == self.size - 1) or (
                direction == 3 and x == self.size - 1):
            required_edge = Unmatched
        else:
            adjacent_tile = self.tile_at(x + offsets[direction][0], y + offsets[direction][1])
            if adjacent_tile is not None:
                left_face = adjacent_tile.tile.faces(adjacent_tile.orientation)[(direction + 2) % 4]
                required_edge = left_face[::-1]
        return required_edge

    def to_picture(self):
        tile_size = self.box.tile_size
        picture = numpy.full([self.size * (tile_size - 2), self.size * (tile_size - 2)], False)
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                px = x * (tile_size - 2)
                py = y * (tile_size - 2)
                picture[py:py + tile_size - 2, px:px + tile_size - 2] = self.tiles[y][x].data()[1:tile_size - 1,
                                                                        1:tile_size - 1]

        return picture

    def __str__(self):
        sa = [[None for _ in range(self.size)] for _ in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                if self.tiles[y][x] is not None:
                    sa[y][x] = self.tiles[y][x].tile.tile_id
        return sa.__str__()


class PlacedTile:
    def __init__(self, tile, orientation):
        self.tile = tile
        self.orientation = orientation

    def data(self):
        return self.tile.data(self.orientation)


def get_box():
    lines = open('input/actual.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    return Box([*map(Tile.from_lines, grouped_lines)])


def find_tile_matching(face, tiles):
    matches = set()
    for t in tiles:
        for f in t.faces():
            if (face == f) or (face == f[::-1]):
                matches.add(t.tile_id)
    return matches


def do_puzzle(box):
    table = Table(box)

    x = 0
    y = 0
    while not table.is_complete():
        print(f"Looking for tile for {x},{y}")
        top_required = table.get_required_edge_for(x, y, 0)
        left_required = table.get_required_edge_for(x, y, 1)
        bottom_required = table.get_required_edge_for(x, y, 2)
        right_required = table.get_required_edge_for(x, y, 3)

        tile = box.take_matching_piece([top_required, left_required, bottom_required, right_required])
        table.place_tile(tile, x, y)

        if x < table.size - 1 and table.tile_at(x + 1, y) is None:
            x += 1
        elif y < table.size - 1 and table.tile_at(x, y + 1) is None:
            y += 1
        elif x > 0 and table.tile_at(x - 1, y) is None:
            x -= 1
        elif y > 0 and table.tile_at(x, y - 1) is None:
            y -= 1

    return table


def remove_sea_monsters(picture):
    masked_picture = picture.copy()
    sea_monster = numpy.array([*map(lambda line: [*map(lambda c: c == '#', line.ljust(20))],
                                    open('input/sea-monster.txt').read().splitlines())])
    not_sea_monster = numpy.logical_not(sea_monster)
    for o in Orientations:
        sea = numpy.rot90(picture, o.rotation)
        if o.flipped:
            sea = numpy.fliplr(sea)
        found = False
        masked_picture = sea.copy()
        for x in range(0, sea.shape[0] - sea_monster.shape[0]):
            for y in range(0, sea.shape[1] - sea_monster.shape[1]):
                masked = numpy.logical_and(sea_monster, sea[x:x + sea_monster.shape[0], y:y + sea_monster.shape[1]])
                if (masked == sea_monster).all():
                    found = True
                    masked_picture[x:x + sea_monster.shape[0], y:y + sea_monster.shape[1]] = numpy.logical_and(
                        not_sea_monster, sea[x:x + sea_monster.shape[0], y:y + sea_monster.shape[1]])
        if found:
            break
    return masked_picture


def main():
    box = get_box()
    table = do_puzzle(box)
    corner_product = table.tile_at(0, 0).tile.tile_id * table.tile_at(table.size - 1, 0).tile.tile_id * table.tile_at(
        table.size - 1, table.size - 1).tile.tile_id * table.tile_at(0, table.size - 1).tile.tile_id
    print(corner_product)

    picture = table.to_picture()
    for y in range(len(picture)):
        print(''.join(list(map(lambda c: '#' if c else '.', picture[y]))))

    monsterless_picture = remove_sea_monsters(picture)

    print(numpy.count_nonzero(monsterless_picture))


if __name__ == "__main__": main()
