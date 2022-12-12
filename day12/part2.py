from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAPPED = {
    'S': chr(ord('a') - 1),
    'E': chr(ord('z') + 1),
}


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(y, x)] = c
            if c == 'E':
                end = (y, x)

    assert end is not None

    seen = set()
    todo = [(0, end)]

    while todo:
        cost, pos = heapq.heappop(todo)

        if coords[pos] == 'a':
            return cost
        elif pos in seen:
            continue
        else:
            seen.add(pos)

        for cand in support.adjacent_4(*pos):
            if cand in coords:
                current_c = MAPPED.get(coords[pos], coords[pos])
                cand_c = MAPPED.get(coords[cand], coords[cand])
                if ord(cand_c) - ord(current_c) >= -1:
                    heapq.heappush(todo, (cost + 1, cand))

    raise AssertionError('wat')


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
