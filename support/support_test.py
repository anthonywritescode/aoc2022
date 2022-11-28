from __future__ import annotations

import support


def test_adjacent_4() -> None:
    pts = set(support.adjacent_4(1, 2))
    assert pts == {(0, 2), (2, 2), (1, 3), (1, 1)}


def test_adjacent_8() -> None:
    pts = set(support.adjacent_8(1, 2))
    assert pts == {
        (0, 1), (1, 1), (2, 1),
        (0, 2), (2, 2),
        (0, 3), (1, 3), (2, 3),
    }


def test_parse_coords_int() -> None:
    coords = support.parse_coords_int('123\n456')
    assert coords == {
        (0, 0): 1,
        (1, 0): 2,
        (2, 0): 3,
        (0, 1): 4,
        (1, 1): 5,
        (2, 1): 6,
    }


def test_parse_coords_hash() -> None:
    coords = support.parse_coords_hash(' # \n#  \n')
    assert coords == {(1, 0), (0, 1)}


def test_parse_numbers_split() -> None:
    assert support.parse_numbers_split('1 2') == [1, 2]
    assert support.parse_numbers_split('1\n2\n') == [1, 2]


def test_parse_numbers_comma() -> None:
    assert support.parse_numbers_comma('1,2,3') == [1, 2, 3]
    assert support.parse_numbers_comma('1,2,3\n') == [1, 2, 3]


def test_format_coords_hash() -> None:
    assert support.format_coords_hash({(1, 0), (0, 1)}) == ' #\n# '


def test_direction4() -> None:
    assert support.Direction4.UP.cw is support.Direction4.RIGHT
    assert support.Direction4.UP.ccw is support.Direction4.LEFT
    assert support.Direction4.UP.opposite is support.Direction4.DOWN
    assert support.Direction4.UP.apply(0, 0) == (0, -1)
