import abc
from re import findall
from collections import deque
from itertools import accumulate
from abc import ABC


class Instruction(ABC):

    @abc.abstractmethod
    def apply_to(self, state):
        return

    @staticmethod
    def from_line(line):
        return {
            'mask': lambda: SetMask(line.split(' = ')[1]),
            'mem': lambda: Assign(int(findall('\\d+', line)[0]), int(findall('\\d+', line)[1]))
        }.get(findall('\\w+', line)[0])()


class SetMask(Instruction):
    def __init__(self, value):
        self.fixed_mask = int(value.replace('X', '0'), 2)
        self.floating_bits = [i for i, x in enumerate(value) if x == "X"]
        self.floating_bits_len = len(self.floating_bits)

    def apply_to(self, state):
        state.fixed_mask = self
        return state


def is_set(x, n):
    return x & 1 << n != 0

def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.

class Assign(Instruction):
    def __init__(self, address, value):
        self.address = list(format(address, '#038b'))[2::]
        self.value = value

    def apply_to(self, state):
        mask = state.fixed_mask
        perms = pow(2, mask.floating_bits_len)
        for i in range(perms):
            address = self.address.copy()
            bits = list(format(i, f"#0{mask.floating_bits_len + 2}b"))[2::]
            for j in range(mask.floating_bits_len):
                address[mask.floating_bits[j]] = str(bits[j])
            a = int("".join(str(i) for i in address), 2) | mask.fixed_mask
            state.mem[a] = self.value
        return state


class State:
    def __init__(self, mem, mask):
        self.mem = mem
        self.mask = mask

    def apply(self, instruction):
        return instruction.apply_to(self)

    def sum_of_mem(self):
        return sum(self.mem.values())


def program():
    return map(Instruction.from_line, open('input/actual.txt').read().splitlines())


def execute(program):
    def last(iterator):
        return deque(iterator, maxlen=1).pop()

    return last(accumulate(program, State.apply, initial=State({}, None)))


def main():
    print(execute(program()).sum_of_mem())


if __name__ == "__main__": main()
