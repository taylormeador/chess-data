FROM python:3.9

RUN pip install chess psycopg2

WORKDIR /app
COPY local_ingestion.py local_ingestion.py
COPY lihcess_pgn/lichess_db_standard_rated_2013-01.pgn pgn.pgn
 
ENTRYPOINT [ "python", "local_ingestion.py" ]