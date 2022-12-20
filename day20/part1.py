from __future__ import annotations

import argparse
import collections
import os.path
from unittest import mock

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    orig_numbers = support.parse_numbers_split(s)
    numbers = collections.deque(list(enumerate(orig_numbers)))

    for i, num in enumerate(orig_numbers):
        idx = numbers.index((i, mock.ANY))
        numbers.rotate(-idx)
        assert numbers.popleft() == (i, num)
        numbers.rotate(-num)
        numbers.appendleft((i, num))

    idx_0 = numbers.index((mock.ANY, 0))
    return sum(
        numbers[(idx_0 + i) % len(numbers)][1]
        for i in (1000, 2000, 3000)
    )


INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 3


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
