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