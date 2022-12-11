-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vals (i INT, x INT);
WITH RECURSIVE
    nn (i, x, val, n, rest)
AS (
    SELECT 0, 1, 0, 0, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        nn.i + 1,
        CASE WHEN nn.n = 0 THEN nn.x + nn.val ELSE nn.x END,
        CASE
            WHEN nn.n = 0 THEN
                CASE
                    WHEN nn.rest LIKE 'noop%' THEN 0
                    ELSE SUBSTR(nn.rest, 6, INSTR(nn.rest, char(10)) - 6)
                END
            ELSE nn.val
        END,
        CASE
            WHEN nn.n = 0 THEN
                CASE
                    WHEN nn.rest LIKE 'noop%' THEN 0
                    ELSE 1
                END
            ELSE 0
        END,
        CASE
            WHEN nn.n = 0 THEN SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            ELSE nn.rest
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO vals
SELECT i, x FROM nn;

WITH RECURSIVE
    nn (i, s)
AS (
    SELECT 0, ''
    UNION ALL
    SELECT
        nn.i + 1,
        nn.s || (
            CASE (SELECT x - 1 <= ((i - 1) % 40) AND ((i - 1) % 40) <= x + 1 FROM vals WHERE vals.i == nn.i + 1)
                WHEN 1 THEN '#'
                WHEN 0 THEN '.'
            END
        ) || (
            CASE
                WHEN (nn.i + 1) % 40 == 0 AND nn.i < 239 THEN char(10)
                ELSE ''
            END
        )
    FROM nn
    WHERE nn.i <= (SELECT MAX(i) FROM vals)
)
SELECT MAX(s) FROM nn;
