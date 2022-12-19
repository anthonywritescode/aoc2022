from __future__ import annotations

import argparse
import collections
import os.path
import re
from typing import Mapping
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

REG = re.compile(r'Each (\w+) robot costs (\d+) (\w+)(?: and (\d+) (\w+))?\.')


def add(*ms: Mapping[str, int]) -> dict[str, int]:
    ret: dict[str, int] = {}
    for m in ms:
        for k, v in m.items():
            ret.setdefault(k, 0)
            ret[k] += v
    return ret


def count(strs: tuple[str, ...]) -> dict[str, int]:
    ret: dict[str, int] = {}
    for s in strs:
        ret.setdefault(s, 0)
        ret[s] += 1
    return ret


def _can_purchase(res: Mapping[str, int], cost: Mapping[str, int]) -> bool:
    return all(res.get(tp, 0) >= n for tp, n in cost.items())


def _negative(cost: Mapping[str, int]) -> dict[str, int]:
    return {tp: -n for tp, n in cost.items()}


class Cost(NamedTuple):
    ore_bot_ore: int
    cla_bot_ore: int
    obs_bot_ore: int
    obs_bot_cla: int
    geo_bot_ore: int
    geo_bot_obs: int


def _compute_one(items: list[tuple[str, str, str, str, str]]) -> int:
    costs: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for bot_tp, n1_s, cost1_s, n2_s, cost2_s in items:
        costs[bot_tp][cost1_s] = int(n1_s)
        if n2_s:
            costs[bot_tp][cost2_s] = int(n2_s)

    cost = Cost(
        ore_bot_ore=costs['ore']['ore'],
        cla_bot_ore=costs['clay']['ore'],
        obs_bot_ore=costs['obsidian']['ore'],
        obs_bot_cla=costs['obsidian']['clay'],
        geo_bot_ore=costs['geode']['ore'],
        geo_bot_obs=costs['geode']['obsidian'],
    )

    max_ore = max(
        cost.ore_bot_ore,
        cost.cla_bot_ore,
        cost.obs_bot_ore,
        cost.geo_bot_ore,
    )

    seen = set()
    best_at: dict[int, int] = {}
    todo = collections.deque([(0, 1, 0, 0, 0, 0, 0, 0, 0)])
    while todo:
        m, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo = todo.popleft()

        ore = min(max_ore * (32 - m), ore)
        cla = min(cost.obs_bot_cla * (32 - m), cla)
        obs = min(cost.geo_bot_obs * (32 - m), obs)
        ore_b = min(ore_b, max_ore)
        cla_b = min(cla_b, cost.obs_bot_cla)
        obs_b = min(obs_b, cost.geo_bot_obs)

        tup = (m, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo)
        if tup in seen:
            continue
        else:
            seen.add(tup)

        best_at[m] = max(best_at.get(m, 0), geo)

        if m == 32:
            continue

        # always buy geode if possible
        if ore >= cost.geo_bot_ore and obs >= cost.geo_bot_obs:
            todo.append((
                m + 1,
                ore_b,
                cla_b,
                obs_b,
                geo_b + 1,
                ore + ore_b - cost.geo_bot_ore,
                cla + cla_b,
                obs + obs_b - cost.geo_bot_obs,
                geo + geo_b,
            ))
            continue

        # can buy obisidan?
        if ore >= cost.obs_bot_ore and cla >= cost.obs_bot_cla:
            todo.append((
                m + 1,
                ore_b,
                cla_b,
                obs_b + 1,
                geo_b,
                ore + ore_b - cost.obs_bot_ore,
                cla + cla_b - cost.obs_bot_cla,
                obs + obs_b,
                geo + geo_b,
            ))

        # can buy clay?
        if ore >= cost.cla_bot_ore:
            todo.append((
                m + 1,
                ore_b,
                cla_b + 1,
                obs_b,
                geo_b,
                ore + ore_b - cost.cla_bot_ore,
                cla + cla_b,
                obs + obs_b,
                geo + geo_b,
            ))

        # can buy ore?
        if ore >= cost.ore_bot_ore:
            todo.append((
                m + 1,
                ore_b + 1,
                cla_b,
                obs_b,
                geo_b,
                ore + ore_b - cost.ore_bot_ore,
                cla + cla_b,
                obs + obs_b,
                geo + geo_b,
            ))

        # buy nothing
        todo.append((
            m + 1,
            ore_b,
            cla_b,
            obs_b,
            geo_b,
            ore + ore_b,
            cla + cla_b,
            obs + obs_b,
            geo + geo_b,
        ))

    return best_at[32]


def compute(s: str) -> int:
    ret = 1

    for line in s.splitlines()[:3]:
        ret *= _compute_one(REG.findall(line))

    return ret


INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''  # noqa: E501
EXPECTED = 56 * 62


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
