from collections import namedtuple
from math import prod

Bus = namedtuple('Bus', ['offset', 'id'])


def buses():
    lines = open('input/actual.txt').read().splitlines()[1].split(',')
    return [*map(lambda line: Bus(line[0], int(line[1])), filter(lambda line: line[1] != 'x', enumerate(lines)))]


def bus_prod(bus, big_n):
    a = bus.id - bus.offset
    return a * pow(int(big_n / bus.id), -1, bus.id) * int(big_n / bus.id)


def t(buses):
    big_n = prod(map(lambda bus: bus.id, buses))
    return sum(map(lambda bus: bus_prod(bus, big_n), buses)) % big_n


def main():
    print(t(buses()))


if __name__ == "__main__": main()
