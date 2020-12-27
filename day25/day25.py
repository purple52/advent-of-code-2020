def keys():
    lines = open('input/actual.txt').read().splitlines()
    card_pub_key = int(lines[0])
    door_pub_key = int(lines[1])
    return card_pub_key, door_pub_key


def transform(loop_size, subject_number=7):
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


def find_loop_size(public_key, subject_number=7):
    i = 1
    value = 1
    while True:
        value *= subject_number
        value = value % 20201227
        if value == public_key:
            return i
        i += 1


def main():
    public_keys = keys()
    print(keys())
    card_loop_size = find_loop_size(public_keys[0])
    door_loop_size = find_loop_size(public_keys[1])
    print(transform(card_loop_size, public_keys[1]))
    print(transform(door_loop_size, public_keys[0]))
    exit()


if __name__ == "__main__": main()
