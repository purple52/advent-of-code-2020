from collections import namedtuple
from math import prod

Bus = namedtuple('Bus', ['offset', 'id'])
Congruence = namedtuple('Congruence', ['modulus', 'remainder'])


def buses():
    lines = open('input/actual.txt').read().splitlines()[1].split(',')
    return [*map(lambda line: Bus(line[0], int(line[1])), filter(lambda line: line[1] != 'x', enumerate(lines)))]


def cmt(congruences):
    prod_all_moduli = prod(map(lambda c: c.modulus, congruences))

    def addend(congruence):
        other_moduli_prod = prod_all_moduli // congruence.modulus
        inverse_mod = pow(other_moduli_prod, -1, congruence.modulus)
        return congruence.remainder * inverse_mod * other_moduli_prod

    return sum(map(addend, congruences)) % prod_all_moduli


def t(buses):
    return cmt([*map(lambda bus: Congruence(bus.id, bus.id - bus.offset), buses)])


def main():
    print(t(buses()))


if __name__ == "__main__": main()
