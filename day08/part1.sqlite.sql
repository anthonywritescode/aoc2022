-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE coords (y INT, x INT, val INT);
WITH RECURSIVE
    nn (y, x, v, rest)
AS (
    SELECT
        0,
        0,
        (SELECT SUBSTR(s, 1, 1) FROM input),
        (SELECT SUBSTR(s, 2) || char(10) FROM input)
    UNION ALL
    SELECT
        CASE SUBSTR(nn.rest, 1, 1)
            WHEN char(10) THEN nn.y + 1
            ELSE nn.y
        END,
        CASE SUBSTR(nn.rest, 1, 1)
            WHEN char(10) THEN -1
            ELSE nn.x + 1
        END,
        CASE SUBSTR(nn.rest, 1, 1)
            WHEN char(10) THEN -1
            ELSE SUBSTR(nn.rest, 1, 1)
        END,
        SUBSTR(nn.rest, 2)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO coords
SELECT nn.y, nn.x, nn.v FROM nn WHERE nn.x != -1;

SELECT COUNT(1) FROM (
    SELECT y, x FROM (
        SELECT coords.y, c2.x
        FROM (SELECT DISTINCT y FROM coords) coords
        INNER JOIN coords c2 ON
            c2.y = coords.y AND (
                c2.x = 0  OR
                c2.val > (
                    SELECT MAX(c3.val)
                    FROM coords c3
                    WHERE c3.y = coords.y AND c3.x < c2.x
                )
            )

        UNION ALL

        SELECT coords.y, c2.x
        FROM (SELECT DISTINCT y FROM coords) coords
        INNER JOIN coords c2 ON
            c2.y = coords.y AND (
                c2.x = (SELECT MAX(x) FROM coords)  OR
                c2.val > (
                    SELECT MAX(c3.val)
                    FROM coords c3
                    WHERE c3.y = coords.y AND c3.x > c2.x
                )
            )

        UNION ALL

        SELECT c2.y, coords.x
        FROM (SELECT DISTINCT x FROM coords) coords
        INNER JOIN coords c2 ON
            c2.x = coords.x AND (
                c2.y = 0  OR
                c2.val > (
                    SELECT MAX(c3.val)
                    FROM coords c3
                    WHERE c3.x = coords.x AND c3.y < c2.y
                )
            )

        UNION ALL

        SELECT c2.y, coords.x
        FROM (SELECT DISTINCT x FROM coords) coords
        INNER JOIN coords c2 ON
            c2.x = coords.x AND (
                c2.y = (SELECT MAX(y) FROM coords)  OR
                c2.val > (
                    SELECT MAX(c3.val)
                    FROM coords c3
                    WHERE c3.x = coords.x AND c3.y > c2.y
                )
            )
    )
    GROUP BY y, x
);
