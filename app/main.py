from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/check")
def root() -> dict[str, str]:
    return {"message": "API is running"}


@app.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntryCreate) -> EntryResponse:
    row = insert_entry(entry.content, entry.tag)
    return EntryResponse(**row)


@app.get("/entries", response_model=list[EntryResponse])
def get_entries() -> list[EntryResponse]:
    results = get_all_entries()
    return [EntryResponse(**row) for row in results]


@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int) -> dict[str, str]:
    deleted = delete_entry_db(entry_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {"message": f"Entry with id {entry_id} deleted"}


@app.put("/entries/{entry_id}", response_model=EntryResponse)
def put_entry(entry_id: int, entry: EntryCreate) -> EntryResponse:
    row = update_entry(entry_id, entry.content, entry.tag)

    if row is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    return EntryResponse(**row)
