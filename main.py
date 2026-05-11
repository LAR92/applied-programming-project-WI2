from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Optional
import re
from sqlmodel import SQLModel, Field, Session, col, create_engine, Relationship, or_, select
from typing import Annotated
from fastapi import Depends

# Main application implementing a notes API backed by SQLModel (SQLite).
# Contains models, DB setup, and FastAPI endpoints for CRUD and stats.

class NoteTag(SQLModel, table=True):
    __tablename__ = "note_tag"
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)
    # Association table for many-to-many Note <-> Tag relationship


class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Many-to-many relationship with Tag via NoteTag association table
    tags: list["Tag"] = Relationship(back_populates="notes", link_model=NoteTag)
    # `tags` will hold Tag objects linked through NoteTag

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        unique=True, 
        index=True,
        min_length=2,
        max_length=30
    )
    
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        """
        Validate and normalize tag name:
        - Strip whitespace
        - Convert to lowercase
        - Validate against pattern: lowercase, digits, dashes only
        """
        if not isinstance(v, str):
            raise ValueError("name must be a string")
        
        # Strip whitespace and lowercase
        v = v.strip().lower()
        
        # Validate pattern: only lowercase letters, digits, and dashes
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("name must contain only lowercase letters, digits, and dashes")
        
        return v
    
    # Many-to-many relationship with Note (implicit link table)
    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTag)
    # `notes` will be populated with Note objects linked to this tag

# Create database engine
engine = create_engine("sqlite:///notes.db")

# Create DB tables if they do not exist yet: notes, tags, note_tag
SQLModel.metadata.create_all(engine)

def validate_and_normalize_tag(tag_name: str) -> str:
    """
    Validate and normalize a tag name:
    - Strip whitespace
    - Convert to lowercase
    - Check length (2-30 chars)
    - Validate pattern (lowercase, digits, dashes only)
    
    Raises ValueError if validation fails.
    Returns normalized tag name.
    """
    if not isinstance(tag_name, str):
        raise ValueError("tag name must be a string")
    
    # Strip and lowercase
    tag_name = tag_name.strip().lower()
    
    # Check minimum length
    if len(tag_name) < 2:
        raise ValueError("tag name must be at least 2 characters")
    
    # Check maximum length
    if len(tag_name) > 30:
        raise ValueError("tag name must be at most 30 characters")
    
    # Validate pattern: only lowercase letters, digits, and dashes
    if not re.match(r"^[a-z0-9-]+$", tag_name):
        raise ValueError("tag name must contain only lowercase letters, digits, and dashes")
    
    return tag_name

def get_session():
    """Create a new database session for each request"""
    with Session(engine) as session:
        yield session


def parse_iso_datetime(value: Optional[str], param_name: str) -> Optional[datetime]:
    if value is None:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={"loc": ["query", param_name], "msg": "Invalid datetime format", "type": "value_error"},
        )

# Dependency type alias for request handlers

# Type alias for cleaner code
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(
    title="Note Taking API",
    description="Simple note management",
    version="1.0.0"
)

@app.get("/")
def root():
    # Simple health/root endpoint
    return {"message": "Hello, World!"}

@app.get("/name/{name}")
def greet_name(name: str):
    # Echo endpoint with a path parameter
    return {"message": f"Hello, {name}!"}

@app.get("/calculate/{number}")
def calculate(number: float):
    result = number * 2 + 5
    # Example calculation endpoint returning localized message
    return {"message": f"Der verrechnete Wert von {number} ist {result}"}


####################################
### Note API Endpoints (Day 2)
####################################

# API Input model
class NoteCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1, max_length=10000)
    category: str = Field(min_length=2, max_length=30)
    tags: list[str] = Field(default_factory=list, max_length=10)
    # Input model for creating/updating notes (tags as list of names)
    
    model_config = {
        "str_strip_whitespace": True,
        "extra": "forbid"
    }
    
    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v):
        """Validate each tag in the list"""
        if not isinstance(v, list):
            raise ValueError("tags must be a list")
        
        # Filter out empty strings and validate each tag
        validated_tags = []
        seen = set()
        
        for tag in v:
            if not isinstance(tag, str):
                raise ValueError("each tag must be a string")
            
            # Validate and normalize tag
            try:
                tag_normalized = validate_and_normalize_tag(tag)
            except ValueError as e:
                raise ValueError(f"Invalid tag '{tag}': {str(e)}")
            
            # Skip duplicates
            if tag_normalized not in seen:
                validated_tags.append(tag_normalized)
                seen.add(tag_normalized)
        
        return validated_tags

# API Output model
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str
    
    class Config:
        from_attributes = True
    # Output model for API responses (serializes DB attributes)


