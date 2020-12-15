from re import findall
from collections import deque
from itertools import accumulate


class Instruction:
    def __init__(self, line):
        parts = line.split(' = ')
        if parts[0] == 'mask':
            self.action = 'mask'
            self.value = int(parts[1].replace('X', '0'), 2), int(parts[1].replace('X', '1'), 2)
        else:
            self.action = 'mem'
            self.value = int(findall('\\d+', parts[0])[0]), int(findall('\\d+', parts[1])[0])


class State:
    def __init__(self, mem, mask):
        self.mem = mem
        self.mask = mask

    def set_mask(self, mask):
        self.mask = mask

    def assign(self, value):
        self.mem[value[0]] = value[1] | self.mask[0] & self.mask[1]

    def apply(self, instruction):
        {
            'mask': lambda: self.set_mask(instruction.value),
            'mem': lambda: self.assign(instruction.value)
        }.get(instruction.action)()
        return self

    def sum_of_mem(self):
        return sum(self.mem.values())


def program():
    return map(Instruction, open('input/actual.txt').read().splitlines())


def execute(program):
    def last(iterator):
        return deque(iterator, maxlen=1).pop()

    return last(accumulate(program, State.apply, initial=State({}, (0, 0))))


def main():
    print(execute(program()).sum_of_mem())


if __name__ == "__main__": main()
