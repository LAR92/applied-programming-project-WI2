from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def root ():
    return{"message": "Hello, World!"}

@app.get("/name/{name}")
def greet_name(name:str):
    return {"message":f"Hello,{name}!"}

@app.get("/zahl/{zahl}")
def greet_name(zahl: int):
    return {"message":f"Zahl +1,{zahl + 1}!"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

app = FastAPI(
    title="Applied Programming Course HS Coburg",
    description="Simple note management API",
    version="1.0.0"
)

###############################
#### Note API Endpoints (Tag 2)
###############################

class NoteCreate(BaseModel):
    title: str
    content: str

 class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: str  

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)