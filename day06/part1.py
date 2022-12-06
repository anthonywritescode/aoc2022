from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    d: collections.deque[str] = collections.deque(maxlen=4)

    for i, c in enumerate(s.strip()):
        d.append(c)

        if len(d) == d.maxlen and len(set(d)) == d.maxlen:
            return i + 1

    raise NotImplementedError('wat')


INPUT_S = '''\
bvwbjplbgvbhsrlpgdmjqwftvncz
'''
EXPECTED = 5


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
