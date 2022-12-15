FROM python:3.9

RUN pip install chess psycopg2

WORKDIR /app
COPY local_ingestion.py local_ingestion.py
COPY lichess_db_standard_rated_2013-02.pgn pgn.pgn
 
ENTRYPOINT [ "python", "local_ingestion.py" ]