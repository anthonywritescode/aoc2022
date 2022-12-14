-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input2.txt'), char(10)));

CREATE TABLE coords (y INT, x INT, c VARCHAR, beginning BIT, ending BIT);
WITH RECURSIVE
    nn (y, x, c, rest)
AS (
    SELECT 0, -1, NULL, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        CASE WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN nn.y + 1 ELSE nn.y END,
        CASE WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN -1 ELSE nn.x + 1 END,
        CASE WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN NULL ELSE SUBSTR(nn.rest, 1, 1) END,
        SUBSTR(nn.rest, 2)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO coords
SELECT y, x, c, 0, 0 FROM nn WHERE c IS NOT NULL;

UPDATE coords SET c = 'a', beginning = 1 WHERE c = 'S';
UPDATE coords SET c = 'z', ending = 1 WHERE c = 'E';

CREATE TABLE deltas (dy INT, dx INT);
INSERT INTO deltas VALUES (1, 0), (-1, 0), (0, 1), (0, -1);

WITH RECURSIVE
    nn (it, todo, seen, answer)
AS (
    SELECT
        0,
        json_array(json_array(y, x, 0)),
        -- placeholder value so it doesn't get converted to scalar
        json_array(json_array(-1, -1)),
        0
        FROM coords WHERE beginning = 1
    UNION
    SELECT
        nn.it + 1,
        (
            SELECT json_group_array(value)
            FROM (
                -- remove lowest
                SELECT j.value FROM json_each(nn.todo) j
                WHERE j.key != (
                    SELECT o.key FROM (
                        SELECT j2.key, json_extract(j2.value, '$[2]')
                        FROM json_each(nn.todo) j2
                        ORDER BY json_extract(j2.value, '$[2]') ASC
                        LIMIT 1
                    ) o
                )
                UNION
                -- extend rest
                SELECT json_array(
                    json_extract(j.value, '$[0]') + deltas.dy,
                    json_extract(j.value, '$[1]') + deltas.dx,
                    json_extract(j.value, '$[2]') + 1
                )
                FROM json_each(nn.todo) j, deltas
                INNER JOIN coords cand ON
                    json_extract(j.value, '$[0]') + deltas.dy = cand.y AND
                    json_extract(j.value, '$[1]') + deltas.dx = cand.x
                INNER JOIN coords curr ON
                    json_extract(j.value, '$[0]') = curr.y AND
                    json_extract(j.value, '$[1]') = curr.x AND
                    (UNICODE(cand.c) - UNICODE(curr.c)) <= 1
                WHERE
                    j.key = (
                        SELECT o.key FROM (
                            SELECT j2.key, json_extract(j2.value, '$[2]')
                            FROM json_each(nn.todo) j2
                            ORDER BY json_extract(j2.value, '$[2]') ASC
                            LIMIT 1
                        ) o
                    )
                    AND
                    (
                        SELECT COUNT(1) FROM json_each(nn.seen) j
                        WHERE j.value = (
                            SELECT o.v FROM (
                                SELECT
                                    json_array(
                                        json_extract(j2.value, '$[0]'),
                                        json_extract(j2.value, '$[1]')
                                    ) AS v,
                                    json_extract(j2.value, '$[2]')
                                FROM json_each(nn.todo) j2
                                ORDER BY json_extract(j2.value, '$[2]') ASC
                                LIMIT 1
                            ) o
                        )
                    ) = 0
            )
        ),
        (
            SELECT json_group_array(value) FROM (
                SELECT j.value FROM json_each(nn.seen) j
                UNION
                SELECT o.v FROM (
                    SELECT
                        json_array(
                            json_extract(j2.value, '$[0]'),
                            json_extract(j2.value, '$[1]')
                        ) AS v,
                        json_extract(j2.value, '$[2]')
                    FROM json_each(nn.todo) j2
                    ORDER BY json_extract(j2.value, '$[2]') ASC
                    LIMIT 1
                ) o
            )
        ),
        (SELECT MIN(json_extract(j.value, '$[2]')) FROM json_each(nn.todo) j)
    FROM nn
    WHERE (
        SELECT COUNT(1) FROM json_each(nn.seen) j
        INNER JOIN coords ON
            json_extract(j.value, '$[0]') = coords.y AND
            json_extract(j.value, '$[1]') = coords.x AND
            coords.ending
    ) = 0
)
SELECT nn.answer FROM nn ORDER BY nn.it DESC LIMIT 1;
