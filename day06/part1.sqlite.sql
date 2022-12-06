-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE answers (n INT);
CREATE TABLE chars (c VARCHAR);
CREATE TRIGGER t_chars AFTER INSERT ON chars FOR EACH ROW BEGIN
    INSERT INTO answers
    SELECT (SELECT COUNT(1) FROM chars)
    WHERE (
        (
            SELECT COUNT(DISTINCT c) FROM (
                SELECT c FROM chars
                ORDER BY ROWID DESC
                LIMIT 4
            )
        ) = 4
    );
END;

WITH RECURSIVE
    nn (c, rest)
AS (
    SELECT '', (SELECT s FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, 1),
        SUBSTR(nn.rest, 2)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO chars
SELECT nn.c FROM nn WHERE c != '';

SELECT MIN(n) FROM answers;
