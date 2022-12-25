from __future__ import annotations

import argparse
import math
import os.path
import sys

import pytest
from z3 import Int
from z3 import Optimize
from z3 import sat

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

REV = {
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '=',
}


def encode_z3(n: int) -> str:
    near = int(math.log(n, 5))
    for nterms in (near - 1, near, near + 1):
        o = Optimize()
        ints = []
        for i in range(nterms):
            this_int = Int(f'i_{i}')
            o.add(this_int <= 2)
            o.add(this_int >= -2)
            ints.append(this_int * (5 ** (nterms - i - 1)))
        o.add(sum(ints) == n)

        if o.check() == sat:
            m = o.model()
            return ''.join(
                REV[m[Int(f'i_{i}')].as_long()]
                for i in range(nterms)
            )

    raise AssertionError('unreachable')


def encode(n: int) -> str:
    ret = ''
    while n:
        rem = n % 5
        if rem <= 2:
            ret += str(rem)
        else:
            ret += {3: '=', 4: '-'}[rem]

        n //= 5
        n += rem // 3

    return ret[::-1]


def compute_value(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        n = 0
        for i, c in enumerate(reversed(line)):
            if c.isdigit():
                n += int(c) * (5 ** i)
            elif c == '-':
                n -= 1 * (5 ** i)
            elif c == '=':
                n -= 2 * (5 ** i)
        ret += n
    return ret


def compute_z3(s: str) -> str:
    return encode_z3(compute_value(s))


def compute(s: str) -> str:
    return encode(compute_value(s))


INPUT_S = '''\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''
EXPECTED = '2=-1=0'


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

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
