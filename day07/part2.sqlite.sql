-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE fs (p VARCHAR, is_dir BIT, size INT);
INSERT INTO fs VALUES ('', 1, 0);

WITH RECURSIVE
    nn (pwd, in_ls, p, is_dir, size, rest)
AS (
    SELECT
        '/',
        0,
        '/',
        0,
        0,
        (SELECT SUBSTR(s, INSTR(s, char(10)) + 1) || char(10) FROM input)
    UNION ALL
    SELECT
        CASE
            WHEN SUBSTR(nn.rest, 1, INSTR(nn.rest, char(10)) - 1) = '$ cd ..' THEN
                CASE nn.pwd
                    WHEN '/' THEN '/'
                    ELSE RTRIM(SUBSTR(nn.pwd, INSTR(nn.pwd, '/') + 1), '/') || '/'
                END
            WHEN nn.rest LIKE '$ cd %' THEN
                SUBSTR(nn.rest, 6, INSTR(nn.rest, char(10)) - 6) || '/' ||
                LTRIM(nn.pwd, '/')
            ELSE
                nn.pwd
        END,
        CASE
            WHEN SUBSTR(nn.rest, 1, INSTR(nn.rest, char(10)) - 1) = '$ ls' THEN 1
            WHEN nn.in_ls AND nn.rest NOT LIKE '$ %' THEN 1
            ELSE 0
        END,
        CASE
            WHEN nn.in_ls AND nn.rest NOT LIKE '$ %' THEN
                SUBSTR(
                    nn.rest,
                    INSTR(nn.rest, ' ') + 1,
                    INSTR(nn.rest, char(10)) - INSTR(nn.rest, ' ') - 1
                )  || '/' ||
                LTRIM(nn.pwd, '/')
            ELSE ''
        END,
        nn.rest LIKE 'dir %',
        CASE
            WHEN nn.in_ls AND nn.rest NOT LIKE '$ %' AND nn.rest NOT LIKE 'dir %' THEN
                SUBSTR(nn.rest, 1, INSTR(nn.rest, ' ') - 1)
            ELSE 0
        END,
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO fs
SELECT nn.p, nn.is_dir, nn.size FROM nn WHERE nn.is_dir OR nn.size > 0;

SELECT sz FROM (
    SELECT SUM(fs2.size) AS sz
    FROM fs
    INNER JOIN fs fs2 ON NOT fs2.is_dir AND fs2.p LIKE '%/' || fs.p
    WHERE fs.is_dir
    GROUP BY fs.p
)
WHERE sz >= 30000000 - (70000000 - (SELECT SUM(fs.size) FROM fs))
ORDER BY sz ASC
LIMIT 1;
