from collections import deque
from itertools import groupby


def deal():
    lines = open('input/actual.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    decks = [*map(lambda p: deque(map(int, p[:0:-1])), grouped_lines)]
    return decks


def scores(decks):
    return [*map(lambda deck: sum([(pos + 1) * card for pos, card in enumerate(deck)]), decks)]


def play_game(decks):
    while decks[0] and decks[1]:
        c0 = decks[0].pop()
        c1 = decks[1].pop()
        if c0 > c1:
            decks[0].appendleft(c0)
            decks[0].appendleft(c1)
        else:
            decks[1].appendleft(c1)
            decks[1].appendleft(c0)
    return scores(decks)


def main():
    decks = deal()
    result = play_game(decks)
    print(result)


if __name__ == "__main__": main()
