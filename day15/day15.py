def start_game(initial, turns):
    mem = {number: i + 1 for i, number in enumerate(initial)}
    last = initial[-1]
    for turn in range(len(initial), turns):
        previous = last
        last = turn - mem.get(previous) if mem.get(previous) else 0
        mem[previous] = turn
    print(last)


def main():
    start_game([7, 14, 0, 17, 11, 1, 2], 2020)
    start_game([7, 14, 0, 17, 11, 1, 2], 30000000)


if __name__ == "__main__": main()
