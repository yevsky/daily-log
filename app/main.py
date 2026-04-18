from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from db.connect import get_connection, init_db

app = FastAPI()

init_db()

class Entry(BaseModel):
    content: str
    tag: str | None = None
    created_at: datetime = datetime.now()

entries: list[Entry] = []

@app.get("/check")
def root() -> dict[str, str]:
    return {"message": "API is running"}

@app.post("/entries")
def create_entry(entry: Entry) -> Entry:
    entries.append(entry)
    return entry

@app.get("/entries")
def get_entries() -> list[Entry]:
    return entries