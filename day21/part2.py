from __future__ import annotations

import argparse
import contextlib
import functools
import os.path
import sys

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
OPS2 = {
    **OPS,
    '/': lambda a, b: a // b,
}


def compute_z3(s: str) -> int:
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


def compute(s: str) -> int:
    ops: dict[str, int | tuple[str, str, str]] = {}

    root_left = root_right = None
    for line in s.splitlines():
        if line.startswith('humn:'):
            continue
        elif line.startswith('root:'):
            _, root_left, _, root_right = line.split()
        elif len(line.split()) == 4:
            name, rest = line.split(': ')
            op1, op, op2 = rest.split()
            ops[name] = (op1, op, op2)
        else:
            name, rest = line.split(': ')
            ops[name] = int(rest)

    assert root_left is not None and root_right is not None

    @functools.lru_cache
    def _value(s: str) -> int:
        val = ops[s]
        if isinstance(val, int):
            return val
        else:
            lhs_s, op, rhs_s = val
            return OPS2[op](_value(lhs_s), _value(rhs_s))

    right_val = _value(root_right)
    assert isinstance(right_val, int)

    expr = ops[root_left]
    with contextlib.suppress(KeyError):  # our loop ends when we lookup humn
        while True:
            assert not isinstance(expr, int), expr
            lhs_s, op, rhs_s = expr
            try:
                lhs = _value(lhs_s)
            except KeyError:  # this side contains the variable!
                rhs = _value(rhs_s)

                if op == '*':
                    right_val //= rhs
                elif op == '/':
                    right_val *= rhs
                elif op == '+':
                    right_val -= rhs
                elif op == '-':
                    right_val += rhs
                else:
                    raise AssertionError('unreachable')

                expr = ops[lhs_s]
            else:
                if op == '-':
                    right_val -= lhs
                    right_val *= -1
                elif op == '+':
                    right_val -= lhs
                elif op == '*':
                    right_val //= lhs
                elif op == '/':
                    right_val = lhs // right_val
                else:
                    raise AssertionError('unreachable')
                expr = ops[rhs_s]

    return right_val


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

    with open(args.data_file) as f, support.timing('z3'):
        print(compute_z3(f.read()), file=sys.stderr)

    print('Alexandra, please stop cheating', file=sys.stderr)

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
