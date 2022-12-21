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
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py'
+ python day01/part1.py
68787
> 7531 μs
+ python day01/part2.py
198041
> 7689 μs
+ python day02/part1.py
13268
> 6047 μs
+ python day02/part2.py
15508
> 5889 μs
+ python day03/part1.py
8123
> 1949 μs
+ python day03/part2.py
2620
> 868 μs
+ python day04/part1.py
651
> 4654 μs
+ python day04/part2.py
956
> 4509 μs
+ python day05/part1.py
QPJPLMNNR
> 6565 μs
+ python day05/part2.py
BQDNWJPVJ
> 2408 μs
+ python day06/part1.py
1100
> 5985 μs
+ python day06/part2.py
2421
> 8177 μs
+ python day07/part1.py
1783610
> 18417 μs
+ python day07/part2.py
4370655
> 18053 μs
+ python day08/part1.py
1698
> 27564 μs
+ python day08/part2.py
672280
> 87745 μs
+ python day09/part1.py
6311
> 61124 μs
+ python day09/part2.py
2482
> 61482 μs
+ python day10/part1.py
15880
> 386 μs
+ python day10/part2.py
###..#.....##..####.#..#..##..####..##.
#..#.#....#..#.#....#.#..#..#....#.#..#
#..#.#....#....###..##...#..#...#..#...
###..#....#.##.#....#.#..####..#...#.##
#....#....#..#.#....#.#..#..#.#....#..#
#....####..###.#....#..#.#..#.####..###
> 1063 μs
+ python day11/part1.py
54036
> 13501 μs
+ python day11/part2.py
13237873355
> 181 ms
+ python day12/part1.py
408
> 152 ms
+ python day12/part2.py
399
> 141 ms
+ python day13/part1.py
6656
> 62574 μs
+ python day13/part2.py
19716
> 123 ms
+ python day14/part1.py
610
> 28146 μs
+ python day14/part2.py
27194
> 513 ms
+ python day15/part1.py
5256611
> 3974 ms
+ python day15/part2.py
13337919186981
> 246 ms (z3)
13337919186981
> 6568 ms
+ python day16/part1.py
1595
> 274 ms
+ python day16/part2.py
2189
> 1399 ms
+ python day17/part1.py
3171
> 90752 μs
+ python day17/part2.py
1586627906921
> 3393 ms
+ python day18/part1.py
3494
> 25009 μs
+ python day18/part2.py
2062
> 61109 μs
+ python day19/part1.py
1404
> 21075 ms
+ python day19/part2.py
5880
> 52485 ms
+ python day20/part1.py
13522
> 2833 ms
+ python day20/part2.py
17113168880158
> 28497 ms
+ python day21/part1.py
194058098264286
> 36037 μs
+ python day21/part2.py
3592056845086
> 1240 ms (z3)
Alexandra, please stop cheating
3592056845086
> 84305 μs
```
