FROM python:3.10

RUN pip install psycopg2

COPY cli.py cli.py
COPY db.py db.py
 
ENTRYPOINT [ "python", "cli.py" ]