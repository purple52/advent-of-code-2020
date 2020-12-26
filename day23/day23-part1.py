class Circle:
    def __init__(self, cups):
        self.size = len(cups)
        self.cups = [0] * self.size
        for i, c in enumerate(cups):
            self.cups[int(c) - 1] = int(cups[(i + 1) % self.size]) - 1
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

    def order(self):
        n = 0
        ordered = []
        for _ in range(self.size):
            ordered.append(n + 1)
            n = self.cups[n]
        return ordered


def main():
    circle = Circle('716892543')
    for i in range(100):
        circle.move()
    print(''.join(map(str, circle.order()[1:])))
    exit()


if __name__ == "__main__": main()
