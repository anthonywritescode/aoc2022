from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)
    visible = set()

    bx, by = support.bounds(coords)

    for y in by.range:
        # down
        val = coords[(y, bx.min)]
        visible.add((y, bx.min))
        for x in range(bx.min + 1, bx.max + 1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

        # up
        val = coords[(y, bx.max)]
        visible.add((y, bx.max))
        for x in range(bx.max, -1, -1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

    for x in bx.range:
        # right
        val = coords[(by.min, x)]
        visible.add((by.min, x))
        for y in range(by.min + 1, by.max + 1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

        # left
        val = coords[(by.max, x)]
        visible.add((by.max, x))
        for y in range(by.max, -1, -1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

    return len(visible)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
