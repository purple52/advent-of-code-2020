from collections import namedtuple
from itertools import groupby
from re import findall

Notes = namedtuple('Notes', ['rules', 'your_ticket', 'nearby_tickets'])
Range = namedtuple('Range', ['min', 'max'])


def parse_rule_line(line):
    rule_name = findall('^[a-z ]+', line)[0]
    ranges = findall('(\\d+)-(\\d+)', line)

    return rule_name, [*map(lambda r: Range(int(r[0]), int(r[1])), ranges)]


def extract_rules(lines):
    return dict(map(parse_rule_line, lines))


def parse_ticket_line(line):
    return [*map(int, line.split(','))]


def extract_nearby_tickets(lines):
    return [*map(parse_ticket_line, lines[1:])]


def extract_notes():
    lines = open('input/actual.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    rules = extract_rules(grouped_lines[0])
    your_ticket = parse_ticket_line(grouped_lines[1][1])
    nearby_tickets = extract_nearby_tickets(grouped_lines[2])
    return Notes(rules, your_ticket, nearby_tickets)


def error(ticket, rules, possible_fields):
    e = 0
    ticket_is_invalid = False
    invalid_rules = []
    for _ in ticket:
        invalid_rules.append(set())
    for i, v in enumerate(ticket):
        field_completely_invalid = True
        for rule in rules:
            rule_is_invalid = True
            for this_range in rules[rule]:
                if this_range.min <= v <= this_range.max:
                    field_completely_invalid = False
                    rule_is_invalid = False
            if rule_is_invalid:
                invalid_rules[i].add(rule)
        if field_completely_invalid:
            e += v
            ticket_is_invalid = True
    if not ticket_is_invalid:
        for i, rule in enumerate(invalid_rules):
            possible_fields[i] = possible_fields[i] - rule
            possible_fields = clean_up(possible_fields)

    return possible_fields, e


def clean_up(possible_fields):
    is_changed = False
    for i in range(len(possible_fields)):
        if (len(possible_fields[i])) == 1:
            for x, field in enumerate(possible_fields):
                if x != i:
                    remaining_rule = next(iter(possible_fields[i]))
                    if remaining_rule in possible_fields[x]:
                        possible_fields[x].discard(remaining_rule)
                        is_changed = True

    return clean_up(possible_fields) if is_changed else possible_fields


def error_rate(notes):
    print(notes)
    possible_fields = []
    for _ in notes.your_ticket:
        possible_fields.append(set(notes.rules.keys()))
    e = 0
    for ticket in notes[2]:
        possible_fields, de = error(ticket, notes[0], possible_fields)
        e += de

    field_order = [*map(lambda f: next(iter(f)), possible_fields)]
    print(field_order)
    return field_order, e


def main():
    notes = extract_notes()
    field_order, e = error_rate(notes)
    m = 1
    for i in range(len(field_order)):
        if field_order[i].startswith('departure'):
            m *= notes.your_ticket[i]
    print(m)


if __name__ == "__main__": main()
