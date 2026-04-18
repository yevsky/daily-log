from datetime import datetime
from typing import TypedDict

from db.connection import get_connection

class EntryOut(TypedDict):
    id: int
    content: str
    tag: str | None = None
    created_at: datetime

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

        return {
            "id": row["id"],
            "content": row["content"],
            "tag": row["tag"],
            "created_at": row["created_at"]
        }

    
def get_all_entries():
    pass
