import chess.pgn
from db import DB
import sys
from pprint import pprint

# this script is the result of the fact that I left off a column in the INSERT statement in the local_ingestion script
# hopefully it will not be needed again

try:
    db = DB()
except:
    print('failed to connect to db')
    sys.exit()

# open pgn file and insert data to db
with open('../lichess_pgn/lichess_db_standard_rated_2014-10.pgn') as f:
    pgn = chess.pgn.read_game(f)
    while pgn:
        # insert mvoes to db
        db.cur.execute(" \
        UPDATE lichess_pgn_2014_10 \
        SET moves = %s \
        WHERE site = %s", (str(pgn.mainline_moves()), pgn.headers['Site']))
        
        db.conn.commit()
        
        # next game
        pgn = chess.pgn.read_game(f)