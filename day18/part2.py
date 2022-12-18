from __future__ import annotations

import argparse
import os.path
import sys
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


def surface_area(pts: set[tuple[int, int, int]]) -> int:
    count = 0
    coords = set()

    for pt in pts:
        count += 6
        for cpt in adjacent_faces(*pt):
            if cpt in coords:
                count -= 2
        coords.add(pt)
    return count


def compute(s: str) -> int:
    count = 0
    coords = set()

    min_x = sys.maxsize
    max_x = -sys.maxsize
    min_y = sys.maxsize
    max_y = -sys.maxsize
    min_z = sys.maxsize
    max_z = -sys.maxsize

    for line in s.splitlines():
        x, y, z = map(int, line.split(','))
        count += 6
        for cx, cy, cz in adjacent_faces(x, y, z):
            if (cx, cy, cz) in coords:
                count -= 2
        coords.add((x, y, z))

        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    all_coords = {
        (x, y, z)
        for x in range(min_x - 1, max_x + 2)
        for y in range(min_y - 1, max_y + 2)
        for z in range(min_z - 1, max_z + 2)
    }

    remaining = all_coords - coords

    todo = [min(remaining)]
    while todo:
        pt = todo.pop()
        if pt in remaining:
            remaining.discard(pt)
        else:
            continue

        for cpt in adjacent_faces(*pt):
            todo.append(cpt)

    return count - surface_area(remaining)


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
EXPECTED = 58


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
