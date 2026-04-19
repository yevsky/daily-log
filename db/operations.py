from datetime import datetime
import sqlite3
from typing import TypedDict

from db.connection import get_connection

class EntryOut(TypedDict):
    id: int
    content: str
    tag: str
    created_at: datetime

def row_to_entry(row: sqlite3.Row) -> EntryOut:
    return {
        "id": row["id"],
        "content": row["content"],
        "tag": row["tag"],
        "created_at": row["created_at"]
    }

def insert_entry(content: str, tag: str | None = None) -> EntryOut:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            INSERT INTO entries (content, tag)
            VALUES (?, ?)
            RETURNING id, content, tag, created_at
            ''',
            (content, tag)
        )
        
        row = cursor.fetchone()
        
        if row is None:
            raise RuntimeError("Insert failed: no row returned")

        conn.commit()

        return row_to_entry(row)

    
def get_all_entries() -> list[EntryOut]:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT id, content, tag, created_at
            FROM entries
            ORDER BY created_at DESC
            '''
        )
        
        rows = cursor.fetchall()
        
        return [row_to_entry(row) for row in rows]
