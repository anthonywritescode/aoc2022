from __future__ import annotations

import argparse
import os.path
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def adjacent_faces(
        x: int,
        y: int,
        z: int,
) -> Generator[tuple[int, int, int], None, None]:
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def compute(s: str) -> int:
    count = 0
    coords = set()

    for line in s.splitlines():
        x, y, z = map(int, line.split(','))
        count += 6
        for cx, cy, cz in adjacent_faces(x, y, z):
            if (cx, cy, cz) in coords:
                count -= 2
        coords.add((x, y, z))

    return count


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 64


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
