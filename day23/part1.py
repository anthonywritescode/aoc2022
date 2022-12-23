from __future__ import annotations

import argparse
import collections
import os.path
import sys

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_hash(s)

    choices = collections.deque([
        (support.Direction4.UP, ((-1, -1), (0, -1), (1, -1))),
        (support.Direction4.DOWN, ((-1, 1), (0, 1), (1, 1))),
        (support.Direction4.LEFT, ((-1, 1), (-1, 0), (-1, -1))),
        (support.Direction4.RIGHT, ((1, 1), (1, 0), (1, -1))),
    ])

    for _ in range(10):
        moves: dict[tuple[int, int], list[tuple[int, int]]]
        moves = collections.defaultdict(list)

        for x, y in coords:
            if all(
                    (cx, cy) not in coords
                    for cx, cy in support.adjacent_8(x, y)
            ):
                continue

            for cand_dir, cand_points in choices:
                if all(
                    (x + dx, y + dy) not in coords
                    for dx, dy in cand_points
                ):
                    moves[cand_dir.apply(x, y)].append((x, y))
                    break

        moved = {k: v[0] for k, v in moves.items() if len(v) == 1}
        coords = (coords - set(moved.values())) | moved.keys()

        choices.rotate(-1)

    bx, by = support.bounds(coords)
    return (bx.max - bx.min + 1) * (by.max - by.min + 1) - len(coords)


INPUT_S = '''\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''
EXPECTED = 110


@ pytest.mark.parametrize(
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

    print('Alexandra, call me', file=sys.stderr)

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
