from __future__ import annotations

import argparse
import functools
import operator
import os.path
from typing import Callable

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '/': lambda a, b: a // b,
    '*': operator.mul,
}


def compute(s: str) -> int:
    ops: dict[str, int | tuple[Callable[[int, int], int], str, str]] = {}

    for line in s.splitlines():
        if len(line.split()) == 4:
            name, rest = line.split(': ')
            op1, op, op2 = rest.split()
            ops[name] = (OPS[op], op1, op2)
        else:
            name, rest = line.split(': ')
            ops[name] = int(rest)

    @functools.lru_cache
    def _value(name: str) -> int:
        val = ops[name]
        if isinstance(val, int):
            return val
        else:
            fn, left, right = val
            return fn(_value(left), _value(right))

    return _value('root')


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
EXPECTED = 152


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