class FileNote(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    # If a JSON file exists (legacy), load FileNote entries for file-backed endpoints
    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            # Ensure older entries without `tags` don't break validation
            for note_dict in data:
                if 'tags' not in note_dict:
                    note_dict['tags'] = []

            # Parse file-backed notes into FileNote Pydantic models
            notes_db = [FileNote(**note_dict) for note_dict in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert FileNote objects to dicts and write JSON
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note in database"""
    
    # Create new Note DB object (will get an id after commit)
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )
    
    # Get or create tags (case-insensitive, deduplicated)
    tag_objects = []
    seen_tags = set()
    
    # Normalize and deduplicate tag names, find or create Tag rows
    for tag_name in note.tags:
        try:
            # Validate and normalize tag name
            tag_name_normalized = validate_and_normalize_tag(tag_name)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Invalid tag: {str(e)}")
        
        # Skip if already seen in this request
        if tag_name_normalized in seen_tags:
            continue
        
        seen_tags.add(tag_name_normalized)
        
        # Find existing tag or create new one
        statement = select(Tag).where(Tag.name == tag_name_normalized)
        existing_tag = session.exec(statement).first()
        
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_normalized)
            session.add(new_tag)
            tag_objects.append(new_tag)
    
    # Attach Tag objects to the Note relationship
    db_note.tags = tag_objects
    
    session.add(db_note)
    session.commit()
    session.refresh(db_note)  # Get the generated ID and load relationships
    
    # Convert to response model
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )

@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
) -> list[NoteResponse]:
    """List notes with filters"""
    
    # Build base query for notes
    statement = select(Note)
    
    # Apply filters
    if category:
        statement = statement.where(Note.category == category)
    
    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%")
            )
        )
    
    if tag:
        tag_lower = tag.lower()
        statement = statement.join(Note.tags).where(Tag.name == tag_lower)

    if created_after:
        created_after_dt = parse_iso_datetime(created_after, "created_after")
        statement = statement.where(Note.created_at >= created_after_dt)

    if created_before:
        created_before_dt = parse_iso_datetime(created_before, "created_before")
        statement = statement.where(Note.created_at <= created_before_dt)
    
    # Execute query and return NoteResponse objects
    notes = session.exec(statement).all()
    
    # Convert DB Note objects to API response models
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[tag.name for tag in n.tags],
            created_at=n.created_at.isoformat()
        )
        for n in notes
    ]

@app.get("/notes/category/{category}")
def get_notes_by_category(category: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes in a specific category"""
    statement = select(Note).where(Note.category == category)
    notes = session.exec(statement).all()
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[tag.name for tag in n.tags],
            created_at=n.created_at.isoformat()
        )
        for n in notes
    ]


@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    """Get statistics about notes (queries SQL database)."""
    # Load all notes including their tags via relationships
    notes = session.exec(select(Note)).all()

    # Count by category and tags
    categories: dict[str, int] = {}
    tag_counts: dict[str, int] = {}

    # Aggregate category counts and tag counts
    for note in notes:
        categories[note.category] = categories.get(note.category, 0) + 1
        for tag in getattr(note, "tags", []) or []:
            # tags are Tag objects in DB
            tag_name = getattr(tag, "name", None) or str(tag)
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1

    # Build top_tags list as list of {"tag": tag, "count": count}, sorted desc
    top_tags = [
        {"tag": tag, "count": count}
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    ][:5]

    unique_tags_count = len(session.exec(select(Tag)).all())

    return {
        "total_notes": len(notes),
        "by_category": categories,
        "top_tags": top_tags,
        "unique_tags_count": unique_tags_count
    }


@app.get("/notes/{note_id}")
def get_note(note_id: str, session: SessionDep) -> NoteResponse:
    """Get a specific note by ID"""
    try:
        note_id_int = int(note_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="note_id must be an integer")

    statement = select(Note).where(Note.id == note_id_int)
    note = session.exec(statement).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat()
    )




# Day 3

# PUT Endpoint um eine bestehende Note zu aktualisieren
@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    """Update an existing note"""

    statement = select(Note).where(Note.id == note_id)
    note = session.exec(statement).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update note fields (handle tags specially)
    update_data = note_update.dict(exclude_unset=True)

    # Handle tags specially: convert tag names to Tag objects
    if "tags" in update_data:
        tag_objects = []
        seen = set()
        for tag_name in update_data["tags"]:
            tag_name_lower = tag_name.lower().strip()
            if not tag_name_lower or tag_name_lower in seen:
                continue
            seen.add(tag_name_lower)
            stmt = select(Tag).where(Tag.name == tag_name_lower)
            existing = session.exec(stmt).first()
            if existing:
                tag_objects.append(existing)
            else:
                new_tag = Tag(name=tag_name_lower)
                session.add(new_tag)
                tag_objects.append(new_tag)

        note.tags = tag_objects

    # Update other simple fields
    for key, value in update_data.items():
        if key == "tags":
            continue
        setattr(note, key, value)

    session.commit()
    session.refresh(note)
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat()
    )

