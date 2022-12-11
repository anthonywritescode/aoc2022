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

SELECT SUM(i * x) FROM vals WHERE i IN (20, 60, 100, 140, 180, 220);
