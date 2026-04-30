from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path

app = FastAPI(
    title="Note Taking API",
    description="Simple note management",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/calculate/{number}")
def calculate(number: float):
    result = number * 2 + 5
    return {"message": f"Der verrechnete Wert von {number} ist {result}"}


####################################
### Note API Endpoints (tag 2)
####################################

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []  # ← ADD THIS (default empty list)

class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []  # ← ADD THIS
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

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    notes_db, note_id_counter = load_notes()
    
    new_note = Note(
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    
    notes_db.append(new_note)
    save_notes(notes_db)
    return new_note

@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None
) -> list[Note]:
    """
    List notes with optional filters
    
    - category: Filter by category
    - search: Search in title and content
    - tag: Filter by tag
    """
    notes_db, _ = load_notes()
    
    # Apply filters
    filtered = []
    for note in notes_db:
        # Filter by category
        if category and note.category != category:
            continue
        
        # Filter by search term
        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()
            if not (title_match or content_match):
                continue
        
        # Filter by tag
        if tag and tag not in note.tags:
            continue
        
        filtered.append(note)
    
    return filtered

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    """Get a specific note by ID"""
    notes_db, _ = load_notes()
    for note in notes_db:
        if note.id == note_id:
            return note
    
    # Not found - raise 404 error
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

################################
######### Crud Endpoints
###############################

@app.get("/queryparameters")
def query_parameters(param1: str = None, param2: int = None) -> dict:
    
    namen = ["Alice", "Bob", "Charlie", "Diana"]

    if not param1: return {"namen": namen}

    namen_gefiltert = []
    for name in namen:
        if param1 in name:
            namen_gefiltert.append(name)

    return {
        "param1": param1,
        "param2": param2,
        "namen": namen_gefiltert
        }

