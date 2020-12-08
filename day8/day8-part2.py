def execute(p, i=0, v=frozenset(), a=0, m=0):
    return None if m > 1 or i in v else a if i == len(p) else {
        'acc': lambda: execute(p, i + 1, v.union({i}), a + p[i][1], m),
        'jmp': lambda: execute(p, i + p[i][1], v.union({i}), a, m) or execute(p, i + 1, v.union({i}), a, m + 1),
        'nop': lambda: execute(p, i + 1, v.union({i}), a, m) or execute(p, i + p[i][1], v.union({i}), a, m + 1)
    }.get(p[i][0])()


print(execute([*map(lambda l: (l.split()[0], int(l.split()[1])), open('input/actual.txt').read().splitlines())]))
