from __future__ import annotations

import argparse
import functools
import os.path
from typing import Callable
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def add(val: int, n: int) -> int:
    return val + n


def mult(val: int, n: int) -> int:
    return val * n


def square(val: int) -> int:
    return val * val


class Monk(NamedTuple):
    items: list[int]
    fn: Callable[[int], int]
    mod: int
    true_target: int
    false_target: int


def compute(s: str) -> int:
    monks = []
    for part in s.split('\n\n'):
        lines = part.splitlines()
        starting = [int(s) for s in lines[1].split(': ')[1].split(', ')]
        if 'old * old' in lines[2]:
            fn = square
        elif ' + ' in lines[2]:
            fn = functools.partial(add, n=int(lines[2].split()[-1]))
        elif ' * ' in lines[2]:
            fn = functools.partial(mult, n=int(lines[2].split()[-1]))
        else:
            raise AssertionError(lines[2])
        mod = int(lines[3].split()[-1])
        true_target = int(lines[4].split()[-1])
        false_target = int(lines[5].split()[-1])
        monks.append(Monk(starting, fn, mod, true_target, false_target))

    seen = [0] * len(monks)

    for _ in range(20):
        for i, monk in enumerate(monks):
            for item in monk.items:
                seen[i] += 1

                item = monk.fn(item) // 3
                if item % monk.mod == 0:
                    monks[monk.true_target].items.append(item)
                else:
                    monks[monk.false_target].items.append(item)

            monk.items.clear()

    seen.sort()
    return seen[-1] * seen[-2]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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
