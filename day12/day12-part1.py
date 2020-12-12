from collections import deque
from itertools import accumulate
from math import cos, radians, sin


class Instruction:
    def __init__(self, line):
        self.action = line[0]
        self.value = int(line[1:])


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translated_by(self, vector):
        return Point(self.x + vector.x, self.y + vector.y)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scaled_by(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def rotated_by(self, degrees):
        return Vector(int(self.x * cos(radians(degrees))) - int(self.y * sin(radians(degrees))),
                      int(self.x * sin(radians(degrees))) + int(self.y * cos(radians(degrees))))


NORTH = Vector(0, 1)
WEST = Vector(-1, 0)
SOUTH = Vector(0, -1)
EAST = Vector(1, 0)


class State:
    def __init__(self, position, facing):
        self.position = position
        self.facing = facing

    def turn_by(self, degrees):
        return State(self.position, self.facing.rotated_by(degrees))

    def move_by(self, vector):
        return State(self.position.translated_by(vector), self.facing)

    def manhattan_distance(self):
        return abs(self.position.x) + abs(self.position.y)

    def apply(self, instruction):
        return {
            'F': lambda: self.move_by(vector=self.facing.scaled_by(instruction.value)),
            'N': lambda: self.move_by(vector=NORTH.scaled_by(instruction.value)),
            'W': lambda: self.move_by(vector=WEST.scaled_by(instruction.value)),
            'S': lambda: self.move_by(vector=SOUTH.scaled_by(instruction.value)),
            'E': lambda: self.move_by(vector=EAST.scaled_by(instruction.value)),
            'L': lambda: self.turn_by(degrees=instruction.value),
            'R': lambda: self.turn_by(degrees=-instruction.value),
        }.get(instruction.action)()


def follow(instructions):
    def last(iterator):
        return deque(iterator, maxlen=1).pop()

    return last(accumulate(instructions, State.apply, initial=State(Point(0, 0), EAST)))


def instructions():
    return map(Instruction, open('input/actual.txt').read().splitlines())


def main():
    print(follow(instructions()).manhattan_distance())


if __name__ == "__main__": main()
