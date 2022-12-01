-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vals (n);
WITH RECURSIVE
    nn (i, n, rest)
AS (
    SELECT 0, 0, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        CASE SUBSTR(nn.rest, 0, INSTR(nn.rest, char(10)))
            WHEN '' THEN nn.i + 1
            ELSE nn.i
        END,
        CASE SUBSTR(nn.rest, 0, INSTR(nn.rest, char(10)))
            WHEN '' THEN 0
            ELSE nn.n + SUBSTR(nn.rest, 0, INSTR(nn.rest, char(10)))
        END,
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO vals
SELECT MAX(nn.n) FROM nn GROUP BY nn.i;

SELECT SUM(n) FROM (SELECT * FROM VALS ORDER BY n DESC LIMIT 3);
