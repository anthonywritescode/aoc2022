from __future__ import annotations

import argparse
import collections
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    start_x, = (x for x, c in enumerate(lines[0]) if c == '.')
    start_x -= 1
    start_y = -1
    target_x, = (x for x, c in enumerate(lines[-1]) if c == '.')
    target_x -= 1
    target_y = len(lines) - 2

    lines = [line[1:-1] for line in lines[1:-1]]
    new_s = ''.join(lines)

    width = len(lines[0])
    height = len(lines)

    up = tuple(
        int(re.sub('[^^]', '0', line).replace('^', '1')[::-1], 2)
        for line in lines
    )
    down = tuple(
        int(re.sub('[^v]', '0', line).replace('v', '1')[::-1], 2)
        for line in lines
    )
    left = tuple(
        int(re.sub('[^<]', '0', new_s[i::width]).replace('<', '1')[::-1], 2)
        for i in range(width)
    )
    right = tuple(
        int(re.sub('[^>]', '0', new_s[i::width]).replace('>', '1')[::-1], 2)
        for i in range(width)
    )

    seen = set()
    todo = collections.deque([(0, 0, start_x, start_y, up, down, left, right)])
    while todo:
        tup = todo.popleft()

        if tup in seen:
            continue
        else:
            seen.add(tup)

        depth, phase, x, y, up, down, left, right = tup

        if (x, y) != (start_x, start_y) and (x, y) != (target_x, target_y):
            if y != -1 and (up[y] | down[y]) & (1 << x):
                continue
            elif y != -1 and (left[x] | right[x]) & (1 << y):
                continue

        if phase == 3 and (x, y) == (target_x, target_y):
            return depth

        next_masks = (
            up[1:] + (up[0],),
            (down[-1],) + down[:-1],
            left[1:] + (left[0],),
            (right[-1],) + right[:-1],
        )

        # wait
        todo.append((depth + 1, phase, x, y, *next_masks))

        # move
        for (cx, cy) in support.adjacent_4(x, y):
            if 0 <= cx < width and 0 <= cy < height:
                todo.append((depth + 1, phase, cx, cy, *next_masks))
            elif phase == 0 and (cx, cy) == (target_x, target_y):
                todo.append((depth + 1, 1, cx, cy, *next_masks))
            elif phase == 1 and (cx, cy) == (start_x, start_y):
                todo.append((depth + 1, 2, cx, cy, *next_masks))
            elif phase == 2 and (cx, cy) == (target_x, target_y):
                todo.append((depth + 1, 3, cx, cy, *next_masks))

    raise NotImplementedError('???')


INPUT_S = '''\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''
EXPECTED = 54


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

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
