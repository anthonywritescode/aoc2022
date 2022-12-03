-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE parts (i, l, r);
WITH RECURSIVE
    nn (i, l, r, rest)
AS (
    SELECT -1, NULL, NULL, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        nn.i + 1,
        SUBSTR(nn.rest, 1, INSTR(nn.rest, char(10)) / 2),
        SUBSTR(nn.rest, 1 + INSTR(nn.rest, char(10)) / 2, INSTR(nn.rest, char(10)) / 2),
        SUBSTR(nn.rest, 1 + INSTR(nn.rest, char(10)))
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO parts
SELECT i, l, r FROM nn WHERE l IS NOT NULL;

CREATE TABLE folded(i, l, c);
WITH RECURSIVE
    nn (i, l, c, rest)
AS (
    SELECT
        0, 1,
        (SELECT SUBSTR(l, 1, 1) FROM parts WHERE i = 0),
        (SELECT SUBSTR(l, 2) FROM parts WHERE i = 0)
    UNION ALL
    SELECT
        CASE
            WHEN nn.rest = '' AND nn.l = 0 THEN nn.i + 1
            ELSE nn.i
        END,
        CASE
            WHEN nn.rest = '' THEN (NOT nn.l)
            ELSE nn.l
        END,
        CASE
            WHEN nn.rest = '' AND nn.l = 1 THEN
                (SELECT SUBSTR(r, 1, 1) FROM parts WHERE i = nn.i)
            WHEN nn.rest = '' AND nn.l = 0 THEN
                (SELECT SUBSTR(l, 1, 1) FROM parts WHERE i = nn.i + 1)
            ELSE SUBSTR(rest, 1, 1)
        END,
        CASE
            WHEN nn.rest = '' AND nn.l = 1 THEN
                (SELECT SUBSTR(r, 2) FROM parts WHERE i = nn.i)
            WHEN nn.rest = '' AND nn.l = 0 THEN
                (SELECT SUBSTR(l, 2) FROM parts WHERE i = nn.i + 1)
            ELSE SUBSTR(rest, 2)
        END
    FROM nn
    WHERE nn.i <= (SELECT MAX(i) FROM parts)
)
INSERT INTO folded
SELECT i, l, c FROM nn WHERE nn.i <= (SELECT MAX(i) FROM parts);


SELECT SUM(
    CASE
        WHEN UNICODE(c) < 97 THEN 27 + UNICODE(c) - UNICODE('A')
        ELSE 1 + UNICODE(c) - UNICODE('a')
    END
)
FROM (
    SELECT folded.c
    FROM folded
    INNER JOIN folded folded2
    ON folded.i = folded2.i AND folded.l != folded2.l AND folded.c = folded2.c
    GROUP BY folded.i
);
