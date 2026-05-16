import requests

BASE_URL = "http://127.0.0.1:8000"

def test_create_note():
    """Prueft einen einfachen Testfall fuer die API."""
    note_data = {
        "title": "Test Note",
        "content": "Test content",
        "category": "Testing",
        "tags": ["test", "pytest"]
    }
    response = requests.post(
        f"{BASE_URL}/notes", 
        json=note_data
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert "id" in data
    assert "created_at" in data


def test_list_notes():
    """Prueft einen einfachen Testfall fuer die API."""
    response = requests.get(
        f"{BASE_URL}/notes"
    )

    assert response.status_code == 200
    assert isinstance(
        response.json(), list
    )


def test_get_note_by_id():
    """Prueft einen einfachen Testfall fuer die API."""
    # Zuerst eine Notiz erstellen.
    create_resp = requests.post(
        f"{BASE_URL}/notes",
        json={
            "title": "Find Me",
            "content": "Test content",
            "category": "Testing",
            "tags": ["test"]
        }
    )
    note_id = create_resp.json()["id"]

    # Danach wieder abrufen
    response = requests.get(
        f"{BASE_URL}/notes/{note_id}"
    )
    assert response.status_code == 200


def test_update_note():
    """Prueft einen einfachen Testfall fuer die API."""
    # Zuerst eine Notiz erstellen.
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Old Title",
        "content": "Old content",
        "category": "Old",
        "tags": ["old"]
    })
    note_id = create_resp.json()["id"]

    # Dann aktualisieren
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "category": "Updated",
        "tags": ["updated"]
    }
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_delete_note():
    """Prueft einen einfachen Testfall fuer die API."""
    # Erstellen und danach loeschen
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Delete Me",
        "content": "Will be deleted",
        "category": "Temp",
        "tags": []
    })
    note_id = create_resp.json()["id"]

    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code in [200, 204]

    # Pruefen, ob sie wirklich weg ist
    get_resp = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_resp.status_code == 404

# Aufgabe 2: Filter testen.

def test_filter_by_category():
    """Prueft einen einfachen Testfall fuer die API."""
    # Notizen in einer bestimmten Kategorie erstellen.
    for i in range(3):
        requests.post(f"{BASE_URL}/notes", json={
            "title": f"Note {i}",
            "content": "Content",
            "category": "Work",
            "tags": []
        })

    response = requests.get(f"{BASE_URL}/notes?category=Work")

    assert response.status_code == 200
    notes = response.json()

    # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
    for note in notes:
        assert note["category"] == "Work"


def test_filter_by_search():
    """Prueft einen einfachen Testfall fuer die API."""
    # Eine Notiz mit "meeting" im Titel erstellen
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Important meeting",
        "content": "Discuss budget",
        "category": "Work",
        "tags": ["meeting"]
    })

    response = requests.get(f"{BASE_URL}/notes?search=meeting")
    assert response.status_code == 200
    # Ergebnisse sollen "meeting" im Titel oder Inhalt haben
    notes = response.json()
    for note in notes:
        assert "meeting" in note["title"].lower() or "meeting" in note["content"].lower()


def test_filter_by_tag():
    """Prueft einen einfachen Testfall fuer die API."""
    # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Tagged Note",
        "content": "Has urgent tag",
        "category": "Work",
        "tags": ["urgent"]
    })

    response = requests.get(f"{BASE_URL}/notes?tag=urgent")
    assert response.status_code == 200
    notes = response.json()
    for note in notes:
        assert "urgent" in note["tags"]


def test_combined_filters():
    """Prueft einen einfachen Testfall fuer die API."""
    # Eine Notiz erstellen, die zu allen Filtern passt
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Urgent meeting notes",
        "content": "Budget meeting discussion",
        "category": "Work",
        "tags": ["urgent", "meeting"]
    })

    response = requests.get(
        f"{BASE_URL}/notes?category=Work&tag=urgent&search=meeting"
    )

    assert response.status_code == 200
    notes = response.json()

    # Einfacher Hinweis: Hier wird dieser Testschritt vorbereitet oder geprueft.
    for note in notes:
        assert note["category"] == "Work"
        assert "urgent" in note["tags"]


def test_date_filtering():
    """Prueft einen einfachen Testfall fuer die API."""
    # Eine Notiz erstellen, sie bekommt die aktuelle Zeit
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Date Test",
        "content": "Testing date filter",
        "category": "Testing",
        "tags": []
    })

    # Mit created_after in der Vergangenheit filtern
    response = requests.get(f"{BASE_URL}/notes?created_after=2020-01-01")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Mit created_before in der Zukunft filtern
    response2 = requests.get(f"{BASE_URL}/notes?created_before=2099-12-31")
    assert response2.status_code == 200
    assert len(response2.json()) >= 1

# Aufgabe 3: Fehlerfaelle testen.

def test_create_note_missing_field():
    """Prueft einen einfachen Testfall fuer die API."""
    invalid_note = {
        "title": "Test",
        # Content und Kategorie fehlen
    }
    response = requests.post(f"{BASE_URL}/notes", json=invalid_note)
    assert response.status_code == 422


def test_get_nonexistent_note():
    """Prueft einen einfachen Testfall fuer die API."""
    response = requests.get(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_note():
    """Prueft einen einfachen Testfall fuer die API."""
    updated_data = {
        "title": "Ghost",
        "content": "Does not exist",
        "category": "None",
        "tags": []
    }
    response = requests.put(f"{BASE_URL}/notes/99999", json=updated_data)
    assert response.status_code == 404


def test_delete_nonexistent_note():
    """Prueft einen einfachen Testfall fuer die API."""
    response = requests.delete(f"{BASE_URL}/notes/99999")
    assert response.status_code == 404

# Aufgabe 4: Funktionen von Tag 3 testen.

def test_notes_statistics():
    """Prueft einen einfachen Testfall fuer die API."""
    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_notes" in data
    assert "by_category" in data


def test_list_categories():
    """Prueft einen einfachen Testfall fuer die API."""
    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)


def test_notes_by_category():
    """Prueft einen einfachen Testfall fuer die API."""
    # Notiz erstellen in known Kategorie
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Category Test",
        "content": "Testing category endpoint",
        "category": "Science",
        "tags": []
    })

    response = requests.get(f"{BASE_URL}/categories/Science/notes")
    assert response.status_code == 200
    notes = response.json()
    for note in notes:
        assert note["category"] == "Science"


def test_patch_note_title_only():
    """Prueft einen einfachen Testfall fuer die API."""
    # Notiz erstellen
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Original Title",
        "content": "Keep this content",
        "category": "Unchanged",
        "tags": ["keep"]
    })
    note_id = create_resp.json()["id"]

    # Nur den Titel aktualisieren
    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={"title": "Changed Title"}
    )

    # Pruefen, ob nur der Titel geaendert wurde
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Changed Title"
    assert data["content"] == "Keep this content"
    assert data["category"] == "Unchanged"


def test_patch_multiple_fields():
    """Prueft einen einfachen Testfall fuer die API."""
    # Aehnlich, aber Titel und Inhalt werden geaendert
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Multi Patch",
        "content": "Old content",
        "category": "Old",
        "tags": ["old"]
    })
    note_id = create_resp.json()["id"]

    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={"title": "New Title", "category": "New"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["category"] == "New"
    assert data["content"] == "Old content"  # Bleibt unveraendert.