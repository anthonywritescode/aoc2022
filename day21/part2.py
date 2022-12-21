from __future__ import annotations

import argparse
import os.path

import pytest
from z3 import Int
from z3 import Optimize
from z3 import sat

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '/': lambda a, b: a / b,
    '*': lambda a, b: a * b,
}


def compute(s: str) -> int:
    o = Optimize()

    for line in s.splitlines():
        if line.startswith('humn:'):
            continue
        elif line.startswith('root:'):
            _, a, _, b = line.split()
            o.add(Int(a) == Int(b))
        elif len(line.split()) == 4:
            name, rest = line.split(': ')
            op1, op, op2 = rest.split()
            o.add(Int(name) == OPS[op](Int(op1), Int(op2)))
        else:
            name, rest = line.split(': ')
            o.add(Int(name) == int(rest))

    assert o.check() == sat

    return o.model()[Int('humn')].as_long()


INPUT_S = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
EXPECTED = 301


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
