from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from db.initialization import init_db
from db.operations import insert_entry, get_all_entries
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # your frontend
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