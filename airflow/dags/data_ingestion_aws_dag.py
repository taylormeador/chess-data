import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


PGN_DATE = '2013-01'
PGN_ZST_FILE = "lichess_db_standard_rated_" + PGN_DATE + ".pgn.zst"
PGN_URL = 'https://database.lichess.org/standard/' + PGN_ZST_FILE
DOWNLOAD_OUTPUT_FILE = AIRFLOW_HOME + '/lichess_db_standard_rated_' + PGN_DATE + '.pgn.zst'
UNZIPPED_OUTPUT_FILE = DOWNLOAD_OUTPUT_FILE.replace('.zst', '')
TABLE_NAME = 'lichess_pgn_' + PGN_DATE.replace('-', '_') # want to match local config

def unzip_pgn():
    import zstandard
    import pathlib

    destination_dir = UNZIPPED_OUTPUT_FILE
    input_file = DOWNLOAD_OUTPUT_FILE
    with open(input_file, 'rb') as compressed:
        decomp = zstandard.ZstdDecompressor()
        output_path = pathlib.Path(destination_dir)
        with open(output_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)


def ingest_pgn():
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    import chess.pgn
    from psycopg2 import sql


    hook = PostgresHook(postgres_conn_id="aws-postgres-chess-data")
    conn = hook.get_conn()
    cur = conn.cursor()

    # create table
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} \
    (id SERIAL PRIMARY KEY, event VARCHAR(255), site VARCHAR(255), date VARCHAR(255), round VARCHAR(255),  \
    white VARCHAR(255), black VARCHAR(255), result VARCHAR(255), white_elo VARCHAR(255), black_elo VARCHAR(255),   \
    white_rating_diff VARCHAR(255), black_rating_diff VARCHAR(255), eco VARCHAR(255),  \
    opening VARCHAR(255) , termination VARCHAR(255), time_control VARCHAR(255), utc_date VARCHAR(255), utc_time VARCHAR(255), moves VARCHAR(10485760))  \
    ").format(table=sql.Identifier(TABLE_NAME))

    cur.execute(query)
    conn.commit()

    # open pgn file and insert data to db
    with open(UNZIPPED_OUTPUT_FILE) as f:
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
            query = sql.SQL("INSERT INTO {table} \
            (event, site, date, round, white, black, result, white_elo, black_elo, white_rating_diff, \
            black_rating_diff, eco, opening, termination, time_control, utc_date, utc_time, moves) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)").format(table=sql.Identifier(TABLE_NAME))
            
            args = (
                game_info['Event'], 
                game_info['Site'],
                game_info['Date'],
                game_info['Round'], 
                game_info['White'],
                game_info['Black'],
                game_info['Result'],
                game_info['WhiteElo'],
                game_info['BlackElo'],
                game_info['WhiteRatingDiff'],
                game_info['BlackRatingDiff'],
                game_info['ECO'],
                game_info['Opening'], 
                game_info['Termination'],
                game_info['TimeControl'],
                game_info['UTCDate'],
                game_info['UTCTime'],
                game_info['Moves']
            )
            
            cur.execute(query, args)
            
            # next game
            pgn = chess.pgn.read_game(f)
    
    # commit iff no exceptions
    conn.commit()

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


with DAG(
    dag_id="data_ingestion_aws_dag",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
) as dag:

    download_pgn_task = BashOperator(
        task_id="download_pgn_task",
        bash_command=f"curl -sSL {PGN_URL} > {DOWNLOAD_OUTPUT_FILE}"
    )

    unzip_pgn_task = PythonOperator(
        task_id="unzip_pgn_task",
        python_callable=unzip_pgn
    )

    ingest_pgn_task = PythonOperator(
        task_id="ingest_pgn_task",
        python_callable=ingest_pgn
    )


    download_pgn_task >> unzip_pgn_task >> ingest_pgn_task