from itertools import groupby
from re import findall


def parse_rule_line(line):
    rule_name = findall('^\w+', line)[0]
    ranges = findall('(\d+)-(\d+)', line)

    return rule_name, [*map(lambda r: (int(r[0]), int(r[1])), ranges)]


def extract_rules(lines):
    return [*map(parse_rule_line, lines)]


def parse_ticket_line(line):
    return [*map(int, line.split(','))]


def extract_nearby_tickets(lines):
    return [*map(parse_ticket_line, lines[1:])]


def extract_notes():
    lines = open('input/actual.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    rules = extract_rules(grouped_lines[0])
    nearby_tickets = extract_nearby_tickets(grouped_lines[2])
    return rules, nearby_tickets


def error(ticket, rules):
    e = 0
    print(f"Checking ticket {ticket} against {rules}")
    for v in ticket:
        print(f"Checking value {v}")
        is_invalid = True
        for r in rules:
            print(f"Checking against rule {r}")
            for rnge in r[1]:
                print(f"Checking against range {rnge}")
                if rnge[0] <= v <= rnge[1]:
                    print(f"v is valid")
                    is_invalid = False
        if is_invalid:
            print(f"Adding {v} to error")
            e += v
    print(f"Error is {e}")
    return e


def error_rate(notes):
    return sum(map(lambda ticket: error(ticket, notes[0]), notes[1]))


def main():
    print(error_rate(extract_notes()))


if __name__ == "__main__": main()
