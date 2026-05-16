# ============================================================================
# Tag 4: Erweiterte API-Funktionen
# ============================================================================
# Ziel: Tests fuer unsere API schreiben und ausfuehren
# - pytest benutzen, um API-Endpunkte zu testen
# - mit TestClient Anfragen an die API nachstellen
# - mit requests die API von aussen ausprobieren
# Themen: FastAPI testen, pytest, TestClient und requests
# ============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

# FastAPI-App erstellen
app = FastAPI(
    title="Applied Programming Course API",
    description="Beispiel-Loesung fuer Tag 4",
    version="1.0.0"
)

# ----------------------------------------------------------------------------
# Pydantic-Modelle
# ----------------------------------------------------------------------------

class GreetingResponse(BaseModel):
    """Antwortmodell fuer Begruessungen.

    Es enthaelt nur die Nachricht, die zurueckgegeben wird."""
    message: str

# ----------------------------------------------------------------------------
# Tag 4: API-Endpunkte zum Testen
# ----------------------------------------------------------------------------

@app.get("/", response_model=GreetingResponse)
def read_root():
    """Start-Endpunkt. Gibt eine Begruessung zurueck."""
    return {"message": "Hello World!"}




@app.get("/greet/{name}", response_model=GreetingResponse)
@app.get("/greetings/{name}", response_model=GreetingResponse)
def read_greeting(name: str):
    """Begruessungs-Endpunkt mit Namen."""
    return {"message": f"Hello, {name}!"}


# ----------------------------------------------------------------------------
# Absichtlich fehlerhafter Endpunkt fuer den Unterricht
# ----------------------------------------------------------------------------

@app.get("/is-adult/{age}")
def check_adult(age: int):
    """Prueft, ob eine Person volljaehrig ist.
    Beispiel: /is-adult/17"""
    is_adult = age > 18

    return {
        "age": age,
        "is_adult": is_adult,
        "can_vote": is_adult,
        "can_drive": is_adult
    }

