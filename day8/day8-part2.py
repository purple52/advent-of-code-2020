def acc(p, i, v, a, m):
    return execute(p, i + 1, v.union({i}), a + p[i][1], m)


def jmp(p, i, v, a, m):
    return execute(p, i + p[i][1], v.union({i}), a, m)


def nop(p, i, v, a, m):
    return execute(p, i + 1, v.union({i}), a, m)


def execute(p, i=0, v=frozenset(), a=0, m=True):
    return None if i in v else a if i == len(p) else {
        'acc': lambda: acc(p, i, v, a, m),
        'jmp': lambda: jmp(p, i, v, a, m) or (nop(p, i, v, a, False) if m else None),
        'nop': lambda: nop(p, i, v, a, m) or (jmp(p, i, v, a, False) if m else None)
    }.get(p[i][0])()


print(execute([*map(lambda l: (l.split()[0], int(l.split()[1])), open('input/actual.txt').read().splitlines())]))
