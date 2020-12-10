from itertools import combinations


def valid(v, t):
    return not next((x for x in combinations(v, 2) if sum(x) == t), False)


def first_invalid(p, data):
    return data[next((x for x in range(p, len(data)) if valid(data[x - p:x], data[x])))]


def weakness(p, data):
    target = first_invalid(p, data)
    nums = find_cont(target, data)
    return min(nums) + max(nums)


def find_cont(target, numbers):
    x = 0
    y = 1
    s = numbers[x] + numbers[y]
    while s != target:
        if s < target:
            y += 1
            s += numbers[y]
        if s > target:
            s -= numbers[x]
            x += 1
    return numbers[x:y+1]


print(weakness(25, [*map(int, open('input/actual.txt').read().splitlines())]))
