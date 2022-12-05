-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE input2 (map STRING, instr STRING);
INSERT INTO input2
SELECT
    SUBSTR(s, 1, INSTR(s, char(10) || char(10))),
    SUBSTR(s, INSTR(s, char(10) || char(10)) + 2) || char(10)
FROM input;

CREATE TABLE stacks (col INT, idx INT NULL, c VARCHAR);
CREATE TRIGGER t_stacks AFTER INSERT ON stacks FOR EACH ROW BEGIN
    UPDATE stacks
    SET idx = (SELECT COUNT(1) FROM stacks WHERE col = NEW.col) - 1
    WHERE col = NEW.col AND idx IS NULL;
END;

WITH RECURSIVE
    nn (rid, just_finished_line, idx, c, rest)
AS (
    SELECT 0, 1, -1, ' ', (SELECT map FROM input2)
    UNION ALL
    SELECT
        nn.rid + 1,
        CASE WHEN INSTR(nn.rest, char(10)) < 5 THEN 1 ELSE 0 END,
        CASE WHEN nn.just_finished_line THEN 1 ELSE nn.idx + 1 END,
        SUBSTR(nn.rest, 2, 1),
        CASE
            WHEN INSTR(nn.rest, char(10)) < 5 THEN
                SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            ELSE
                SUBSTR(nn.rest, 5)
        END
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO stacks
SELECT idx, NULL, c FROM nn WHERE c != ' ' ORDER BY nn.rid DESC;

INSERT INTO stacks VALUES (99999, NULL, '');

CREATE TABLE raw_instructions (rid INT, n INT, src INT, dest INT);
WITH RECURSIVE
    nn (rid, n, src, dest, rest)
AS (
    SELECT -2, -1, -1, -1, (SELECT instr FROM input2)
    UNION ALL
    SELECT
        nn.rid + 2,
        SUBSTR(nn.rest, 6, INSTR(nn.rest, " from ") - 6),
        SUBSTR(
            nn.rest,
            INSTR(nn.rest, " from ") + 6,
            INSTR(nn.rest, " to ") - (INSTR(nn.rest, " from ") + 6)
        ),
        SUBSTR(
            nn.rest,
            INSTR(nn.rest, " to ") + 4,
            INSTR(nn.rest, char(10)) - (INSTR(nn.rest, " to ") + 4)
        ),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO raw_instructions
SELECT
    CASE z WHEN 0 THEN nn.rid ELSE nn.rid + 1 END,
    nn.n,
    CASE z WHEN 0 THEN nn.src ELSE 99999 END,
    CASE z WHEN 0 THEN 99999 ELSE nn.dest END
    FROM nn
INNER JOIN (SELECT 0 AS z UNION ALL SELECT 1 AS z)
WHERE n > 0
ORDER BY rid;

CREATE TABLE instructions (src INT, dest INT);
CREATE TRIGGER t_instructions AFTER INSERT ON instructions FOR EACH ROW BEGIN
    UPDATE stacks
    SET
        col = NEW.dest,
        idx = (SELECT MAX(idx) + 1 FROM stacks WHERE col = NEW.dest)
    WHERE
        col = NEW.src AND
        idx = (SELECT MAX(idx) FROM stacks WHERE col = NEW.src);
END;

WITH RECURSIVE
    nn (rid, n, src, dest)
AS (
    SELECT rid, n, src, dest FROM raw_instructions WHERE rid = 0
    UNION ALL
    SELECT
        CASE WHEN nn.n = 1 THEN nn.rid + 1 ELSE nn.rid END,
        CASE
            WHEN nn.n = 1 THEN
                (
                    SELECT raw_instructions.n
                    FROM raw_instructions
                    WHERE rid = nn.rid + 1
                )
            ELSE
                nn.n - 1
        END,
        CASE
            WHEN nn.n = 1 THEN
                (
                    SELECT raw_instructions.src
                    FROM raw_instructions
                    WHERE rid = nn.rid + 1
                )
            ELSE
                nn.src
        END,
        CASE
            WHEN nn.n = 1 THEN
                (
                    SELECT raw_instructions.dest
                    FROM raw_instructions
                    WHERE rid = nn.rid + 1
                )
            ELSE
                nn.dest
        END
    FROM nn
    WHERE nn.rid < (SELECT MAX(rid) FROM raw_instructions)
)
INSERT INTO instructions
SELECT src, dest FROM nn;

CREATE TABLE answer(c);
INSERT INTO answer
SELECT c FROM stacks
WHERE idx = (SELECT MAX(idx) FROM stacks s2 WHERE s2.col = stacks.col)
ORDER BY col ASC;

WITH RECURSIVE
    nn (n, s)
AS (
    SELECT 0, ''
    UNION ALL
    SELECT nn.n + 1, nn.s || (SELECT c FROM answer WHERE ROWID = nn.n + 1)
    FROM nn
    WHERE nn.n < (SELECT MAX(ROWID) FROM answer)
)
SELECT nn.s FROM nn ORDER BY nn.n DESC LIMIT 1;
