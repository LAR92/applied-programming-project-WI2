import pytest
import requests
import json
import os

BASE_URL = "http://localhost:8000"

# ============================================================================
# FIXTURE: Clear database before and after each test
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_database():
    """Clear the database before each test"""
    # Before test
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass
    
    yield
    
    # After test - also cleanup
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass


# ============================================================================
# SIMPLE ENDPOINTS TESTS
# ============================================================================

class TestSimpleEndpoints:
    """Test basic greeting and calculation endpoints"""
    
    def test_root_endpoint(self):
        """Test GET / returns correct message"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        # The root endpoint returns "Hello, World!" (with comma)
        assert "Hello" in data["message"] and "World" in data["message"]
    
    def test_greet_name_endpoint(self):
        """Test GET /name/{name} with various names"""
        test_names = ["Alice", "Bob", "Charlie", "Anna", "Max"]
        for name in test_names:
            response = requests.get(f"{BASE_URL}/name/{name}")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == f"Hello, {name}!"
    
    def test_greet_name_with_special_chars(self):
        """Test GET /name with special characters"""
        test_cases = ["Müller", "José", "François", "Björn"]
        for name in test_cases:
            response = requests.get(f"{BASE_URL}/name/{name}")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == f"Hello, {name}!"
    
    def test_calculate_endpoint(self):
        """Test GET /calculate/{number} with various numbers"""
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
            # The API returns floats, so we convert to float for comparison
            assert f"Der verrechnete Wert von {float(number)}" in data["message"]
            assert str(float(expected_result)) in data["message"]


# ============================================================================
# CREATE NOTE TESTS
# ============================================================================

class TestCreateNote:
    """Test POST /notes endpoint"""
    
    def test_create_simple_note(self):
        """Test creating a note with title, content, category"""
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
        """Test creating a note with multiple tags"""
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
        """Test that tags are normalized to lowercase"""
        payload = {
            "title": "Test Tags",
            "content": "Testing tag normalization",
            "category": "general",
            "tags": ["Python", "PROGRAMMING", "FastAPI"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Tags should be lowercased
        assert set(data["tags"]) == {"python", "programming", "fastapi"}
    
    def test_create_note_with_duplicate_tags(self):
        """Test that duplicate tags are deduplicated"""
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
        """Test creating a note with very long content"""
        long_content = ("Lorem ipsum " * 799).rstrip()  # About 9599 characters, no trailing space
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
        """Test creating notes with unicode characters"""
        payload = {
            "title": "Ünïçödé Têxt 中文 العربية",
            "content": "こんにちは мир 🚀 🎉",
            "category": "general",
            "tags": ["unicode", "中文", "русский"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["content"] == payload["content"]
    
    def test_create_note_with_invalid_title_too_short(self):
        """Test creating a note with title too short"""
        payload = {
            "title": "Hi",  # Too short (min 3 chars)
            "content": "Valid content",
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_note_with_invalid_title_too_long(self):
        """Test creating a note with title too long"""
        payload = {
            "title": "A" * 101,  # Too long (max 100 chars)
            "content": "Valid content",
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_note_with_invalid_content_too_long(self):
        """Test creating a note with content too long"""
        payload = {
            "title": "Valid Title",
            "content": "A" * 10001,  # Too long (max 10000 chars)
            "category": "work",
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_note_with_invalid_category_too_short(self):
        """Test creating a note with category too short"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "a",  # Too short (min 2 chars)
            "tags": []
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_note_with_too_many_tags(self):
        """Test creating a note with too many tags"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "work",
            "tags": [f"tag{i}" for i in range(11)]  # 11 tags (max 10)
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_note_with_whitespace_stripping(self):
        """Test that whitespace is stripped from string fields"""
        payload = {
            "title": "  Valid Title  ",
            "content": "  Valid content  ",
            "category": "work",
            "tags": [" tag1 ", " tag2 "]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Valid Title"  # Whitespace stripped
        assert data["content"] == "Valid content"  # Whitespace stripped
        assert data["tags"] == ["tag1", "tag2"]  # Whitespace stripped from tags
    
    def test_create_work_note_with_work_tag_passing(self):
        """Test creating a work note with work tag (should pass)"""
        payload = {
            "title": "Work Meeting",
            "content": "Discuss project timeline",
            "category": "work",
            "tags": ["work", "meeting"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_create_work_note_without_work_tag_failing(self):
        """Test creating a work note without work tag (should fail)"""
        payload = {
            "title": "Work Meeting",
            "content": "Discuss project timeline",
            "category": "work",
            "tags": ["meeting", "urgent"]  # Missing "work" tag
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_create_non_work_note_without_work_tag_passing(self):
        """Test creating a non-work note without work tag (should pass)"""
        payload = {
            "title": "Personal Note",
            "content": "Remember to buy groceries",
            "category": "personal",
            "tags": ["shopping", "reminder"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


# ============================================================================
# LIST/GET NOTES TESTS
# ============================================================================

class TestListNotes:
    """Test GET /notes endpoint with various filters"""
    
    def test_list_empty_notes(self):
        """Test listing notes when database is empty"""
        response = requests.get(f"{BASE_URL}/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_list_all_notes(self):
        """Test listing all created notes"""
        # Create test notes
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
        """Test filtering notes by category"""
        # Create notes with different categories
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
        """Test searching notes by title or content"""
        notes = [
            {"title": "Python Tutorial", "content": "Learn Python basics", "category": "Learn", "tags": []},
            {"title": "JavaScript Guide", "content": "Python vs JavaScript", "category": "Learn", "tags": []},
            {"title": "Database Tips", "content": "Use SQLite for small projects", "category": "Tech", "tags": []},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Search for "Python" - should find 2 notes
        response = requests.get(f"{BASE_URL}/notes?search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Search for "SQLite" - should find 1 note
        response = requests.get(f"{BASE_URL}/notes?search=SQLite")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_list_notes_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        note = {"title": "Python Guide", "content": "Content", "category": "Tech", "tags": []}
        requests.post(f"{BASE_URL}/notes", json=note)
        
        # Search with different cases
        for search_term in ["python", "PYTHON", "Python", "pYtHoN"]:
            response = requests.get(f"{BASE_URL}/notes?search={search_term}")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
    
    def test_list_notes_filter_by_tag(self):
        """Test filtering notes by tag"""
        notes = [
            {"title": "Note 1", "content": "Content 1", "category": "Work", "tags": ["urgent", "work"]},
            {"title": "Note 2", "content": "Content 2", "category": "Work", "tags": ["urgent"]},
            {"title": "Note 3", "content": "Content 3", "category": "Personal", "tags": ["personal"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Filter by tag "urgent" - should find 2 notes
        response = requests.get(f"{BASE_URL}/notes?tag=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("urgent" in note["tags"] for note in data)
    
    def test_list_notes_filter_by_tag_case_insensitive(self):
        """Test that tag filtering is case-insensitive"""
        note = {"title": "Test", "content": "Content", "category": "Work", "tags": ["URGENT"]}
        requests.post(f"{BASE_URL}/notes", json=note)
        
        # Search with different cases
        response = requests.get(f"{BASE_URL}/notes?tag=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_list_notes_combined_filters(self):
        """Test combining multiple filters"""
        notes = [
            {"title": "Python Work", "content": "Work with Python", "category": "Work", "tags": ["python"]},
            {"title": "Python Personal", "content": "Python hobby", "category": "Personal", "tags": ["python"]},
            {"title": "Work Notes", "content": "Other work", "category": "Work", "tags": ["notes"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Filter by category AND search
        response = requests.get(f"{BASE_URL}/notes?category=Work&search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Python Work"


# ============================================================================
# GET SINGLE NOTE TESTS
# ============================================================================

class TestGetSingleNote:
    """Test GET /notes/{note_id} endpoint"""
    
    def test_get_existing_note(self):
        """Test retrieving an existing note by ID"""
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
        """Test retrieving a note that doesn't exist"""
        response = requests.get(f"{BASE_URL}/notes/9999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_get_note_with_multiple_tags(self):
        """Test retrieving a note with multiple tags"""
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
# UPDATE NOTE TESTS (PUT)
# ============================================================================

class TestUpdateNote:
    """Test PUT /notes/{note_id} endpoint"""
    
    def test_update_all_fields(self):
        """Test updating all fields of a note"""
        # Create note
        payload = {
            "title": "Original Title",
            "content": "Original content",
            "category": "Original",
            "tags": ["old"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Update all fields
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
        """Test updating only the title"""
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "Cat",
            "tags": []
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Update - must provide all required fields for PUT
        update_payload = {
            "title": "New Title",
            "content": "Content",  # Keep same
            "category": "Cat",      # Keep same
            "tags": []
        }
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
    
    def test_update_nonexistent_note(self):
        """Test updating a note that doesn't exist"""
        update_payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": []
        }
        response = requests.put(f"{BASE_URL}/notes/9999", json=update_payload)
        assert response.status_code == 404
    
    def test_update_tags(self):
        """Test updating tags"""
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
# PARTIAL UPDATE NOTE TESTS (PATCH)
# ============================================================================

class TestPatchNote:
    """Test PATCH /notes/{note_id} endpoint"""
    
    def test_patch_title_only(self):
        """Test patching only the title"""
        payload = {
            "title": "Original",
            "content": "Original content",
            "category": "Original",
            "tags": ["original"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        original_created_at = create_response.json()["created_at"]
        
        # Patch only title
        patch_payload = {"title": "Patched Title"}
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
        assert data["content"] == "Original content"  # Unchanged
        assert data["category"] == "Original"          # Unchanged
        assert data["tags"] == ["original"]            # Unchanged
    
    def test_patch_content_only(self):
        """Test patching only the content"""
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
        assert data["title"] == "Title"           # Unchanged
        assert data["content"] == "New content"
        assert data["category"] == "Cat"          # Unchanged
    
    def test_patch_tags_only(self):
        """Test patching only the tags"""
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
        assert data["title"] == "Title"      # Unchanged
        assert data["content"] == "Content"  # Unchanged
    
    def test_patch_multiple_fields(self):
        """Test patching multiple fields at once"""
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
        assert data["content"] == "Original"  # Unchanged
        assert data["category"] == "Original" # Unchanged
    
    def test_patch_empty_payload(self):
        """Test patching with empty payload (no changes)"""
        payload = {
            "title": "Title",
            "content": "Content",
            "category": "Cat",
            "tags": ["tag"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        original_data = create_response.json()
        
        # Patch with empty dict
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
        assert response.status_code == 200
        data = response.json()
        # All fields should remain unchanged
        assert data["title"] == original_data["title"]
        assert data["content"] == original_data["content"]
        assert data["category"] == original_data["category"]
    
    def test_patch_nonexistent_note(self):
        """Test patching a note that doesn't exist"""
        response = requests.patch(f"{BASE_URL}/notes/9999", json={"title": "New"})
        assert response.status_code == 404


# ============================================================================
# DELETE NOTE TESTS
# ============================================================================

class TestDeleteNote:
    """Test DELETE /notes/{note_id} endpoint"""
    
    def test_delete_existing_note(self):
        """Test deleting an existing note"""
        payload = {
            "title": "To Delete",
            "content": "Content",
            "category": "Cat",
            "tags": ["delete"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Verify note exists
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 200
        
        # Delete note
        response = requests.delete(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 204 or response.status_code == 200
        
        # Verify note is gone
        response = requests.get(f"{BASE_URL}/notes/{note_id}")
        assert response.status_code == 404
    
    def test_delete_nonexistent_note(self):
        """Test deleting a note that doesn't exist"""
        response = requests.delete(f"{BASE_URL}/notes/9999")
        assert response.status_code == 404
    
    def test_delete_note_removes_from_list(self):
        """Test that deleted note is removed from list"""
        # Create 3 notes
        for i in range(3):
            payload = {
                "title": f"Note {i}",
                "content": "Content",
                "category": "Cat",
                "tags": []
            }
            requests.post(f"{BASE_URL}/notes", json=payload)
        
        # List all notes - should be 3
        response = requests.get(f"{BASE_URL}/notes")
        notes = response.json()
        note_id_to_delete = notes[0]["id"]
        
        # Delete first note
        requests.delete(f"{BASE_URL}/notes/{note_id_to_delete}")
        
        # List again - should be 2
        response = requests.get(f"{BASE_URL}/notes")
        notes = response.json()
        assert len(notes) == 2
        assert all(note["id"] != note_id_to_delete for note in notes)


# ============================================================================
# STATISTICS TESTS
# ============================================================================

class TestNotesStats:
    """Test GET /notes/stats endpoint"""
    
    def test_stats_empty_database(self):
        """Test stats when database is empty"""
        response = requests.get(f"{BASE_URL}/notes/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_notes"] == 0
        assert data["by_category"] == {}
        assert data["top_tags"] == []
        assert data["unique_tags_count"] == 0
    
    def test_stats_single_note(self):
        """Test stats with one note"""
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
        """Test stats with multiple notes and categories"""
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
        """Test that tags are counted correctly"""
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
        
        # Find tag counts
        tag_dict = {tag["tag"]: tag["count"] for tag in data["top_tags"]}
        assert tag_dict["python"] == 2
        assert tag_dict["code"] == 2
        assert tag_dict["tutorial"] == 1
        assert tag_dict["javascript"] == 1


# ============================================================================
# TAGS ENDPOINTS TESTS
# ============================================================================

class TestTagsEndpoints:
    """Test /tags endpoints"""
    
    def test_list_tags_returns_list(self):
        """Test that listing tags returns a list"""
        response = requests.get(f"{BASE_URL}/tags")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Tags are sorted
        assert data == sorted(data)
    
    def test_list_tags_with_created_notes(self):
        """Test listing tags after creating notes with tags"""
        notes = [
            {"title": "N1", "content": "C", "category": "Cat", "tags": ["zebra", "apple", "mango"]},
            {"title": "N2", "content": "C", "category": "Cat", "tags": ["banana"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/tags")
        assert response.status_code == 200
        data = response.json()
        # Our new tags should be in the list
        assert "zebra" in data
        assert "apple" in data
        assert "mango" in data
        assert "banana" in data
        # Verify it's sorted
        assert data == sorted(data)
    
    def test_get_notes_by_tag(self):
        """Test GET /tags/{tag_name}/notes"""
        notes = [
            {"title": "Python 1", "content": "Content", "category": "school", "tags": ["python", "programming"]},
            {"title": "Python 2", "content": "Content", "category": "school", "tags": ["python"]},
            {"title": "JavaScript", "content": "Content", "category": "school", "tags": ["javascript", "programming"]},
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        # Get notes with "python" tag
        response = requests.get(f"{BASE_URL}/tags/python/notes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("python" in note["tags"] for note in data)
    
    def test_get_notes_by_nonexistent_tag(self):
        """Test getting notes by a tag that doesn't exist"""
        response = requests.get(f"{BASE_URL}/tags/nonexistent_unique_tag_xyz/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []


# ============================================================================
# CATEGORIES ENDPOINTS TESTS
# ============================================================================

class TestCategoriesEndpoints:
    """Test /categories endpoints"""
    
    def test_list_categories_empty(self):
        """Test listing categories when database is empty"""
        response = requests.get(f"{BASE_URL}/categories")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_list_categories_sorted(self):
        """Test that categories are returned sorted"""
        notes = [
            {"title": "N1", "content": "C", "category": "work", "tags": ["work"]},
            {"title": "N2", "content": "C", "category": "personal", "tags": []},
            {"title": "N3", "content": "C", "category": "school", "tags": []},
            {"title": "N4", "content": "C", "category": "personal", "tags": []},  # Duplicate category
        ]
        
        for note in notes:
            requests.post(f"{BASE_URL}/notes", json=note)
        
        response = requests.get(f"{BASE_URL}/categories")
        assert response.status_code == 200
        data = response.json()
        # Should be unique and sorted
        assert data == ["personal", "school", "work"]
    
    def test_get_notes_by_category_endpoint(self):
        """Test GET /categories/{category_name}/notes"""
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
        """Test getting notes by a category that doesn't exist"""
        response = requests.get(f"{BASE_URL}/categories/NonExistent/notes")
        assert response.status_code == 200
        data = response.json()
        assert data == []