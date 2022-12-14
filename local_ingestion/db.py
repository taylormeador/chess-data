import psycopg2

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
                    database="chess_data",
                    user="root",
                    password="root",
                    host="localhost",
                    port="5432"
                )
        self.cur = self.conn.cursor()
