import psycopg2 # type: ignore
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
