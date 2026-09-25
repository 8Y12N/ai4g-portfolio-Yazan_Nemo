import sqlite3
from datetime import datetime

DB_PATH = "glossary.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS glossary (
            term TEXT PRIMARY KEY,
            definition TEXT NOT NULL,
            source_paper TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_terms(terms: list[dict], source_paper: str = "unknown"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    for item in terms:
        cursor.execute("""
            INSERT INTO glossary (term, definition, source_paper, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(term) DO UPDATE SET
                definition = excluded.definition,
                source_paper = excluded.source_paper,
                last_updated = excluded.last_updated
        """, (item["term"], item["definition"], source_paper, now))

    conn.commit()
    conn.close()


def get_all_terms() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM glossary ORDER BY last_updated DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
