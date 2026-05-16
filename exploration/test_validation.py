"""Prueft einen einfachen Testfall fuer die API."""
import pytest
import requests
from typing import Generator

BASE_URL = "http://localhost:8000"


@pytest.fixture
def client() -> Generator:
    """Prueft einen einfachen Testfall fuer die API."""
    # Vor dem Test die Datenbank leeren.
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass
    
    yield None  # Hier wird requests direkt als Client benutzt.
    
    # Nach dem Test die Datenbank leeren.
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass


# ============================================================================
# Pydantic-Validierung fuer Felder
# ============================================================================

class TestNoteCreateValidation:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_create_note_rejects_short_title(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "ab",  # zu kurz (min_length=3)
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "title" in str(response.json()).lower()
    
    def test_create_note_rejects_empty_title(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_valid_title(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",  # Mindestens drei Zeichen.
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_create_note_rejects_empty_content(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "",  # min_length=1
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_short_category(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "a",  # zu kurz (min_length=2)
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_valid_category(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "ab",  # Genau zwei Zeichen.
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


class TestTagValidation:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_create_note_normalizes_tags(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["  WORK  ", "Meeting", "WORK"]  # Gross-/Kleinschreibung, Leerzeichen und Duplikate gemischt
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Soll klein geschrieben und ohne Duplikate gespeichert werden
        assert "work" in data["tags"]
        assert "meeting" in data["tags"]
        assert len([t for t in data["tags"] if t == "work"]) == 1  # keine Duplikate
    
    def test_create_note_rejects_short_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["a"]  # zu kurz (min_length=2)
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_long_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["a" * 31]  # zu lang (max_length=30)
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_invalid_chars(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag@name"]  # Sonderzeichen @ ist nicht erlaubt
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_underscore(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag_name"]  # Unterstrich ist nicht erlaubt
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_space(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag name"]  # Leerzeichen ist nicht erlaubt
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_tag_with_dashes_and_digits(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag-123", "my-tag"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "tag-123" in data["tags"]
        assert "my-tag" in data["tags"]
    
    def test_tag_name_rejects_uppercase(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["MyTag", "WORK"]  # Grossbuchstaben sollen klein gemacht werden
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Soll in Kleinbuchstaben umgewandelt werden
        assert "mytag" in data["tags"]
        assert "work" in data["tags"]
        # Die alte Schreibweise soll nicht extra existieren
        assert "MyTag" not in data["tags"]
        assert "WORK" not in data["tags"]


class TestCrossFieldValidation:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_work_note_requires_work_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Work Note",
            "content": "Valid content",
            "category": "work",
            "tags": ["meeting"]  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "work" in str(response.json()).lower()
    
    def test_work_note_succeeds_with_work_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Work Note",
            "content": "Valid content",
            "category": "work",
            "tags": ["work", "important"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "work" in data["tags"]
    
    def test_non_work_note_does_not_require_work_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Personal Note",
            "content": "Valid content",
            "category": "personal",
            "tags": ["shopping"]  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


class TestExtraFieldsRejection:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_create_note_forbids_extra_fields(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"],
            "unknown_field": "should not be here"  # Zusatzfeld
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "unknown_field" in str(response.json()).lower() or "extra" in str(response.json()).lower()
    
    def test_create_note_with_valid_fields_only(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


# ============================================================================
# Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
# ============================================================================

class TestPatchValidation:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_patch_with_empty_body_succeeds(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        # Zuerst eine Notiz erstellen
        payload = {
            "title": "Original",
            "content": "Original content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert create_response.status_code == 201
        note_id = create_response.json()["id"]
        
        # PATCH mit leerem Body.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original"  # unveraendert
    
    def test_patch_with_invalid_title_fails(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        # Zuerst eine Notiz erstellen
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": "ab"})
        assert response.status_code == 422
    
    def test_patch_with_empty_title_fails(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": ""})
        assert response.status_code == 422
    
    def test_patch_with_valid_title_succeeds(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": "Updated"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
    
    def test_patch_with_invalid_tags_fails(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"tags": ["a"]})
        assert response.status_code == 422
    
    def test_patch_work_category_requires_work_tag(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"category": "work", "tags": ["meeting"]}
        )
        assert response.status_code == 422
    
    def test_patch_work_category_with_work_tag_succeeds(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"category": "work", "tags": ["work", "meeting"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "work"
        assert "work" in data["tags"]
    
    def test_patch_forbids_extra_fields(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"title": "Updated", "unknown_field": "bad"}
        )
        assert response.status_code == 422


# ============================================================================
# Integrationstests
# ============================================================================

class TestValidationIntegration:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_full_valid_note_flow(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        # Notiz erstellen
        payload = {
            "title": "My Work Task",
            "content": "This is a detailed work task description",
            "category": "work",
            "tags": ["work", "urgent"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        note_id = response.json()["id"]
        
        # Notiz aktualisieren
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"tags": ["work", "completed"]}
        )
        assert response.status_code == 200
    
    def test_comprehensive_validation_chain(self, client):
        """Prueft einen einfachen Testfall fuer die API."""
        # Ungueltig: leerer Titel
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "", "content": "C", "category": "pc", "tags": ["t1"]}
        ).status_code == 422
        
        # Ungueltig: zu kurze Kategorie
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "p", "tags": ["t1"]}
        ).status_code == 422
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "work", "tags": ["meeting"]}
        ).status_code == 422
        
        # Gueltig: alle Regeln passen
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "work", "tags": ["work"]}
        ).status_code == 201
