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
> 756 μs
+ python day01/part2.py day01/input.txt
198041
> 789 μs
+ python day02/part1.py day02/input.txt
13268
> 1485 μs
+ python day02/part2.py day02/input.txt
508
> 1533 μs
+ python day03/part1.py day03/input.txt
8123
> 907 μs
+ python day03/part2.py day03/input.txt
2620
> 625 μs
+ python day04/part1.py day04/input.txt
651
> 1722 μs
+ python day04/part2.py day04/input.txt
956
> 1634 μs
+ python day05/part1.py day05/input.txt
QPJPLMNNR
> 1462 μs
+ python day05/part2.py day05/input.txt
BQDNWJPVJ
> 960 μs
+ python day06/part1.py day06/input.txt
1100
> 898 μs
+ python day06/part2.py day06/input.txt
2421
> 2621 μs
+ python day07/part1.py day07/input.txt
1783610
> 17884 μs
+ python day07/part2.py day07/input.txt
4370655
> 18399 μs
+ python day08/part1.py day08/input.txt
1698
> 18528 μs
+ python day08/part2.py day08/input.txt
672280
> 80456 μs
+ python day09/part1.py day09/input.txt
6311
> 32644 μs
+ python day09/part2.py day09/input.txt
2482
> 106 ms
+ python day10/part1.py day10/input.txt
15880
> 193 μs
+ python day10/part2.py day10/input.txt
###..#.....##..####.#..#..##..####..##.
#..#.#....#..#.#....#.#..#..#....#.#..#
#..#.#....#....###..##...#..#...#..#...
###..#....#.##.#....#.#..####..#...#.##
#....#....#..#.#....#.#..#..#.#....#..#
#....####..###.#....#..#.#..#.####..###
> 426 μs
+ python day11/part1.py day11/input.txt
54036
> 1214 μs
+ python day11/part2.py day11/input.txt
13237873355
> 629 ms
+ python day12/part1.py day12/input.txt
408
> 37389 μs
+ python day12/part2.py day12/input.txt
399
> 27576 μs
+ python day13/part1.py day13/input.txt
6656
> 20986 μs
+ python day13/part2.py day13/input.txt
19716
> 31122 μs
+ python day14/part1.py day14/input.txt
610
> 31320 μs
+ python day14/part2.py day14/input.txt
27194
> 2672 ms
```
