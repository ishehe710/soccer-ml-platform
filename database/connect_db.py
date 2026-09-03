import os
from dotenv import load_dotenv
import psycopg
from src.config.settings import settings


def get_connection():
    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )

conn = get_connection()
print("Connected to Postgres database!")
conn.close()