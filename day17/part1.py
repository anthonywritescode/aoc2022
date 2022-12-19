from __future__ import annotations

import argparse
import functools
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Piece:
    def __init__(self, places: set[tuple[int, int]]) -> None:
        self.places = frozenset((x, -y) for x, y in places)

    @functools.cached_property
    def height(self) -> int:
        _, by = support.bounds(self.places)
        return by.max - by.min + 1

    @functools.cached_property
    def width(self) -> int:
        bx, _ = support.bounds(self.places)
        return bx.max - bx.min + 1

    def at(self, dx: int, dy: int) -> set[tuple[int, int]]:
        return {(x + dx, y + dy) for x, y in self.places}

    def __hash__(self) -> int:
        return hash(self.places)


PIECES_S = '''\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''
PIECES = tuple(
    Piece(support.parse_coords_hash(piece))
    for piece in PIECES_S.split('\n\n')
)


def format_coords_hash(coords: set[tuple[int, int]]) -> str:
    bx, by = support.bounds(coords)
    return '\n'.join(
        ''.join(
            '#' if (x, y) in coords else ' '
            for x in bx.range
        )
        for y in range(by.max, by.min - 1, -1)
    )


def print_coords_hash(coords: set[tuple[int, int]]) -> None:
    print(format_coords_hash(coords))


def move(
        coords: set[tuple[int, int]],
        piece: Piece,
        x: int,
        y: int,
        direction: str,
) -> int:
    if direction == '<':
        if x == 0 or piece.at(x - 1, y) & coords:
            return x
        else:
            return x - 1
    elif direction == '>':
        if x == 7 - piece.width or piece.at(x + 1, y) & coords:
            return x
        else:
            return x + 1
    else:
        raise NotImplementedError(f'??? {direction=}')


def compute(s: str) -> int:
    s = s.strip()

    pieces = itertools.cycle(PIECES)

    coords = support.parse_coords_hash('#######')
    max_height = 0
    gas = itertools.cycle(s)

    for _ in range(2022):
        piece = next(pieces)
        x = 2
        y = max_height + piece.height + 3

        while True:
            x = move(coords, piece, x, y, next(gas))

            if piece.at(x, y - 1) & coords:
                coords |= piece.at(x, y)
                max_height = max(y, max_height)
                break
            else:
                y -= 1

    return max_height


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 3068


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
