from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    first, rest = s.split('\n\n')

    lastline_len = len(first.splitlines()[-1].rstrip())
    stacks: list[list[str]]
    stacks = [[] for _ in range((lastline_len + 2) // 4)]

    for line in first.splitlines():
        for i, c in enumerate(line[1::4]):
            if not c.isspace():
                stacks[i].append(c)

    for stack in stacks:
        stack.reverse()

    for instr in rest.splitlines():
        _, n_s, _, f_s, _, d_s = instr.split()
        n, f, d = int(n_s), int(f_s), int(d_s)

        for _ in range(n):
            stacks[d - 1].append(stacks[f - 1].pop())

    return ''.join(stack[-1] if stack else '' for stack in stacks)


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
