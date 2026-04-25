from collections.abc import Generator
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import SessionLocal

from db.initialization import init_db
from db.operations import (
    insert_entry,
    get_all_entries,
    update_entry,
    delete_entry_db
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class EntryCreate(BaseModel):
    content: str
    tag: str | None = None


class EntryResponse(BaseModel):
    id: int
    content: str
    tag: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/check")
def root() -> dict[str, str]:
    return {"message": "API is running"}


@app.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)) -> EntryResponse:
    row = insert_entry(db, entry.content, entry.tag)
    return EntryResponse.model_validate(row)


@app.get("/entries", response_model=list[EntryResponse])
def get_entries(db: Session = Depends(get_db)) -> list[EntryResponse]:
    results = get_all_entries(db)
    return [EntryResponse.model_validate(row) for row in results]


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    deleted = delete_entry_db(db, entry_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {"message": f"Entry with id {entry_id} deleted"}


@app.put("/entries/{entry_id}", response_model=EntryResponse)
def put_entry(entry_id: int, entry: EntryCreate, db: Session = Depends(get_db)) -> EntryResponse:
    row = update_entry(db, entry_id, entry.content, entry.tag)

    if row is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    return EntryResponse.model_validate(row)