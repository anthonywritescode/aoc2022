from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PT = (500, 0)


def compute(s: str) -> int:
    coords = set()
    for line in s.splitlines():
        points = line.split(' -> ')
        prev_x, prev_y = support.parse_point_comma(points[0])
        for point in points[1:]:
            cand_x, cand_y = support.parse_point_comma(point)
            if cand_x == prev_x:
                for y in range(min(cand_y, prev_y), max(cand_y, prev_y) + 1):
                    coords.add((cand_x, y))
            else:
                for x in range(min(cand_x, prev_x), max(cand_x, prev_x) + 1):
                    coords.add((x, cand_y))
            prev_x, prev_y = cand_x, cand_y

    max_y = max(y for _, y in coords)

    i = 0

    while True:
        px, py = 500, 0
        while True:
            if (px, py) in coords:
                return i
            elif py == max_y + 1:
                coords.add((px, py))
                break
            elif (px, py + 1) not in coords:
                py += 1
            elif (px - 1, py + 1) not in coords:
                px -= 1
                py += 1
            elif (px + 1, py + 1) not in coords:
                px += 1
                py += 1
            else:
                coords.add((px, py))
                break

        i += 1

    raise AssertionError('unreachable')


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
