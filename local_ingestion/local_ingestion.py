import chess.pgn
from db import DB
import sys
from pprint import pprint

try:
    db = DB()
except:
    print('failed to connect to db')
    sys.exit()

# open pgn file and insert data to db
with open('../lichess_pgn/lichess_db_standard_rated_2014-10.pgn') as f:
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

        pprint(game_info)

        # insert to db
        db.cur.execute("INSERT INTO lichess_pgn_2014_10 \
        (event, site, date, round, white, black, result, white_elo, black_elo, white_rating_diff, black_rating_diff, eco, opening, termination, time_control, utc_date, utc_time, moves) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
        (game_info['Event'], game_info['Site'], game_info['Date'], game_info['Round'], 
        game_info['White'], game_info['Black'], game_info['Result'], game_info['WhiteElo'], game_info['BlackElo'], 
        game_info['WhiteRatingDiff'], game_info['BlackRatingDiff'], game_info['ECO'], game_info['Opening'], 
        game_info['Termination'], game_info['TimeControl'], game_info['UTCDate'], game_info['UTCTime'], game_info['Moves']))
        
        db.conn.commit()
        
        # next game
        pgn = chess.pgn.read_game(f)








