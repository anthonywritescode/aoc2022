advent of code 2022
===================

https://adventofcode.com/2022

### stream / youtube

- [Streamed daily on twitch](https://twitch.tv/anthonywritescode)
- [Streams uploaded to youtube afterwards](https://www.youtube.com/@anthonywritescode-vods)

### about

for 2022, I'm planning to implement in python

### timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python day01/part1.py day01/input.txt
68787
> 7531 μs
+ python day01/part2.py day01/input.txt
198041
> 7689 μs
+ python day02/part1.py day02/input.txt
13268
> 6047 μs
+ python day02/part2.py day02/input.txt
15508
> 5889 μs
+ python day03/part1.py day03/input.txt
8123
> 1949 μs
+ python day03/part2.py day03/input.txt
2620
> 868 μs
+ python day04/part1.py day04/input.txt
651
> 4654 μs
+ python day04/part2.py day04/input.txt
956
> 4509 μs
+ python day05/part1.py day05/input.txt
QPJPLMNNR
> 6565 μs
+ python day05/part2.py day05/input.txt
BQDNWJPVJ
> 2408 μs
+ python day06/part1.py day06/input.txt
1100
> 5985 μs
+ python day06/part2.py day06/input.txt
2421
> 8177 μs
+ python day07/part1.py day07/input.txt
1783610
> 18417 μs
+ python day07/part2.py day07/input.txt
4370655
> 18053 μs
+ python day08/part1.py day08/input.txt
1698
> 27564 μs
+ python day08/part2.py day08/input.txt
672280
> 87745 μs
+ python day09/part1.py day09/input.txt
6311
> 61124 μs
+ python day09/part2.py day09/input.txt
2482
> 61482 μs
+ python day10/part1.py day10/input.txt
15880
> 386 μs
+ python day10/part2.py day10/input.txt
###..#.....##..####.#..#..##..####..##.
#..#.#....#..#.#....#.#..#..#....#.#..#
#..#.#....#....###..##...#..#...#..#...
###..#....#.##.#....#.#..####..#...#.##
#....#....#..#.#....#.#..#..#.#....#..#
#....####..###.#....#..#.#..#.####..###
> 1063 μs
+ python day11/part1.py day11/input.txt
54036
> 13501 μs
+ python day11/part2.py day11/input.txt
13237873355
> 181 ms
+ python day12/part1.py day12/input.txt
408
> 152 ms
+ python day12/part2.py day12/input.txt
399
> 141 ms
+ python day13/part1.py day13/input.txt
6656
> 62574 μs
+ python day13/part2.py day13/input.txt
19716
> 123 ms
+ python day14/part1.py day14/input.txt
610
> 28146 μs
+ python day14/part2.py day14/input.txt
27194
> 513 ms
+ python day15/part1.py day15/input.txt
5256611
> 3974 ms
+ python day15/part2.py day15/input.txt
13337919186981
> 246 ms (z3)
13337919186981
> 6568 ms
+ python day16/part1.py day16/input.txt
1595
> 274 ms
+ python day16/part2.py day16/input.txt
2189
> 1399 ms
+ python day17/part1.py day17/input.txt
3171
> 90752 μs
+ python day17/part2.py day17/input.txt
1586627906921
> 3393 ms
+ python day18/part1.py day18/input.txt
3494
> 25009 μs
+ python day18/part2.py day18/input.txt
2062
> 61109 μs
+ python day19/part1.py day19/input.txt
1404
> 21075 ms
+ python day19/part2.py day19/input.txt
5880
> 52485 ms
```
