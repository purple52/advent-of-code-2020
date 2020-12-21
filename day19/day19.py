from collections import namedtuple
from itertools import groupby
from re import match

Rule = namedtuple('Rule', ['sub_rules_list'])
Match = namedtuple('Match', ['value'])


def parse_rule(line):
    m = match('(^\\d+): (.*)', line)
    r = match('"(\\w+)"', m.group(2))
    if r:
        return int(m.group(1)), Match(r.group(1))
    else:
        sub_rule_list = [*map(lambda sub_rule: [*map(int, sub_rule.split(' '))], m.group(2).split(' | '))]
        return int(m.group(1)), Rule(sub_rule_list)


def extract_rules(lines):
    return dict(map(parse_rule, lines))


def extract():
    lines = open('input/actual2.txt').read().splitlines()
    grouped_lines = [list(y) for x, y in groupby(lines, lambda line: len(line) == 0) if not x]
    rules = extract_rules(grouped_lines[0])
    values = grouped_lines[1]
    return rules, values


def match_rules(s, rule_list, rules):
    if not s or not rule_list:
        return not s and not rule_list
    else:
        if isinstance(rules[rule_list[0]], Match):
            return s[0] == rules[rule_list[0]].value and match_rules(s[1:], rule_list[1:], rules)
        else:
            for sub_rules in rules[rule_list[0]].sub_rules_list:
                if match_rules(s, sub_rules + rule_list[1:], rules):
                    return True
    return False


def main():
    rules, values = extract()
    valid = [*map(lambda v: match_rules(v, [0], rules), values)].count(True)
    print(f"Valid strings: {valid}")


if __name__ == "__main__": main()
