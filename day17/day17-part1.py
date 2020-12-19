from collections import namedtuple
from copy import deepcopy

Offset = namedtuple('Offset', ['x', 'y', 'z'])


class State:
    def __init__(self, data, offset):
        self.data = deepcopy(data)
        self.offset = offset

    def print(self):
        for z in range(self.min_z(), self.max_z() + 1):
            print()
            print(f"z={z}")
            for y in range(self.width_y()):
                print(''.join(self.data[z - self.offset.z][y]))
        print()

    def min_x(self):
        return self.offset.x

    def max_x(self):
        return len(self.data[0][0]) + self.offset.x - 1

    def width_x(self):
        return self.max_x() - self.min_x() + 1

    def min_y(self):
        return self.offset.y

    def max_y(self):
        return len(self.data[0]) + self.offset.y - 1

    def width_y(self):
        return self.max_y() - self.min_y() + 1

    def min_z(self):
        return self.offset.z

    def max_z(self):
        return len(self.data) + self.offset.z - 1

    def width_z(self):
        return self.max_z() - self.min_z() + 1

    def get_point(self, x, y, z):
        if (self.min_z() <= z <= self.max_z()) and (self.min_y() <= y <= self.max_y()) and (self.min_x() <= x <= self.max_x()):
            return self.data[z - self.offset.z][y - self.offset.y][x - self.offset.x]
        else:
            return '.'

    def set_point(self, x, y, z, value):
        if self.min_z() <= z <= self.max_z():
            if self.min_y() <= y <= self.max_y():
                if self.min_x() <= x <= self.max_x():
                    self.data[z - self.offset.z][y - self.offset.y][x - self.offset.x] = value
                else:
                    for uz in range(self.width_z()):
                        for uy in range(self.width_y()):
                            if x < self.min_x():
                                self.data[uz][uy].insert(0, '.')
                            else:
                                self.data[uz][uy].append('.')
                    if x < self.min_x():
                        self.offset = Offset(self.offset.x -1, self.offset.y, self.offset.z)
                    self.set_point(x, y, z, value)
            else:
                for uz in range(self.width_z()):
                    if y < self.min_y():
                        self.data[uz].insert(0, ['.' for _ in range(self.width_x())])
                    else:
                        self.data[uz].append(['.' for _ in range(self.width_x())])
                if y < self.min_y():
                    self.offset = Offset(self.offset.x, self.offset.y - 1, self.offset.z)
                self.set_point(x, y, z, value)
        else:
            if z < self.min_z():
                self.data.insert(0, [['.' for _ in range(self.width_x())] for _ in range(self.width_y())])
                self.offset = Offset(self.offset.x, self.offset.y, self.offset.z - 1)
            else:
                self.data.append([['.' for _ in range(self.width_x())] for _ in range(self.width_y())])
            self.set_point(x, y, z, value)

    def iterate(self):
        new_state = self.deepcopy()
        for z in range(self.min_z() - 1, self.max_z() + 2):
            for y in range(self.min_y() - 1, self.max_y() + 2):
                for x in range(self.min_x() - 1, self.max_x() + 2):
                    neighbours = self.neighbours(x, y, z)
                    if self.get_point(x, y, z) == '#':
                        if neighbours < 2 or neighbours > 3:
                            new_state.set_point(x, y, z, '.')
                    else:
                        if neighbours == 3:
                            new_state.set_point(x, y, z, '#')
        return new_state

    def neighbours(self, x, y, z):
        count = 0
        for dz in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dz == 0 and dy == 0 and dx == 0) and self.get_point(x + dx, y + dy, z + dz) == '#':
                        count += 1
        return count

    def count_active(self):
        count = 0
        for z in range(self.min_z(), self.max_z() + 1):
            for y in range(self.min_y(), self.max_y() + 1):
                for x in range(self.min_x(), self.max_x() + 1):
                    if self.get_point(x, y, z) == '#':
                        count += 1
        return count

    def deepcopy(self):
        return State(self.data, self.offset)


def run(initial_state):
    state = initial_state
    for i in range(1,7):
        state = state.iterate()
    print(f"Active: {state.count_active()}")


def parse_input():
    lines = open('input/actual.txt').read().splitlines()
    z0 = [*map(list, lines)]
    return State([z0], Offset(0, 0, 0))


def main():
    initial_state = parse_input()
    run(initial_state)


if __name__ == "__main__": main()
