from collections import deque
import numpy as np
from itertools import groupby


def deal():
    lines = open('input/actual.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    decks = [*map(lambda p: deque(map(int, p[:0:-1])), grouped_lines)]
    return decks


def scores(decks):
    return [*map(lambda deck: sum([(pos + 1) * card for pos, card in enumerate(deck)]), decks)]


def play_game(decks):
    old_decks = set()
    while decks[0] and decks[1]:

        if str(decks[0]) + str(decks[1]) in old_decks:
            return 0, decks

        old_decks.add(str(decks[0]) + str(decks[1]))

        cards = (decks[0].pop(), decks[1].pop())

        if len(decks[0]) >= cards[0] and len(decks[1]) >= cards[1]:
            new_decks = [
                deque(list(decks[0])[len(decks[0]) - cards[0]:]),
                deque(list(decks[1])[len(decks[1]) - cards[1]:])
            ]
            round_winner = play_game(new_decks)
        else:
            round_winner = (np.argmax(cards), decks)

        decks[round_winner[0]].appendleft(cards[round_winner[0]])
        decks[round_winner[0]].appendleft(cards[(round_winner[0] + 1) % 2])

    if decks[0]:
        return 0, decks
    else:
        return 1, decks


def main():
    decks = deal()
    result = play_game(decks)
    print(result[0])
    print(scores(result[1]))


if __name__ == "__main__": main()
