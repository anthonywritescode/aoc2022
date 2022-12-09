-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

-- oh no
PRAGMA recursive_triggers = ON;

CREATE TABLE points (i INT, x INT, y INT);
INSERT INTO points VALUES
    (0, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3, 0, 0),
    (4, 0, 0),
    (5, 0, 0),
    (6, 0, 0),
    (7, 0, 0),
    (8, 0, 0),
    (9, 0, 0);

CREATE TABLE visited(i INT, x INT, y INT, PRIMARY KEY (i, x, y));
INSERT INTO visited SELECT * FROM points;

CREATE TRIGGER t_points AFTER UPDATE ON points FOR EACH ROW BEGIN
    INSERT OR REPLACE INTO visited VALUES (NEW.i, NEW.x, NEW.y) ON CONFLICT DO NOTHING;

    UPDATE points
        SET
            x = (
                CASE
                    WHEN ABS(NEW.x - (SELECT points.x FROM points WHERE points.i = NEW.i + 1)) = 2 THEN
                        (NEW.x + (SELECT points.x FROM points WHERE points.i = NEW.i + 1)) / 2
                    WHEN ABS(NEW.y - (SELECT points.y FROM points WHERE points.i = NEW.i + 1)) = 2 THEN
                        NEW.x
                    ELSE
                        x
                END
            ),
            y = (
                CASE
                    WHEN ABS(NEW.y - (SELECT points.y FROM points WHERE points.i = NEW.i + 1)) = 2 THEN
                        (NEW.y + (SELECT points.y FROM points WHERE points.i = NEW.i + 1)) / 2
                    WHEN ABS(NEW.x - (SELECT points.x FROM points WHERE points.i = NEW.i + 1)) = 2 THEN
                        NEW.y
                    ELSE
                        y
                END
            )
        WHERE
            points.i = NEW.i + 1 AND (
                ABS(NEW.x - (SELECT points.x FROM points WHERE points.i = NEW.i + 1)) = 2 OR
                ABS(NEW.y - (SELECT points.y FROM points WHERE points.i = NEW.i + 1)) = 2
            );
END;

CREATE TABLE updates (dx INT, dy INT);
CREATE TRIGGER t_updates AFTER INSERT ON updates BEGIN
    UPDATE points SET x = x + NEW.dx, y = y + new.dy WHERE i = 0;
END;

WITH RECURSIVE
    nn (n, dx, dy, rest)
AS (
    SELECT 0, 0, 0, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        CASE
            WHEN nn.n = 0 THEN
                SUBSTR(nn.rest, 3, INSTR(nn.rest, char(10)) - 3)
            ELSE
                nn.n - 1
        END,
        CASE
            WHEN nn.n = 0 THEN
                CASE SUBSTR(nn.rest, 1, 1)
                    WHEN 'L' THEN -1
                    WHEN 'R' THEN 1
                    ELSE 0
                END
            ELSE nn.dx
        END,
        CASE
            WHEN nn.n = 0 THEN
                CASE SUBSTR(nn.rest, 1, 1)
                    WHEN 'U' THEN -1
                    WHEN 'D' THEN 1
                    ELSE 0
                END
            ELSE nn.dy
        END,
        CASE
            WHEN nn.n = 0 THEN
                SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            ELSE
                nn.rest
        END
    FROM nn WHERE nn.n > 0 OR nn.rest != ''
)
INSERT INTO updates
SELECT dx, dy FROM nn WHERE nn.n != 0;

SELECT COUNT(1) FROM visited WHERE i = 1;
