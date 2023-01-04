import psycopg2

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database='chess_data',
            user='chessdatacli',
            password='password',
            host='chess-db.cvlsbsapg8h4.us-east-2.rds.amazonaws.com',
            port=5432
        )
        self.cur = self.conn.cursor()

    def get_best_openings(self, username, color):
        result = '1-0' if color == 'white' else '0-1'
        # threshold = 5 if color == 'white' else 1
        self.cur.execute(""" \
        WITH openings_count AS ( \
        SELECT opening, COUNT(opening) AS opening_count \
        FROM games \
        WHERE %s = '%s' \
        GROUP BY opening \
            ) \
        SELECT pgn.opening, \
            openings_count.opening_count AS num_games, \
            COUNT(pgn.result) AS num_wins, \
            COUNT(pgn.result)::NUMERIC / openings_count.opening_count::NUMERIC * 100 AS ratio
        FROM games as pgn \
        JOIN openings_count \
        ON pgn.opening = openings_count.opening \
        WHERE %s = '%s' \
        GROUP BY pgn.opening, pgn.result, openings_count.opening_count \
        HAVING openings_count.opening_count >= %d AND pgn.result = '%s' AND COUNT(pgn.result)::NUMERIC / openings_count.opening_count::NUMERIC * 100 > 50 \
        ORDER BY ratio DESC""" % (color, username, color, username, 5, result))
        return self.cur.fetchall()


    def get_worst_openings(self, username, color):
        result = '0-1' if color == 'white' else '1-0'
        self.cur.execute(""" \
        WITH openings_count AS ( \
        SELECT opening, COUNT(opening) AS opening_count \
        FROM games \
        WHERE %s = '%s' \
        GROUP BY opening \
            ) \
        SELECT pgn.opening, \
            openings_count.opening_count AS num_games, \
            COUNT(pgn.result) AS num_losses, \
            COUNT(pgn.result)::NUMERIC / openings_count.opening_count::NUMERIC * 100 AS ratio
        FROM games as pgn \
        JOIN openings_count \
        ON pgn.opening = openings_count.opening \
        WHERE %s = '%s' \
        GROUP BY pgn.opening, pgn.result, openings_count.opening_count \
        HAVING openings_count.opening_count >= %d AND pgn.result = '%s' AND COUNT(pgn.result)::NUMERIC / openings_count.opening_count::NUMERIC * 100 > 50 \
        ORDER BY ratio DESC""" % (color, username, color, username, 5, result))
        return self.cur.fetchall()


