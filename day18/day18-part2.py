from collections import deque


def calculate(expression):
    rpn = parse(expression)
    return evaluate(rpn)


def parse(expression):
    output = deque()
    operators = deque()
    for c in expression:
        if c.isdigit():
            output.append(int(c))
        elif c == '+' or c == '*':
            while operators and (c == '*' and operators[-1] == '+') and operators[-1] != '(':
                output.append(operators.pop())
            operators.append(c)
        elif c == '(':
            operators.append(c)
        elif c == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators and operators[-1] == '(':
                operators.pop()
    while len(operators) != 0:
        output.append(operators.pop())
    return output


def evaluate(rpn):
    stack = deque()
    for t in rpn:
        if isinstance(t, int):
            stack.append(t)
        elif t == '+':
            stack.append(stack.pop() + stack.pop())
        elif t == '*':
            stack.append(stack.pop() * stack.pop())
    return stack.pop()


def main():
    s = sum(map(calculate, open('input/actual.txt').read().splitlines()))
    print(f"Sum: {s}")


if __name__ == "__main__": main()
