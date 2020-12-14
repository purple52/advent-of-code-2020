
def notes():
    earliest_departure, buses = open('input/actual.txt').read().splitlines()[:2]
    return int(earliest_departure), [*map(int, filter(lambda b: b != 'x', buses.split(',')))]


def waiting_times(notes):
    return map(lambda bus_id: (bus_id, bus_id - (notes[0] % bus_id)), notes[1])


def earliest_bus(notes):
    return min(waiting_times(notes), key=lambda b: b[1])


def answer(b):
    return b[0] * b[1]


def main():
    print(answer(earliest_bus(notes())))


if __name__ == "__main__": main()
