from datetime import datetime
import sqlite3
from typing import TypedDict

from db.connection import get_connection


class EntryOut(TypedDict):
    id: int
    content: str
    tag: str | None
    created_at: datetime


def row_to_entry(row: sqlite3.Row) -> EntryOut:
    return {
        "id": row["id"],
        "content": row["content"],
        "tag": row["tag"],
        "created_at": row["created_at"],
    }


def insert_entry(content: str, tag: str | None = None) -> EntryOut:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO entries (content, tag)
            VALUES (?, ?)
            """,
            (content, tag),
        )

        entry_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT id, content, tag, created_at
            FROM entries
            WHERE id = ?
            """,
            (entry_id,),
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Insert failed")

        conn.commit()
        return row_to_entry(row)


def get_all_entries() -> list[EntryOut]:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, content, tag, created_at
            FROM entries
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()
        return [row_to_entry(row) for row in rows]


def delete_entry_db(entry_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM entries
            WHERE id = ?
            """,
            (entry_id,),
        )

        conn.commit()

        return cursor.rowcount > 0


def update_entry(entry_id: int, content: str, tag: str | None = None) -> EntryOut | None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE entries
            SET content = ?, tag = ?
            WHERE id = ?
            """,
            (content, tag, entry_id),
        )

        if cursor.rowcount == 0:
            return None

        cursor.execute(
            """
            SELECT id, content, tag, created_at
            FROM entries
            WHERE id = ?
            """,
            (entry_id,),
        )

        row = cursor.fetchone()
        conn.commit()

        return row_to_entry(row) if row else None