# Delete Endpoint um eine Note zu löschen
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note"""
    statement = select(Note).where(Note.id == note_id)
    note = session.exec(statement).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return Response(status_code=204)

# GET Endpoint um alle einzigartigen Tags aus allen Notizen zu bekommen
@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags from all notes"""
    statement = select(Tag)
    tags = session.exec(statement).all()
    
    return sorted([tag.name for tag in tags])


# GET Endpoint um alle Notizen mit einem bestimmten Tag zu bekommen
@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes with specific tag"""
    
    # Find the tag (case-insensitive)
    tag_lower = tag_name.lower()
    statement = select(Tag).where(Tag.name == tag_lower)
    tag = session.exec(statement).first()
    
    if not tag:
        return []  # No notes if tag doesn't exist
    
    # Return all notes associated with this tag
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            category=note.category,
            tags=[t.name for t in note.tags],
            created_at=note.created_at.isoformat()
        )
        for note in tag.notes
    ]


# GET Endpoint um alle einzigartigen Kategorien aus allen Notizen zu bekommen
@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    """Get all unique categories from all notes"""
    statement = select(Note.category).distinct()
    categories = session.exec(statement).all()
    
    return sorted(categories)


# GET Endpoint um alle Notizen einer bestimmten Kategorie zu bekommen
@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes in a specific category"""
    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()
    
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            category=note.category,
            tags=[tag.name for tag in note.tags],
            created_at=note.created_at.isoformat()
        )
        for note in notes
    ]

# Add PATCH ENDPOINT um nur bestimmte Felder einer Note zu aktualisieren

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    category: Optional[str] = Field(None, min_length=2, max_length=30)
    tags: Optional[list[str]] = Field(None, max_length=10)
    
    model_config = {
        "str_strip_whitespace": True,
        "extra": "forbid"
    }
    
    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v):
        """Validate each tag in the list (only if provided)"""
        if v is None:
            return None
        
        if not isinstance(v, list):
            raise ValueError("tags must be a list")
        
        # Filter out empty strings and validate each tag
        validated_tags = []
        seen = set()
        
        for tag in v:
            if not isinstance(tag, str):
                raise ValueError("each tag must be a string")
            
            # Validate and normalize tag
            try:
                tag_normalized = validate_and_normalize_tag(tag)
            except ValueError as e:
                raise ValueError(f"Invalid tag '{tag}': {str(e)}")
            
            # Skip duplicates
            if tag_normalized not in seen:
                validated_tags.append(tag_normalized)
                seen.add(tag_normalized)
        
        return validated_tags
    
    @model_validator(mode="after")
    def validate_work_category_requires_work_tag(self):
        """
        Cross-field validation: if both category and tags are provided,
        and category is "work", then tags must contain "work".
        Only validates if both fields are provided (not None).
        """
        if self.category == "work" and self.tags is not None and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")
        return self

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> NoteResponse:
    """
    Partially update a note (only provided fields)
    
    Unlike PUT, PATCH only updates fields you provide
    """
    statement = select(Note).where(Note.id == note_id)
    note = session.exec(statement).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update only provided fields
    update_data = note_update.dict(exclude_unset=True)

    # Handle tags specially: convert tag names to Tag objects
    if "tags" in update_data:
        tag_objects = []
        seen = set()
        for tag_name in update_data["tags"]:
            try:
                # Validate and normalize tag name
                tag_name_normalized = validate_and_normalize_tag(tag_name)
            except ValueError as e:
                raise HTTPException(status_code=422, detail=f"Invalid tag: {str(e)}")
            
            # Skip if already seen in this request
            if tag_name_normalized in seen:
                continue
            seen.add(tag_name_normalized)
            
            stmt = select(Tag).where(Tag.name == tag_name_normalized)
            existing = session.exec(stmt).first()
            if existing:
                tag_objects.append(existing)
            else:
                new_tag = Tag(name=tag_name_normalized)
                session.add(new_tag)
                tag_objects.append(new_tag)

        note.tags = tag_objects

    # Update other simple fields
    for key, value in update_data.items():
        if key == "tags":
            continue
        setattr(note, key, value)

    session.add(note)
    session.commit()
    session.refresh(note)

    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat()
    )

######