from datetime import datetime, timezone
from psycopg.rows import dict_row
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            created_at TEXT NOT NULL,
            click_count INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save(code, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO urls (code, long_url, created_at, click_count)
        VALUES (%s, %s, %s, %s)
        """,
        (code, url, datetime.now(timezone.utc).isoformat(), 0)
    )
    conn.commit()
    conn.close()

def get_url(code):
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)
    cursor.execute("SELECT long_url, created_at, click_count FROM urls WHERE code = %s", (code,))
    result = cursor.fetchone()
    conn.close()
    return result 

def exists(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE code = %s", (code,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def increment_click_count(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET click_count = click_count + 1 WHERE code = %s", (code,))
    conn.commit()
    conn.close()

def get_click_count(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT click_count FROM urls WHERE code = %s", (code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

init_db()  # Initialize the database when the module is imported