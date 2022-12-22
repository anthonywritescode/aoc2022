from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    map_s, dirs = s.split('\n\n')

    coords = {}
    for y, line in enumerate(map_s.splitlines()):
        for x, c in enumerate(line):
            if c in '.#':
                coords[(x, y)] = c

    bx, by = support.bounds(coords)
    y = by.min
    x = min(x for (x, y) in coords if y == 0)
    direction = support.Direction4.RIGHT

    for part in re.split('([RL])', dirs):
        if part == 'R':
            direction = direction.cw
        elif part == 'L':
            direction = direction.ccw
        else:
            n = int(part)
            for _ in range(n):
                cand = direction.apply(x, y)
                if cand not in coords:
                    if direction is support.Direction4.RIGHT:
                        cand_x = min(cx for (cx, cy) in coords if cy == y)
                        cand = (cand_x, y)
                    elif direction is support.Direction4.LEFT:
                        cand_x = max(cx for (cx, cy) in coords if cy == y)
                        cand = (cand_x, y)
                    elif direction is support.Direction4.UP:
                        cand_y = max(cy for (cx, cy) in coords if cx == x)
                        cand = (x, cand_y)
                    elif direction is support.Direction4.DOWN:
                        cand_y = min(cy for (cx, cy) in coords if cx == x)
                        cand = (x, cand_y)
                    else:
                        raise NotImplementedError(direction)

                if coords[cand] == '#':
                    break
                else:
                    x, y = cand

    facing = {
        support.Direction4.RIGHT: 0,
        support.Direction4.LEFT: 2,
        support.Direction4.UP: 3,
        support.Direction4.DOWN: 1,
    }

    return 1000 * (y + 1) + 4 * (x + 1) + facing[direction]


INPUT_S = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
EXPECTED = 6032


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
