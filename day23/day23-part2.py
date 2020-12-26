class Circle:
    def __init__(self, cups):
        self.size = 1000000
        self.cups = [0] * self.size
        for i, c in enumerate(cups):
            self.cups[int(c) - 1] = int(cups[(i + 1) % len(cups)]) - 1
        self.cups[int(cups[-1]) - 1] = len(cups)
        for i in range(len(cups), self.size):
            self.cups[i] = i + 1
        self.cups[self.size - 1] = int(cups[0]) - 1
        self.current = int(cups[0]) - 1

    def move(self):
        picked_up = [self.cups[self.current]]
        picked_up.append(self.cups[picked_up[0]])
        picked_up.append(self.cups[picked_up[1]])
        self.cups[self.current] = self.cups[picked_up[2]]

        destination = (self.current - 1) % self.size
        while destination in picked_up:
            destination = (destination - 1) % self.size

        n = self.cups[destination]
        self.cups[destination] = picked_up[0]
        self.cups[picked_up[2]] = n

        self.current = self.cups[self.current]


def main():
    circle = Circle('716892543')
    for i in range(10000000):
        circle.move()
    print((circle.cups[0] + 1) * (circle.cups[circle.cups[0]] + 1))
    exit()


if __name__ == "__main__": main()
