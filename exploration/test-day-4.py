import pytest
import requests
import json
import os

BASE_URL = "http://localhost:8000"

# ============================================================================
# Fixture: Die Datenbank wird vor und nach jedem Test geleert.
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_database():
    """Prueft einen einfachen Testfall fuer die API."""
    # Vor dem Test wird aufgeraeumt.
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass
    
    yield
    
    # Nach dem Test wird nochmal aufgeraeumt.
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass


# ============================================================================
# Einfache Tests fuer Endpunkte.
# ============================================================================

class TestSimpleEndpoints:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_root_endpoint(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        assert "Hello" in data["message"] and "World" in data["message"]
    
    def test_greet_name_endpoint(self):
        """Prueft einen einfachen Testfall fuer die API."""
        test_names = ["Alice", "Bob", "Charlie", "Anna", "Max"]
        for name in test_names:
            response = requests.get(f"{BASE_URL}/name/{name}")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == f"Hello, {name}!"
    
    def test_greet_name_with_special_chars(self):
        """Prueft einen einfachen Testfall fuer die API."""
        test_cases = ["Müller", "José", "François", "Björn"]
        for name in test_cases:
            response = requests.get(f"{BASE_URL}/name/{name}")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == f"Hello, {name}!"
    
    def test_calculate_endpoint(self):
        """Prueft einen einfachen Testfall fuer die API."""
        test_cases = [
            (0, 5),      # 0 * 2 + 5 = 5
            (5, 15),     # 5 * 2 + 5 = 15
            (10, 25),    # 10 * 2 + 5 = 25
            (-5, -5),    # -5 * 2 + 5 = -5
            (3.5, 12),   # 3.5 * 2 + 5 = 12
        ]
        for number, expected_result in test_cases:
            response = requests.get(f"{BASE_URL}/calculate/{number}")
            assert response.status_code == 200
            data = response.json()
            # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
            assert f"Der verrechnete Wert von {float(number)}" in data["message"]
            assert str(float(expected_result)) in data["message"]


# ============================================================================
# Tests zum Erstellen von Notizen.
# ============================================================================

class TestCreateNote:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_create_simple_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Einkaufslist",
            "content": "Milch, Brot, Eier, Käse",
            "category": "Shopping",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Einkaufslist"
        assert data["content"] == "Milch, Brot, Eier, Käse"
        assert data["category"] == "Shopping"
        assert data["tags"] == []
        assert "id" in data
        assert "created_at" in data
    
    def test_create_note_with_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Python Lernen",
            "content": "FastAPI, SQLModel, Testing",
            "category": "Learning",
            "tags": ["python", "programming", "fastapi"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert set(data["tags"]) == {"python", "programming", "fastapi"}
    
    def test_create_note_with_case_insensitive_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test Tags",
            "content": "Testing tag normalization",
            "category": "general",
            "tags": ["Python", "PROGRAMMING", "FastAPI"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        assert set(data["tags"]) == {"python", "programming", "fastapi"}
    
    def test_create_note_with_duplicate_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Duplicate Tags",
            "content": "Testing duplicate handling",
            "category": "general",
            "tags": ["python", "Python", "PYTHON"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["tags"] == ["python"]
    
    def test_create_note_with_long_content(self):
        """Prueft einen einfachen Testfall fuer die API."""
        long_content = ("Lorem ipsum " * 799).rstrip()  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        payload = {
            "title": "Long Note",
            "content": long_content,
            "category": "general",
            "tags": ["long"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == long_content
    
    def test_create_note_with_unicode(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Ünïçödé Têxt 中文 العربية",
            "content": "こんにちは мир 🚀 🎉",
            "category": "general",
            "tags": ["unicode", "international"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["content"] == payload["content"]
    
    def test_create_note_with_invalid_title_too_short(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Hi",  # zu kurz (min 3 chars)
            "content": "Valid content",
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_note_with_invalid_title_too_long(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "A" * 101,  # zu lang (max 100 chars)
            "content": "Valid content",
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_note_with_invalid_content_too_long(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "A" * 10001,  # zu lang (max 10000 chars)
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_note_with_invalid_category_too_short(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "a",  # zu kurz (min 2 chars)
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_note_with_too_many_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "work",
            "tags": [f"tag{i}" for i in range(11)]  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_note_with_whitespace_stripping(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "  Valid Title  ",
            "content": "  Valid content  ",
            "category": "work",
            "tags": [" work ", " tag2 "]  # Bei Kategorie work wird auch der Tag work benutzt.
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Valid Title"  # Whitespace stripped
        assert data["content"] == "Valid content"  # Whitespace stripped
        assert data["tags"] == ["work", "tag2"]  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
    
    def test_create_work_note_with_work_tag_passing(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Work Meeting",
            "content": "Discuss project timeline",
            "category": "work",
            "tags": ["work", "meeting"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_create_work_note_without_work_tag_failing(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Work Meeting",
            "content": "Discuss project timeline",
            "category": "work",
            "tags": ["meeting", "urgent"]  # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Hier wird ein Validierungsfehler erwartet.
    
    def test_create_non_work_note_without_work_tag_passing(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Personal Note",
            "content": "Remember to buy groceries",
            "category": "personal",
            "tags": ["shopping", "reminder"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


# ============================================================================
# Tests zum Auflisten und Laden von Notizen.
# ============================================================================

class TestListNotes:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_list_empty_notes(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_list_all_notes(self):
        """Prueft einen einfachen Testfall fuer die API."""
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        notes_data = [
            {"title": "Note 1", "content": "Content 1", "category": "work", "tags": ["work"]},
            {"title": "Note 2", "content": "Content 2", "category": "personal", "tags": ["personal"]},
            {"title": "Note 3", "content": "Content 3", "category": "work", "tags": ["work", "urgent"]},
        ]
        
        for note_data in notes_data:
            requests.post(f"{BASE_URL}/notes", json=note_data)
        
        response = requests.get(f"{BASE_URL}/notes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in note for note in data)
    
    def test_list_notes_filter_by_category(self):
        """Prueft einen einfachen Testfall fuer die API."""
        # Notizen mit verschiedenen Kategorien erstellen.
        notes = [
            {"title": "Work 1", "content": "Work content 1", "category": "work", "tags": []},
            {"title": "Work 2", "content": "Work content 2", "category": "work", "tags": []},
            {"title": "Personal", "content": "Personal content", "category": "personal", "tags": []},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/notes?category=work")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(note["category"] == "work" for note in data)
    
    def test_list_notes_filter_by_search(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Python Tutorial", "content": "Learn Python basics", "category": "Learn", "tags": []},
            {"title": "JavaScript Guide", "content": "Python vs JavaScript", "category": "Learn", "tags": []},
            {"title": "Database Tips", "content": "Use SQLite for small projects", "category": "Tech", "tags": []},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Nach Python suchen, es sollten zwei Notizen passen.
        response = requests.get(f"{BASE_URL}/notes?search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Nach SQLite suchen, es sollte eine Notiz passen.
        response = requests.get(f"{BASE_URL}/notes?search=SQLite")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_list_notes_search_case_insensitive(self):
        """Prueft einen einfachen Testfall fuer die API."""
        note = {"title": "Python Guide", "content": "Content", "category": "Tech", "tags": []}
        requests.post(f"{BASE_URL}/notes", json=note)
        
        # Die Suche mit verschiedener Gross- und Kleinschreibung testen.
        for search_term in ["python", "PYTHON", "Python", "pYtHoN"]:
            response = requests.get(f"{BASE_URL}/notes?search={search_term}")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
    
    def test_list_notes_filter_by_tag(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Note 1", "content": "Content 1", "category": "Work", "tags": ["urgent", "work"]},
            {"title": "Note 2", "content": "Content 2", "category": "Work", "tags": ["urgent"]},
            {"title": "Note 3", "content": "Content 3", "category": "Personal", "tags": ["personal"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Nach dem Tag urgent filtern, es sollten zwei Notizen passen.
        response = requests.get(f"{BASE_URL}/notes?tag=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("urgent" in note["tags"] for note in data)
    
    def test_list_notes_filter_by_tag_case_insensitive(self):
        """Prueft einen einfachen Testfall fuer die API."""
        note = {"title": "Test", "content": "Content", "category": "Work", "tags": ["URGENT"]}
        requests.post(f"{BASE_URL}/notes", json=note)
        
        # Die Suche mit verschiedener Gross- und Kleinschreibung testen.
        response = requests.get(f"{BASE_URL}/notes?tag=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_list_notes_combined_filters(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Python Work", "content": "Work with Python", "category": "Work", "tags": ["python"]},
            {"title": "Python Personal", "content": "Python hobby", "category": "Personal", "tags": ["python"]},
            {"title": "Work Notes", "content": "Other work", "category": "Work", "tags": ["notes"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Kategorie und Suche zusammen benutzen.
        response = requests.get(f"{BASE_URL}/notes?category=Work&search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Python Work"


# ============================================================================
# Tests fuer eine einzelne Notiz.
# ============================================================================

class TestGetSingleNote:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_get_existing_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test Note",
            "content": "Test content",
            "category": "Test",
            "tags": ["test"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "Test Note"
        assert data["content"] == "Test content"
        assert data["category"] == "Test"
    
    def test_get_nonexistent_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/notes/9999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_get_note_with_multiple_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Tagged Note",
            "content": "Content",
            "category": "Test",
            "tags": ["tag1", "tag2", "tag3"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert set(data["tags"]) == {"tag1", "tag2", "tag3"}


# ============================================================================
# Tests zum Aktualisieren mit PUT.
# ============================================================================

class TestUpdateNote:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_update_all_fields(self):
        """Prueft einen einfachen Testfall fuer die API."""
        # Notiz erstellen
        payload = {
            "title": "Original Title",
            "content": "Original content",
            "category": "Original",
            "tags": ["old"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Alle Felder aktualisieren.
        update_payload = {
            "title": "Updated Title",
            "content": "Updated content",
            "category": "Updated",
            "tags": ["new", "updated"]
        }
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
        assert data["category"] == "Updated"
        assert set(data["tags"]) == {"new", "updated"}
    
    def test_update_title_only(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "Cat",
            "tags": []
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        update_payload = {
            "title": "New Title",
            "content": "Content",  # Gleich lassen.
            "category": "Cat",      # Gleich lassen.
            "tags": []
        }
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
    
    def test_update_nonexistent_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        update_payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": []
        }
        response = requests.put(f"{BASE_URL}/notes/9999", json=update_payload)
        assert response.status_code == 404
    
    def test_update_tags(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "Cat",
            "tags": ["old1", "old2"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        update_payload = {
            "title": "Test",
            "content": "Content",
            "category": "Cat",
            "tags": ["new1", "new2", "new3"]
        }
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert set(data["tags"]) == {"new1", "new2", "new3"}


# ============================================================================
# Tests zum teilweise Aktualisieren mit PATCH.
# ============================================================================

class TestPatchNote:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_patch_title_only(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Original",
            "content": "Original content",
            "category": "Original",
            "tags": ["original"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        
        # Mit PATCH nur den Titel aendern.
        patch_payload = {"title": "Patched Title"}
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        assert data["content"] == "Original content"  # unveraendert
        assert data["category"] == "Original"          # unveraendert
        assert data["tags"] == ["original"]            # unveraendert
    
    def test_patch_content_only(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Original content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        patch_payload = {"content": "New content"}
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Title"           # unveraendert
        assert data["content"] == "New content"
        assert data["category"] == "Cat"          # unveraendert
    
    def test_patch_tags_only(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["old"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        patch_payload = {"tags": ["new", "tags"]}
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200
        data = response.json()
        assert set(data["tags"]) == {"new", "tags"}
        assert data["title"] == "Title"      # unveraendert
        assert data["content"] == "Content"  # unveraendert
    
    def test_patch_multiple_fields(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Original",
            "content": "Original",
            "category": "Original",
            "tags": ["original"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        patch_payload = {
            "title": "Patched",
            "tags": ["patched", "updated"]
        }
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched"
        assert set(data["tags"]) == {"patched", "updated"}
        assert data["content"] == "Original"  # unveraendert
        assert data["category"] == "Original" # unveraendert
    
    def test_patch_empty_payload(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        original_data = create_response.json()
        
        # Mit PATCH ein leeres Objekt senden.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
        assert response.status_code == 200
        data = response.json()
        # Alle Felder sollen gleich bleiben.
        assert data["title"] == original_data["title"]
        assert data["content"] == original_data["content"]
        assert data["category"] == original_data["category"]
    
    # Regeln fuer NoteUpdate testen.
    
    def test_patch_title_constraint_min_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einen zu kurzen Titel mit PATCH testen.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": ""})
        assert response.status_code == 422
        
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": "ab"})
        assert response.status_code == 422
    
    def test_patch_title_constraint_max_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einen zu langen Titel mit PATCH testen.
        long_title = "a" * 101
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": long_title})
        assert response.status_code == 422
    
    def test_patch_content_constraint_min_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Leeren Inhalt mit PATCH testen.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"content": ""})
        assert response.status_code == 422
    
    def test_patch_content_constraint_max_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Zu langen Inhalt mit PATCH testen.
        long_content = "a" * 10001
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"content": long_content})
        assert response.status_code == 422
    
    def test_patch_category_constraint_min_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Zu kurze Kategorie mit PATCH testen.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"category": ""})
        assert response.status_code == 422
        
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"category": "a"})
        assert response.status_code == 422
    
    def test_patch_category_constraint_max_length(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Zu lange Kategorie mit PATCH testen.
        long_category = "a" * 31
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"category": long_category})
        assert response.status_code == 422
    
    def test_patch_tags_constraint_max_items(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Zu viele Tags mit PATCH testen.
        too_many_tags = [f"tag{i}" for i in range(11)]
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"tags": too_many_tags})
        assert response.status_code == 422
    
    def test_patch_work_category_requires_work_tag(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Kategorie work ohne work-Tag testen.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={
            "category": "work",
            "tags": ["meeting"]
        })
        assert response.status_code == 422
        
        # Nur die Kategorie zu aendern soll hier klappen.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"category": "work"})
        assert response.status_code == 200
    
    def test_patch_work_category_with_work_tag(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Kategorie und Tags zusammen aendern, inklusive work-Tag.
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={
            "category": "work",
            "tags": ["work", "meeting"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "work"
        assert "work" in data["tags"]
    
    def test_patch_nonexistent_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.patch(f"{BASE_URL}/notes/9999", json={"title": "New"})
        assert response.status_code == 404


# ============================================================================
# Tests zum Loeschen von Notizen.
# ============================================================================

class TestDeleteNote:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_delete_existing_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "To Delete",
            "content": "Content",
            "category": "Cat",
            "tags": ["delete"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Pruefen, ob die Notiz existiert.
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 200
        
        # Notiz loeschen.
        response = requests.delete(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 204 or response.status_code == 200
        
        # Pruefen, ob die Notiz weg ist.
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 404
    
    def test_delete_nonexistent_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.delete(f"{BASE_URL}/notes/9999")
        assert response.status_code == 404
    
    def test_delete_note_removes_from_list(self):
        """Prueft einen einfachen Testfall fuer die API."""
        # Drei Notizen erstellen.
        for i in range(3):
            payload = {
                "title": f"Note {i}",
                "content": "Content",
                "category": "Cat",
                "tags": []
            }
            requests.post(f"{BASE_URL}/notes", json=payload)
        
        # Alle Notizen laden, es sollten drei sein.
        response = requests.get(f"{BASE_URL}/notes")
        notes = response.json()
        note_id_to_delete = notes[0]["id"]
        
        # Die erste Notiz loeschen.
        requests.delete(f"{BASE_URL}/notes/{note_id_to_delete}")
        
        # Nochmal laden, es sollten zwei sein.
        response = requests.get(f"{BASE_URL}/notes")
        notes = response.json()
        assert len(notes) == 2
        assert all(note["id"] != note_id_to_delete for note in notes)


# ============================================================================
# Tests fuer Statistiken.
# ============================================================================

class TestNotesStats:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_stats_empty_database(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/notes/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_notes"] == 0
        assert data["by_category"] == {}
        assert data["top_tags"] == []
        assert data["unique_tags_count"] == 0
    
    def test_stats_single_note(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "work",
            "tags": ["work", "tag1"]
        }
        requests.post(f"{BASE_URL}/notes", json=payload)
        
        response = requests.get(f"{BASE_URL}/notes/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_notes"] == 1
        assert data["by_category"]["work"] == 1
        assert data["unique_tags_count"] == 2
        assert len(data["top_tags"]) == 1
    
    def test_stats_multiple_notes_categories(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Work 1", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "Work 2", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "Personal", "content": "C", "category": "personal", "tags": ["personal"]},
            {"title": "General", "content": "C", "category": "general", "tags": ["general"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/notes/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_notes"] == 4
        assert data["by_category"]["work"] == 2
        assert data["by_category"]["personal"] == 1
        assert data["by_category"]["general"] == 1
    
    def test_stats_tag_frequency(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Note 1", "content": "C", "category": "work", "tags": ["work", "python", "code"]},
            {"title": "Note 2", "content": "C", "category": "work", "tags": ["work", "python", "tutorial"]},
            {"title": "Note 3", "content": "C", "category": "work", "tags": ["work", "javascript", "code"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/notes/stats")
        assert response.status_code == 200
        data = response.json()
        
        # Tag-Zaehler suchen.
        tag_dict = {tag["tag"]: tag["count"] for tag in data["top_tags"]}
        assert tag_dict["python"] == 2
        assert tag_dict["code"] == 2
        assert tag_dict["tutorial"] == 1
        assert tag_dict["javascript"] == 1


# ============================================================================
# Tests fuer Tag-Endpunkte.
# ============================================================================

class TestTagsEndpoints:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_list_tags_returns_list(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/tags")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Tags sind sortiert.
        assert data == sorted(data)
    
    def test_list_tags_with_created_notes(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "N1", "content": "C", "category": "Cat", "tags": ["zebra", "apple", "mango"]},
            {"title": "N2", "content": "C", "category": "Cat", "tags": ["banana"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/tags")
        assert response.status_code == 200
        data = response.json()
        # Die neuen Tags sollen in der Liste sein.
        assert "zebra" in data
        assert "apple" in data
        assert "mango" in data
        assert "banana" in data
        # Pruefen, ob es sortiert ist.
        assert data == sorted(data)
    
    def test_get_notes_by_tag(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Python 1", "content": "Content", "category": "school", "tags": ["python", "programming"]},
            {"title": "Python 2", "content": "Content", "category": "school", "tags": ["python"]},
            {"title": "JavaScript", "content": "Content", "category": "school", "tags": ["javascript", "programming"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Notizen mit dem Tag python laden.
        response = requests.get(f"{BASE_URL}/tags/python/notes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("python" in note["tags"] for note in data)
    
    def test_get_notes_by_nonexistent_tag(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/tags/nonexistent_unique_tag_xyz/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []


# ============================================================================
# Tests fuer Kategorie-Endpunkte.
# ============================================================================

class TestCategoriesEndpoints:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_list_categories_empty(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/categories")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_list_categories_sorted(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "N1", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "N2", "content": "C", "category": "personal", "tags": []},
            {"title": "N3", "content": "C", "category": "school", "tags": []},
            {"title": "N4", "content": "C", "category": "personal", "tags": []},  # Doppelte Kategorie.
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/categories")
        assert response.status_code == 200
        data = response.json()
        # Soll eindeutig und sortiert sein
        assert data == ["personal", "school", "work"]
    
    def test_get_notes_by_category_endpoint(self):
        """Prueft einen einfachen Testfall fuer die API."""
        notes = [
            {"title": "Work 1", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "Work 2", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "Personal", "content": "C", "category": "personal", "tags": []},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/categories/work/notes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(note["category"] == "work" for note in data)
    
    def test_get_notes_by_nonexistent_category(self):
        """Prueft einen einfachen Testfall fuer die API."""
        response = requests.get(f"{BASE_URL}/categories/NonExistent/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []


# ============================================================================
# Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
# ============================================================================

class TestTagValidation:
    """Prueft einen einfachen Testfall fuer die API."""
    
    def test_tag_valid_simple(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["work"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "work" in data["tags"]
    
    def test_tag_valid_with_digits(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag123"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "tag123" in data["tags"]
    
    def test_tag_valid_with_dashes(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["my-tag-123"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "my-tag-123" in data["tags"]
    
    def test_tag_whitespace_stripped(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["  work  ", "\ttag\n"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Leerzeichen sollen entfernt werden
        assert "work" in data["tags"]
        assert "tag" in data["tags"]
        # Versionen mit Leerzeichen sollen nicht existieren
        assert "  work  " not in data["tags"]
    
    def test_tag_uppercase_converted_to_lowercase(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["WORK", "Meeting"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Soll klein geschrieben sein
        assert "work" in data["tags"]
        assert "meeting" in data["tags"]
        # Grossschreibung soll nicht extra existieren
        assert "WORK" not in data["tags"]
        assert "Meeting" not in data["tags"]
    
    def test_tag_min_length_1_fails(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["a"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_tag_min_length_2_succeeds(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["ab"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_tag_max_length_30_succeeds(self):
        """Prueft einen einfachen Testfall fuer die API."""
        tag_30 = "a" * 30
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": [tag_30]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_tag_max_length_31_fails(self):
        """Prueft einen einfachen Testfall fuer die API."""
        tag_31 = "a" * 31
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": [tag_31]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_tag_invalid_uppercase_in_pattern(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["MyTag"]  # enthaelt Grossbuchstaben
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        # Eigentlich wird Grossschreibung vorher klein gemacht.
        # Der Validator macht daraus Kleinbuchstaben, deshalb ist es gueltig.
        assert response.status_code == 201
        data = response.json()
        assert "mytag" in data["tags"]
    
    def test_tag_invalid_special_chars(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag@name"]  # enthaelt @
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_tag_invalid_underscore(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag_name"]  # enthaelt Unterstrich
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_tag_invalid_space(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag name"]  # enthaelt ein Leerzeichen in der Mitte
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_tag_valid_dash_at_edges(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["-tag-", "a-b"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "-tag-" in data["tags"]
        assert "a-b" in data["tags"]
    
    def test_tag_empty_string_fails(self):
        """Prueft einen einfachen Testfall fuer die API."""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["   "]  # nur Leerzeichen
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        assert response.status_code == 422
    
    def test_patch_tag_constraint_validation(self):
        """Prueft einen einfachen Testfall fuer die API."""
        # Erste Notiz erstellen
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
        patch_payload = {"tags": ["a"]}  # zu kurz (min_length=2)
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 422
        
        # PATCH mit einem gueltigen Tag soll klappen.
        patch_payload = {"tags": ["tag2", "tag-3"]}
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200