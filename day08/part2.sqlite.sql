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

SELECT
    MAX (
        (
            WITH RECURSIVE nn (y) AS (
                SELECT coords.y
                UNION ALL
                SELECT nn.y - 1
                FROM nn
                WHERE
                    nn.y > 0 AND (
                        nn.y = coords.y OR
                        (
                            SELECT c2.val
                            FROM coords c2
                            WHERE c2.y = nn.y AND c2.x = coords.x
                        ) < coords.val
                    )
            )
            SELECT COUNT(1) - 1 FROM nn
        ) * (
            WITH RECURSIVE nn (y) AS (
                SELECT coords.y
                UNION ALL
                SELECT nn.y + 1
                FROM nn
                WHERE
                    nn.y < (SELECT MAX(y) FROM coords) AND (
                        nn.y = coords.y OR
                        (
                            SELECT c2.val
                            FROM coords c2
                            WHERE c2.y = nn.y AND c2.x = coords.x
                        ) < coords.val
                    )
            )
            SELECT COUNT(1) - 1 FROM nn
        ) * (
            WITH RECURSIVE nn (x) AS (
                SELECT coords.x
                UNION ALL
                SELECT nn.x - 1
                FROM nn
                WHERE
                    nn.x > 0 AND (
                        nn.x = coords.x OR
                        (
                            SELECT c2.val
                            FROM coords c2
                            WHERE c2.x = nn.x AND c2.y = coords.y
                        ) < coords.val
                    )
            )
            SELECT COUNT(1) - 1 FROM nn
        ) * (
            WITH RECURSIVE nn (x) AS (
                SELECT coords.x
                UNION ALL
                SELECT nn.x + 1
                FROM nn
                WHERE
                    nn.x < (SELECT MAX(x) FROM coords) AND (
                        nn.x = coords.x OR
                        (
                            SELECT c2.val
                            FROM coords c2
                            WHERE c2.x = nn.x AND c2.y = coords.y
                        ) < coords.val
                    )
            )
            SELECT COUNT(1) - 1 FROM nn
        )
    )
FROM coords;
