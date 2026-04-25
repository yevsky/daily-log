from sqlalchemy.orm import Session
from db.models import Entry


def insert_entry(db: Session, content: str, tag: str | None = None) -> Entry:
    entry = Entry(content=content, tag=tag)

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def get_all_entries(db: Session) -> list[Entry]:
    return (
        db.query(Entry)
        .order_by(Entry.created_at.desc())
        .all()
    )


def update_entry(db: Session, entry_id: int, content: str, tag: str | None = None) -> Entry | None:
    entry = db.query(Entry).filter(Entry.id == entry_id).first()

    if not entry:
        return None

    entry.content = content
    entry.tag = tag

    db.commit()
    db.refresh(entry)

    return entry


def delete_entry_db(db: Session, entry_id: int) -> bool:
    entry = db.query(Entry).filter(Entry.id == entry_id).first()

    if not entry:
        return False

    db.delete(entry)
    db.commit()

    return True