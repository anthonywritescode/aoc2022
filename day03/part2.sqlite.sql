-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE folded (g, i, c);
WITH RECURSIVE
    nn (i, c, rest)
AS (
    SELECT
        0,
        (SELECT SUBSTR(s, 1, 1) FROM input),
        (SELECT SUBSTR(s, 2) || char(10) FROM input)
    UNION ALL
    SELECT
        CASE
            WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN nn.i + 1
            ELSE nn.i
        END,
        CASE
            WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN SUBSTR(nn.rest, 2, 1)
            ELSE SUBSTR(nn.rest, 1, 1)
        END,
        CASE
            WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN SUBSTR(nn.rest, 3)
            ELSE SUBSTR(nn.rest, 2)
        END
    FROM nn
    WHERE nn.rest != char(10)
)
INSERT INTO folded
SELECT i / 3, i % 3, c FROM nn;

SELECT SUM(
    CASE
        WHEN UNICODE(c) < 97 THEN 27 + UNICODE(c) - UNICODE('A')
        ELSE 1 + UNICODE(c) - UNICODE('a')
    END
)
FROM (
    SELECT folded.c
    FROM folded
    INNER JOIN folded folded2 ON folded.g = folded2.g AND folded.c = folded2.c
    INNER JOIN folded folded3 ON folded.g = folded3.g AND folded.c = folded3.c
    WHERE folded.i = 0 AND folded2.i = 1 AND folded3.i = 2
    GROUP BY folded.g
);
