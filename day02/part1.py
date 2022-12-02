from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

shape = {'R': 1, 'P': 2, 'S': 3}
win = {'R': 'S', 'P': 'R', 'S': 'P'}
trans = {
    'A': 'R', 'B': 'P', 'C': 'S',
    'X': 'R', 'Y': 'P', 'Z': 'S',
}


def compute(s: str) -> int:
    for k, v in trans.items():
        s = s.replace(k, v)

    n = 0
    for line in s.splitlines():
        a, b = line.split()
        if a == b:
            n += 3
        elif win[a] != b:
            n += 6
        else:
            pass
        n += shape[b]
    return n


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
