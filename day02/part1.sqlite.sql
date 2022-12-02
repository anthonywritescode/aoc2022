-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE weights (choice, weight_val);
INSERT INTO weights VALUES ('A', 1), ('B', 2), ('C', 3);

CREATE TABLE vals (them, us);
WITH RECURSIVE
    nn (them, us, rest)
AS (
    SELECT NULL, NULL, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, 1),
        REPLACE(
            REPLACE(
                REPLACE(
                    SUBSTR(nn.rest, 3, 1),
                    'X', 'A'
                ),
                'Y', 'B'
            ),
            'Z', 'C'
        ),
        SUBSTR(nn.rest, 5)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO vals
SELECT them, us FROM nn WHERE them IS NOT NULL;

SELECT SUM(outcome + weight_val) FROM (
    SELECT
        CASE
            WHEN them = us THEN 3
            WHEN them = 'A' AND us = 'B' THEN 6
            WHEN them = 'B' AND us = 'C' THEN 6
            WHEN them = 'C' AND us = 'A' THEN 6
            ELSE 0
        END AS outcome,
        weight_val
    FROM vals
    INNER JOIN weights ON vals.us = weights.choice
);
