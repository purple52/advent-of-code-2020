def execute(p, i=0, v=frozenset(), a=0):
    return a if i in v else {
        'acc': lambda: execute(p, i + 1, v.union({i}), a + p[i][1]),
        'jmp': lambda: execute(p, i + p[i][1], v.union({i}), a),
        'nop': lambda: execute(p, i + 1, v.union({i}), a)
    }.get(p[i][0])()


print(execute([*map(lambda l: (l.split()[0], int(l.split()[1])), open('input/actual.txt').read().splitlines())]))
