import chess.pgn
import sys
import argparse
import psycopg2

# parse pgn file and insert games to database
def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    file_path = params.file_path

    # connect to db
    try:
        conn = psycopg2.connect(
                    database=db,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
        cur = conn.cursor()
        print('success')
        sys.exit()  # remove me TODO
    except Exception as e:
        print('failed to connect to db:', e)
        sys.exit()

    # create table
    cur.execute(' \
    CREATE TABLE IF NOT EXISTS lichess_pgn_2013_02 \
    (id SERIAL PRIMARY KEY, event VARCHAR(255), site VARCHAR(255), date VARCHAR(255), round VARCHAR(255),  \
    white VARCHAR(255), black VARCHAR(255), result VARCHAR(255), white_elo VARCHAR(255), black_elo VARCHAR(255),   \
    white_rating_diff VARCHAR(255), black_rating_diff VARCHAR(255), eco VARCHAR(255),  \
    opening VARCHAR(255) , termination VARCHAR(255), time_control VARCHAR(255), utc_date VARCHAR(255), utc_time VARCHAR(255), moves VARCHAR(10485760))  \
    ')

    # open pgn file and insert data to db
    with open(file_path) as f:
        pgn = chess.pgn.read_game(f)
        while pgn:
            # parse game info
            game_info = {
            'Event': None,
            'Site': None,
            'Date': None,
            'Round': None,
            'White': None,
            'Black': None,
            'Result': None,
            'BlackElo': None,
            'BlackRatingDiff': None,
            'ECO': None,
            'Opening': None,
            'Termination': None,
            'TimeControl': None,
            'UTCDate': None,
            'WhiteRatingDiff': None,
            'UTCTime': None,
            'WhiteElo': None
            }

            for header in pgn.headers:
                game_info[header] = pgn.headers[header]
            game_info['Moves'] = str(pgn.mainline_moves())



            # insert to db
            cur.execute("INSERT INTO lichess_pgn_2013_02 \
            (event, site, date, round, white, black, result, white_elo, black_elo, white_rating_diff, black_rating_diff, eco, opening, termination, time_control, utc_date, utc_time, moves) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (game_info['Event'], game_info['Site'], game_info['Date'], game_info['Round'], 
            game_info['White'], game_info['Black'], game_info['Result'], game_info['WhiteElo'], game_info['BlackElo'], 
            game_info['WhiteRatingDiff'], game_info['BlackRatingDiff'], game_info['ECO'], game_info['Opening'], 
            game_info['Termination'], game_info['TimeControl'], game_info['UTCDate'], game_info['UTCTime'], game_info['Moves']))
            
            conn.commit()
            
            # next game
            pgn = chess.pgn.read_game(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest pgn data to local postgres db')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    # parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    # '../lichess_pgn/lichess_db_standard_rated_2014-10.pgn'
    parser.add_argument('--file_path', required=True, help='path of the pgn file')

    args = parser.parse_args()

    main(args)








