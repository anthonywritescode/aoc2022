from __future__ import annotations

import argparse
import curses
import enum
import os.path
import re
from typing import Callable
from unittest import mock

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


Face = enum.Enum('Face', 'TOP BACK LEFT FRONT RIGHT BOTTOM')


def ccw_pt(x: int, y: int, *, size: int) -> tuple[int, int]:
    return (y, size - x - 1)


def ccw(coords: set[tuple[int, int]], *, size: int) -> set[tuple[int, int]]:
    return {ccw_pt(x, y, size=size) for (x, y) in coords}


def cw(coords: set[tuple[int, int]], *, size: int) -> set[tuple[int, int]]:
    return ccw(ccw(ccw(coords, size=size), size=size), size=size)


def compute_curses(stdscr: curses._CursesWindow, s: str) -> int:
    map_s, dirs = s.split('\n\n')

    lines = map_s.splitlines()

    if len(lines[0]) < 50:
        size = 4

        # small input
        top = '\n'.join(line[8:12] for line in lines[:4])
        front = '\n'.join(line[8:12] for line in lines[4:8])
        bottom = '\n'.join(line[8:12] for line in lines[8:12])

        back = '\n'.join(line[:4] for line in lines[4:8])
        left = '\n'.join(line[4:8] for line in lines[4:8])
        right = '\n'.join(line[12:16] for line in lines[8:12])

        coords = {
            Face.FRONT: support.parse_coords_hash(front),
            Face.TOP: support.parse_coords_hash(top),
            Face.BOTTOM: support.parse_coords_hash(bottom),
            Face.BACK: support.parse_coords_hash(back),
            Face.LEFT: support.parse_coords_hash(left),

            Face.RIGHT: ccw(support.parse_coords_hash(right), size=size),
        }

        def back_to_orig_right(x: int, y: int) -> tuple[int, int]:
            x, y = ccw_pt(x, y, size=size)
            return x + size * 3, y + size * 2

        back_to_orig = {
            Face.FRONT: lambda x, y: (x + size * 2, y + size),
            Face.TOP: lambda x, y: (x + size * 2, y),
            Face.BACK: lambda x, y: (x, y + size),
            Face.LEFT: lambda x, y: (x + size, y + size),
            Face.BOTTOM: lambda x, y: (x + size * 2, y + size * 2),
            Face.RIGHT: back_to_orig_right,
        }
        back_to_orig_dir: dict[Face, Callable[[support.Direction4], support.Direction4]] = {  # noqa: E501
            Face.FRONT: lambda d: d,
            Face.TOP: lambda d: d,
            Face.BACK: lambda d: d,
            Face.LEFT: lambda d: d,
            Face.BOTTOM: lambda d: d,
            Face.RIGHT: lambda d: d.cw,
        }
    else:
        # big input
        size = 50

        # NO ROTATE
        front = '\n'.join(line[50:100] for line in lines[50:100])
        top = '\n'.join(line[50:100] for line in lines[:50])
        bottom = '\n'.join(line[50:100] for line in lines[100:150])

        # CCW
        right = '\n'.join(line[100:150] for line in lines[:50])
        left = '\n'.join(line[:50] for line in lines[100:150])
        back = '\n'.join(line[:50] for line in lines[150:200])

        coords = {
            Face.FRONT: support.parse_coords_hash(front),
            Face.TOP: support.parse_coords_hash(top),
            Face.BOTTOM: support.parse_coords_hash(bottom),

            Face.BACK: cw(support.parse_coords_hash(back), size=size),
            Face.LEFT: cw(support.parse_coords_hash(left), size=size),
            Face.RIGHT: cw(support.parse_coords_hash(right), size=size),
        }

        def back_to_orig_left(x: int, y: int) -> tuple[int, int]:
            x, y = ccw_pt(x, y, size=size)
            return x, y + size * 2

        back_to_orig = {
            Face.LEFT: back_to_orig_left,
        }
        back_to_orig_dir = {
            Face.LEFT: lambda d: d.ccw,
        }

    x, y = 0, 0
    face = Face.TOP
    direction = support.Direction4.RIGHT

    def render() -> None:
        if os.environ.get('MODE') != 'manual':
            return

        pad = 2

        offsets = {
            Face.TOP: (1 + (pad + size) * 2, 1),
            Face.BACK: (1, 1 + (pad + size)),
            Face.LEFT: (1 + (pad + size), 1 + (pad + size)),
            Face.FRONT: (1 + (pad + size) * 2, 1 + (pad + size)),
            Face.RIGHT: (1 + (pad + size) * 3, 1 + (pad + size)),
            Face.BOTTOM: (1 + (pad + size) * 2, 1 + (pad + size) * 2),
        }

        def _grid(face: Face, grid: set[tuple[int, int]]) -> None:
            for yi in range(size):
                stdscr.addstr(
                    yi + offsets[face][1], offsets[face][0],
                    ''.join(
                        '#' if (xi, yi) in grid else '.'
                        for xi in range(size)
                    ),
                )

        direction_s = {
            support.Direction4.UP: '^',
            support.Direction4.DOWN: 'v',
            support.Direction4.RIGHT: '>',
            support.Direction4.LEFT: '<',
        }

        if size >= 50:
            stdscr.insstr(0, 0, f'{str(face):<100}')

            for yi in range(size):
                stdscr.addstr(
                    yi + 1, 1,
                    ''.join(
                        '#' if (xi, yi) in coords[face] else '.'
                        for xi in range(size)
                    ),
                )

            stdscr.addstr(
                1 + y, 1 + x,
                direction_s[direction],
            )
        else:
            for k, v in coords.items():
                _grid(k, v)

            stdscr.addstr(
                offsets[face][1] + y, offsets[face][0] + x,
                direction_s[direction],
            )

        stdscr.move(0, 0)
        if os.environ.get('MODE') != 'AUTO':
            stdscr.get_wch()

    render()

    for part in re.split('([RL])', dirs):
        if part == 'R':
            direction = direction.cw
        elif part == 'L':
            direction = direction.ccw
        else:
            n = int(part)
            for _ in range(n):
                cand_face = face
                cand_direction = direction

                if x == 0 and direction is support.Direction4.LEFT:
                    trans = {
                        Face.TOP: (
                            Face.LEFT,
                            lambda x, y: (y, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.FRONT: (
                            Face.LEFT,
                            lambda x, y: (size - 1, y),
                            support.Direction4.LEFT,
                        ),
                        Face.RIGHT: (
                            Face.FRONT,
                            lambda x, y: (size - 1, y),
                            support.Direction4.LEFT,
                        ),
                        Face.LEFT: (
                            Face.BACK,
                            lambda x, y: (size - 1, y),
                            support.Direction4.LEFT,
                        ),
                        Face.BACK: (
                            Face.RIGHT,
                            lambda x, y: (size - 1, y),
                            support.Direction4.LEFT,
                        ),
                        Face.BOTTOM: (
                            Face.LEFT,
                            lambda x, y: (size - y - 1, size - 1),
                            support.Direction4.UP,
                        ),
                    }

                    cand_face, fn, cand_direction = trans[face]
                    cand_x, cand_y = fn(x, y)

                elif x == size - 1 and direction is support.Direction4.RIGHT:
                    trans = {
                        Face.TOP: (
                            Face.RIGHT,
                            lambda x, y: (size - y - 1, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.FRONT: (
                            Face.RIGHT,
                            lambda x, y: (0, y),
                            support.Direction4.RIGHT,
                        ),
                        Face.RIGHT: (
                            Face.BACK,
                            lambda x, y: (0, y),
                            support.Direction4.RIGHT,
                        ),
                        Face.BACK: (
                            Face.LEFT,
                            lambda x, y: (0, y),
                            support.Direction4.RIGHT,
                        ),
                        Face.LEFT: (
                            Face.FRONT,
                            lambda x, y: (0, y),
                            support.Direction4.RIGHT,
                        ),
                        Face.BOTTOM: (
                            Face.RIGHT,
                            lambda x, y: (y, size - 1),
                            support.Direction4.UP,
                        ),
                    }

                    cand_face, fn, cand_direction = trans[face]
                    cand_x, cand_y = fn(x, y)
                elif y == 0 and direction == support.Direction4.UP:
                    trans = {
                        Face.TOP: (
                            Face.BACK,
                            lambda x, y: (size - x - 1, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.FRONT: (
                            Face.TOP,
                            lambda x, y: (x, size - 1),
                            support.Direction4.UP,
                        ),
                        Face.RIGHT: (
                            Face.TOP,
                            lambda x, y: (size - 1, size - x - 1),
                            support.Direction4.LEFT,
                        ),
                        Face.BACK: (
                            Face.TOP,
                            lambda x, y: (size - x - 1, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.LEFT: (
                            Face.TOP,
                            lambda x, y: (0, x),
                            support.Direction4.RIGHT,
                        ),
                        Face.BOTTOM: (
                            Face.FRONT,
                            lambda x, y: (x, size - 1),
                            support.Direction4.UP,
                        ),
                    }

                    cand_face, fn, cand_direction = trans[face]
                    cand_x, cand_y = fn(x, y)
                elif y == size - 1 and direction is support.Direction4.DOWN:
                    trans = {
                        Face.TOP: (
                            Face.FRONT,
                            lambda x, y: (x, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.FRONT: (
                            Face.BOTTOM,
                            lambda x, y: (x, 0),
                            support.Direction4.DOWN,
                        ),
                        Face.RIGHT: (
                            Face.BOTTOM,
                            lambda x, y: (size - 1, x),
                            support.Direction4.LEFT,
                        ),
                        Face.BACK: (
                            Face.BOTTOM,
                            lambda x, y: (size - x - 1, size - 1),
                            support.Direction4.UP,
                        ),
                        Face.LEFT: (
                            Face.BOTTOM,
                            lambda x, y: (0, size - x - 1),
                            support.Direction4.RIGHT,
                        ),
                        Face.BOTTOM: (
                            Face.BACK,
                            lambda x, y: (size - x - 1, size - 1),
                            support.Direction4.UP,
                        ),
                    }

                    cand_face, fn, cand_direction = trans[face]
                    cand_x, cand_y = fn(x, y)
                else:
                    cand_face = face
                    cand_direction = direction
                    cand_x, cand_y = direction.apply(x, y)

                assert 0 <= cand_x < size, cand_x
                assert 0 <= cand_y < size, cand_y

                if (cand_x, cand_y) in coords[cand_face]:
                    break
                else:
                    render()
                    x, y = cand_x, cand_y
                    face = cand_face
                    direction = cand_direction

    # XXX: all the subtractions are off by 1!
    # XXX: probably off by one in ccw also!

    facing = {
        support.Direction4.RIGHT: 0,
        support.Direction4.LEFT: 2,
        support.Direction4.UP: 3,
        support.Direction4.DOWN: 1,
    }

    x, y = back_to_orig[face](x, y)
    direction = back_to_orig_dir[face](direction)

    return 1000 * (y + 1) + 4 * (x + 1) + facing[direction]


def compute(s: str) -> int:
    return curses.wrapper(compute_curses, s)


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
EXPECTED = 5031


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    with mock.patch.object(
        curses,
        'wrapper',
        lambda fn, *args, **kwargs: fn(mock.Mock(), *args, **kwargs),
    ):
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
