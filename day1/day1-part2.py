entries = [*map(int, open('input/actual.txt').read().splitlines())]

for x_index, x_value in enumerate(entries):
    for y_index, y_value in enumerate(entries[x_index + 1:len(entries)]):
        for z_index, z_value in enumerate(entries[y_index + 1:len(entries)]):
            if x_value + y_value + z_value == 2020:
                print(x_value * y_value * z_value)
                exit()
