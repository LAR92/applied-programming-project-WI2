import requests

BASE_URL = "http://127.0.0.1:8000"

def test_create_note():
    """Test creating a new note"""
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
    """Test listing all notes"""
    response = requests.get(
        f"{BASE_URL}/notes"
    )

    assert response.status_code == 200
    assert isinstance(
        response.json(), list
    )


def test_get_note_by_id():
    """Test getting specific note"""
    # First create a note
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

    # Then get it
    response = requests.get(
        f"{BASE_URL}/notes/{note_id}"
    )
    assert response.status_code == 200


def test_update_note():
    """Test updating a note (PUT)"""
    # Create note first
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Old Title",
        "content": "Old content",
        "category": "Old",
        "tags": ["old"]
    })
    note_id = create_resp.json()["id"]

    # Update it
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
    """Test deleting a note"""
    # Create then delete
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Delete Me",
        "content": "Will be deleted",
        "category": "Temp",
        "tags": []
    })
    note_id = create_resp.json()["id"]

    response = requests.delete(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code in [200, 204]

    # Verify it's gone
    get_resp = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_resp.status_code == 404

#  Task 2: Test Filtering

def test_filter_by_category():
    """Test filtering notes by category"""
    # Create notes in specific category
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

    # All returned notes should be in Work category
    for note in notes:
        assert note["category"] == "Work"


def test_filter_by_search():
    """Test search functionality"""
    # Create a note with "meeting" in title
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Important meeting",
        "content": "Discuss budget",
        "category": "Work",
        "tags": ["meeting"]
    })

    response = requests.get(f"{BASE_URL}/notes?search=meeting")
    assert response.status_code == 200
    # Results should contain "meeting" in title or content
    notes = response.json()
    for note in notes:
        assert "meeting" in note["title"].lower() or "meeting" in note["content"].lower()


def test_filter_by_tag():
    """Test filtering by tag"""
    # Create a note with specific tag
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
    """Test using multiple filters at once"""
    # Create a note that matches all filters
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

    # Verify all filters applied
    for note in notes:
        assert note["category"] == "Work"
        assert "urgent" in note["tags"]


def test_date_filtering():
    """Test date-based filtering (Day 3 Task 5)"""
    # Create a note (will have current timestamp)
    requests.post(f"{BASE_URL}/notes", json={
        "title": "Date Test",
        "content": "Testing date filter",
        "category": "Testing",
        "tags": []
    })

    # Filter with created_after in the past
    response = requests.get(f"{BASE_URL}/notes?created_after=2020-01-01")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Filter with created_before in the future
    response2 = requests.get(f"{BASE_URL}/notes?created_before=2099-12-31")
    assert response2.status_code == 200
    assert len(response2.json()) >= 1

#  Task 3: Test Error Cases

def test_create_note_missing_field():
    """Test creating note with missing required field"""
    invalid_note = {
        "title": "Test",
        # Missing content and category
    }
    response = requests.post(f"{BASE_URL}/notes", json=invalid_note)
    assert response.status_code == 422


def test_get_nonexistent_note():
    """Test getting a note that doesn't exist"""
    response = requests.get(f"{BASE_URL}/notes/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_note():
    """Test updating a note that doesn't exist"""
    updated_data = {
        "title": "Ghost",
        "content": "Does not exist",
        "category": "None",
        "tags": []
    }
    response = requests.put(f"{BASE_URL}/notes/99999", json=updated_data)
    assert response.status_code == 404


def test_delete_nonexistent_note():
    """Test deleting a note that doesn't exist"""
    response = requests.delete(f"{BASE_URL}/notes/99999")
    assert response.status_code == 404

#  Task 4: Test Day 3 Homework Features

def test_notes_statistics():
    """Test GET /notes/stats endpoint (Day 3 Task 2)"""
    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_notes" in data
    assert "by_category" in data


def test_list_categories():
    """Test GET /categories endpoint (Day 3 Task 3)"""
    response = requests.get(f"{BASE_URL}/categories")

    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)


def test_notes_by_category():
    """Test GET /categories/{category}/notes (Day 3 Task 3)"""
    # Create note in known category
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
    """Test PATCH to update only title (Day 3 Task 4)"""
    # Create note
    create_resp = requests.post(f"{BASE_URL}/notes", json={
        "title": "Original Title",
        "content": "Keep this content",
        "category": "Unchanged",
        "tags": ["keep"]
    })
    note_id = create_resp.json()["id"]

    # Update only title
    response = requests.patch(
        f"{BASE_URL}/notes/{note_id}",
        json={"title": "Changed Title"}
    )

    # Check if only title is changed
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Changed Title"
    assert data["content"] == "Keep this content"
    assert data["category"] == "Unchanged"


def test_patch_multiple_fields():
    """Test PATCH with multiple fields"""
    # Similar but update title and content
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
    assert data["content"] == "Old content"  # unchanged