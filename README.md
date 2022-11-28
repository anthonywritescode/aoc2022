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
```
