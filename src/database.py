from datetime import datetime, timezone
import sqlite3

def init_db():
    conn = sqlite3.connect("tiny_url.db")
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
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO urls (code, long_url, created_at, click_count)
        VALUES (?, ?, ?, ?)
        """,
        (code, url, datetime.now(timezone.utc).isoformat(), 0)
    )
    conn.commit()
    conn.close()

def get_url(code):
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"long_url": result[0], "created_at": get_created_at(code)["created_at"], "click_count": get_click_count(code)["click_count"]}
    else:
        return None

def exists(code):
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def increment_click_count(code):
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET click_count = click_count + 1 WHERE code = ?", (code,))
    conn.commit()
    conn.close()

def get_click_count(code):
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("SELECT click_count FROM urls WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"click_count": result[0]}
    else:
        return None
    
def get_created_at(code):
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("SELECT created_at FROM urls WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"created_at": result[0]}
    else:
        return None

def delete_all_codes():
    conn = sqlite3.connect("tiny_url.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls")
    conn.commit()
    conn.close()

init_db()  # Initialize the database when the module is imported