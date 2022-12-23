SELECT result, COUNT(result), to_char(COUNT(result)::NUMERIC/(SELECT COUNT(*) FROM lichess_pgn_2013_01) * 100,'990D99%') AS outcome_percent
FROM lichess_pgn_2013_01
GROUP BY result
ORDER BY COUNT(result) DESC
LIMIT 100

WITH openings_count AS (
    SELECT opening, COUNT(opening) AS opening_count
    FROM lichess_pgn_2013_01
    GROUP BY opening
)
SELECT pgn.opening,
    CASE pgn.result
        WHEN '1-0' THEN 1
        WHEN '0-1' THEN -1
        ELSE 0
    END as outcome,
    COUNT(pgn.result) AS result_count,
    openings_count.opening_count,
    to_char(COUNT(pgn.result)::NUMERIC / openings_count.opening_count::NUMERIC * 100,'990D99%') AS ratio 
FROM lichess_pgn_2013_01 as pgn
JOIN openings_count
ON pgn.opening = openings_count.opening
GROUP BY pgn.opening, pgn.result, openings_count.opening_count
HAVING COUNT(pgn.opening) > 99
ORDER BY COUNT(pgn.opening) DESC