-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE lines (s);
WITH RECURSIVE
    nn (s, rest)
AS (
    SELECT NULL, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, char(10)) - 1),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO lines
SELECT s FROM nn WHERE s IS NOT NULL;

CREATE TABLE items_lines (i INT, s VARCHAR);
INSERT INTO items_lines
SELECT (ROWID - 2) / 7, SUBSTR(s, INSTR(s, ': ') + 2) || ', '
FROM lines WHERE s LIKE '%Starting items%';

CREATE TABLE items (monk INT, val INT);
WITH RECURSIVE
    nn (i, n, s)
AS (
    SELECT 0, NULL, (SELECT s FROM items_lines WHERE i = 0)
    UNION ALL
    SELECT
        CASE WHEN nn.s == '' THEN nn.i + 1 ELSE nn.i END,
        CASE
            WHEN nn.s == '' THEN NULL
            ELSE SUBSTR(nn.s, 1, INSTR(nn.s, ', ') - 1)
        END,
        CASE
            WHEN nn.s == '' THEN (SELECT s FROM items_lines WHERE i = nn.i + 1)
            ELSE SUBSTR(nn.s, INSTR(nn.s, ', ') + 2)
        END
    FROM nn
    WHERE nn.i <= (SELECT MAX(i) FROM items_lines)
)
INSERT INTO items
SELECT i, n FROM nn WHERE nn.n IS NOT NULL;

CREATE TABLE monk (id INT, op VARCHAR, op_n INT NULL, mod INT, true_monk INT, false_monk INT);

INSERT INTO monk
SELECT
    (lines.ROWID - 3) / 7,
    CASE
        WHEN lines.s LIKE '%new = old * old%' THEN 'square'
        WHEN lines.s LIKE '%new = old +%' THEN 'add'
        WHEN lines.s LIKE '%new = old *%' THEN 'mult'
        ELSE NULL
    END,
    CASE
        WHEN lines.s LIKE '%new = old * old%' THEN NULL
        ELSE SUBSTR(lines.s, 26)
    END,
    SUBSTR(lines2.s, 22),
    SUBSTR(lines3.s, 30),
    SUBSTR(lines4.s, 31)
FROM lines
INNER JOIN lines lines2 ON lines2.ROWID = lines.ROWID + 1
INNER JOIN lines lines3 ON lines3.ROWID = lines.ROWID + 2
INNER JOIN lines lines4 ON lines4.ROWID = lines.ROWID + 3
WHERE lines.s LIKE '%Operation: %';

CREATE TABLE seen(monk INT, n INT);
INSERT INTO seen SELECT monk.id, 0 FROM monk;

CREATE TABLE work (monk INT);
CREATE TRIGGER t_work AFTER INSERT ON work FOR EACH ROW BEGIN
    UPDATE seen
    SET n = n + (SELECT COUNT(1) FROM items WHERE items.monk = NEW.monk)
    WHERE monk = NEW.monk;

    UPDATE items
    SET val = (
        CASE (SELECT monk.op FROM monk WHERE monk.id = NEW.monk)
            WHEN 'square' THEN val * val
            WHEN 'add' THEN val + (SELECT monk.op_n FROM monk WHERE monk.id = NEW.monk)
            WHEN 'mult' THEN val * (SELECT monk.op_n FROM monk WHERE monk.id = NEW.monk)
            ELSE '?????'
        END
    )
    WHERE monk = NEW.monk;

    UPDATE items
    SET val = val / 3
    WHERE monk = NEW.monk;

    UPDATE items
    SET monk = (
        CASE
            WHEN val % (SELECT monk.mod FROM monk WHERE monk.id = NEW.monk) = 0 THEN
                (SELECT monk.true_monk FROM monk WHERE monk.id = NEW.monk)
            ELSE
                (SELECT monk.false_monk FROM monk WHERE monk.id = NEW.monk)
        END
    )
    WHERE monk = NEW.monk;
END;

WITH RECURSIVE
    nn (i, monk)
AS (
    SELECT 0, 0
    UNION ALL
    SELECT
        CASE
            WHEN nn.monk = (SELECT MAX(id) FROM monk) THEN nn.i + 1
            ELSE nn.i
        END,
        CASE
            WHEN nn.monk = (SELECT MAX(id) FROM monk) THEN 0
            ELSE nn.monk + 1
        END
    FROM nn
    WHERE i < 20
)
INSERT INTO work
SELECT monk FROM nn WHERE i < 20;

SELECT
    (SELECT n FROM seen ORDER BY n DESC LIMIT 1 OFFSET 0) *
    (SELECT n FROM seen ORDER BY n DESC LIMIT 1 OFFSET 1);
