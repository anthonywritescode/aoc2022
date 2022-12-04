-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vals (a INT, b INT, c INT, d INT);
WITH RECURSIVE
    nn (a, b, c, d, rest)
AS (
    SELECT -1, -1, -1, -1, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, '-') - 1),
        SUBSTR(
            nn.rest,
            1 + INSTR(nn.rest, '-'),
            INSTR(nn.rest, ',') - INSTR(nn.rest, '-') - 1
        ),
        SUBSTR(
            nn.rest,
        1 + INSTR(nn.rest, ','),
        INSTR(SUBSTR(nn.rest, 1 + INSTR(nn.rest, ',')), '-') - 1
        ),
        SUBSTR(
            nn.rest,
            1 + INSTR(nn.rest, ',') +
            INSTR(SUBSTR(nn.rest, 1 + INSTR(nn.rest, ',')), '-'),
            INSTR(nn.rest, char(10)) - (
                1 + INSTR(nn.rest, ',') +
                INSTR(SUBSTR(nn.rest, 1 + INSTR(nn.rest, ',')), '-')
            )
        ),
        SUBSTR(nn.rest, 1 + INSTR(nn.rest, char(10)))
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO vals
SELECT a, b, c, d FROM nn WHERE a != -1;

SELECT
    SUM((a <= c AND c <= b) OR (c <= a AND a <= d))
FROM vals;
