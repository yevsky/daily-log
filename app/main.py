from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from db.initialization import init_db
from db.operations import insert_entry, get_all_entries

app = FastAPI()

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