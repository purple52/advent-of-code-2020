from collections import namedtuple
from copy import deepcopy

Offset = namedtuple('Offset', ['x', 'y', 'z', 'w'])


class State:
    def __init__(self, data, offset):
        self.data = deepcopy(data)
        self.offset = offset

    def print(self):
        for w in range(self.min_w(), self.max_w() + 1):
            for z in range(self.min_z(), self.max_z() + 1):
                print()
                print(f"z={z}, w={w}")
                for y in range(self.width_y()):
                    print(''.join(self.data[w - self.offset.w][z - self.offset.z][y]))
        print()

    def min_x(self):
        return self.offset.x

    def max_x(self):
        return len(self.data[0][0][0]) + self.offset.x - 1

    def width_x(self):
        return self.max_x() - self.min_x() + 1

    def min_y(self):
        return self.offset.y

    def max_y(self):
        return len(self.data[0][0]) + self.offset.y - 1

    def width_y(self):
        return self.max_y() - self.min_y() + 1

    def min_z(self):
        return self.offset.z

    def max_z(self):
        return len(self.data[0]) + self.offset.z - 1

    def width_z(self):
        return self.max_z() - self.min_z() + 1

    def min_w(self):
        return self.offset.w

    def max_w(self):
        return len(self.data) + self.offset.w - 1

    def width_w(self):
        return self.max_w() - self.min_w() + 1

    def get_point(self, x, y, z, w):
        if (self.min_w() <= w <= self.max_w()) and (self.min_z() <= z <= self.max_z()) and (
                self.min_y() <= y <= self.max_y()) and (self.min_x() <= x <= self.max_x()):
            return self.data[w - self.offset.w][z - self.offset.z][y - self.offset.y][x - self.offset.x]
        else:
            return '.'

    def set_point(self, x, y, z, w, value):
        if self.min_w() <= w <= self.max_w():
            if self.min_z() <= z <= self.max_z():
                if self.min_y() <= y <= self.max_y():
                    if self.min_x() <= x <= self.max_x():
                        self.data[w - self.offset.w][z - self.offset.z][y - self.offset.y][x - self.offset.x] = value
                    else:
                        for uw in range(self.width_w()):
                            for uz in range(self.width_z()):
                                for uy in range(self.width_y()):
                                    if x < self.min_x():
                                        self.data[uw][uz][uy].insert(0, '.')
                                    else:
                                        self.data[uw][uz][uy].append('.')
                        if x < self.min_x():
                            self.offset = Offset(self.offset.x - 1, self.offset.y, self.offset.z, self.offset.w)
                        self.set_point(x, y, z, w, value)
                else:
                    for uw in range(self.width_w()):
                        for uz in range(self.width_z()):
                            if y < self.min_y():
                                self.data[uw][uz].insert(0, ['.'] * self.width_x())
                            else:
                                self.data[uw][uz].append(['.'] * self.width_x())
                    if y < self.min_y():
                        self.offset = Offset(self.offset.x, self.offset.y - 1, self.offset.z, self.offset.w)
                    self.set_point(x, y, z, w, value)
            else:
                for uw in range(self.width_w()):
                    if z < self.min_z():
                        self.data[uw].insert(0, [['.' for _ in range(self.width_x())] for _ in range(self.width_y())])
                    else:
                        self.data[uw].append([['.' for _ in range(self.width_x())] for _ in range(self.width_y())])
                if z < self.min_z():
                    self.offset = Offset(self.offset.x, self.offset.y, self.offset.z - 1, self.offset.w)
                self.set_point(x, y, z, w, value)
        else:
            if w < self.min_w():
                self.data.insert(0, [[['.' for _ in range(self.width_x())] for _ in range(self.width_y())] for _ in
                                     range(self.width_z())])
                self.offset = Offset(self.offset.x, self.offset.y, self.offset.z, self.offset.w - 1)
            else:
                self.data.append([[['.' for _ in range(self.width_x())] for _ in range(self.width_y())] for _ in
                                  range(self.width_z())])
            self.set_point(x, y, z, w, value)

    def iterate(self):
        new_state = self.deepcopy()
        for w in range(self.min_w() - 1, self.max_w() + 2):
            for z in range(self.min_z() - 1, self.max_z() + 2):
                for y in range(self.min_y() - 1, self.max_y() + 2):
                    for x in range(self.min_x() - 1, self.max_x() + 2):
                        neighbours = self.neighbours(x, y, z, w)
                        if self.get_point(x, y, z, w) == '#':
                            if neighbours < 2 or neighbours > 3:
                                new_state.set_point(x, y, z, w, '.')
                        else:
                            if neighbours == 3:
                                new_state.set_point(x, y, z, w, '#')
        return new_state

    def neighbours(self, x, y, z, w):
        count = 0
        for dw in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if not (dw == 0 and dz == 0 and dy == 0 and dx == 0) and self.get_point(x + dx, y + dy, z + dz,
                                                                                                w + dw) == '#':
                            count += 1
        return count

    def count_active(self):
        count = 0
        for w in range(self.min_w(), self.max_w() + 1):
            for z in range(self.min_z(), self.max_z() + 1):
                for y in range(self.min_y(), self.max_y() + 1):
                    for x in range(self.min_x(), self.max_x() + 1):
                        if self.get_point(x, y, z, w) == '#':
                            count += 1
        return count

    def deepcopy(self):
        return State(self.data, self.offset)


def run(initial_state):
    state = initial_state
    for i in range(1, 7):
        state = state.iterate()
    print(f"Active: {state.count_active()}")


def parse_input():
    lines = open('input/actual.txt').read().splitlines()
    z0 = [*map(list, lines)]
    return State([[z0]], Offset(0, 0, 0, 0))


def main():
    initial_state = parse_input()
    run(initial_state)


if __name__ == "__main__": main()
