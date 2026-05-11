"""
Comprehensive validation tests for Notes API.
Tests Pydantic validation, SQLModel constraints, and business rules.
"""
import pytest
import requests
from typing import Generator

BASE_URL = "http://localhost:8000"


@pytest.fixture
def client() -> Generator:
    """Fixture that provides an HTTP client and cleans up database before/after tests"""
    # Before test: clean up database
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass
    
    yield None  # Client is the requests module itself
    
    # After test: clean up database
    try:
        response = requests.get(f"{BASE_URL}/notes")
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                requests.delete(f"{BASE_URL}/notes/{note['id']}")
    except:
        pass


# ============================================================================
# PYDANTIC FIELD VALIDATION TESTS
# ============================================================================

class TestNoteCreateValidation:
    """Test NoteCreate Pydantic model validation"""
    
    def test_create_note_rejects_short_title(self, client):
        """Test that title < 3 chars is rejected with 422"""
        payload = {
            "title": "ab",  # Too short (min_length=3)
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "title" in str(response.json()).lower()
    
    def test_create_note_rejects_empty_title(self, client):
        """Test that empty title is rejected with 422"""
        payload = {
            "title": "",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_valid_title(self, client):
        """Test that valid titles are accepted"""
        payload = {
            "title": "Valid Title",  # Exactly 3+ chars
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
    
    def test_create_note_rejects_empty_content(self, client):
        """Test that empty content is rejected with 422"""
        payload = {
            "title": "Valid Title",
            "content": "",  # min_length=1
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_short_category(self, client):
        """Test that category < 2 chars is rejected with 422"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "a",  # Too short (min_length=2)
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_valid_category(self, client):
        """Test that valid categories are accepted"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "ab",  # Exactly 2 chars
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


class TestTagValidation:
    """Test tag validation constraints"""
    
    def test_create_note_normalizes_tags(self, client):
        """Test that tags are normalized (lowercased, stripped, deduplicated)"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["  WORK  ", "Meeting", "WORK"]  # Mixed case, whitespace, duplicates
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Should be normalized to lowercase and deduplicated
        assert "work" in data["tags"]
        assert "meeting" in data["tags"]
        assert len([t for t in data["tags"] if t == "work"]) == 1  # No duplicates
    
    def test_create_note_rejects_short_tag(self, client):
        """Test that tags < 2 chars are rejected with 422"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["a"]  # Too short (min_length=2)
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_long_tag(self, client):
        """Test that tags > 30 chars are rejected with 422"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["a" * 31]  # Too long (max_length=30)
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_invalid_chars(self, client):
        """Test that tags with non-alphanumeric (except dashes) are rejected with 422"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag@name"]  # Special char @ not allowed
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_underscore(self, client):
        """Test that tags with underscores are rejected (pattern: ^[a-z0-9-]+$)"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag_name"]  # Underscore not allowed
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_rejects_tag_with_space(self, client):
        """Test that tags with internal spaces are rejected"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag name"]  # Space not allowed
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
    
    def test_create_note_accepts_tag_with_dashes_and_digits(self, client):
        """Test that tags with dashes and digits are accepted"""
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
        """Test that uppercase letters in tags are normalized to lowercase"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["MyTag", "WORK"]  # Uppercase should be converted to lowercase
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        # Should be converted to lowercase
        assert "mytag" in data["tags"]
        assert "work" in data["tags"]
        # Original case should not exist
        assert "MyTag" not in data["tags"]
        assert "WORK" not in data["tags"]


class TestCrossFieldValidation:
    """Test cross-field validation rules"""
    
    def test_work_note_requires_work_tag(self, client):
        """Test that category='work' requires 'work' tag (422 if missing)"""
        payload = {
            "title": "Work Note",
            "content": "Valid content",
            "category": "work",
            "tags": ["meeting"]  # Missing 'work' tag
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "work" in str(response.json()).lower()
    
    def test_work_note_succeeds_with_work_tag(self, client):
        """Test that work notes with 'work' tag are accepted"""
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
        """Test that non-work categories don't require 'work' tag"""
        payload = {
            "title": "Personal Note",
            "content": "Valid content",
            "category": "personal",
            "tags": ["shopping"]  # No 'work' tag, but category is personal
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


class TestExtraFieldsRejection:
    """Test that extra fields are rejected"""
    
    def test_create_note_forbids_extra_fields(self, client):
        """Test that unknown fields are rejected with 422 (extra='forbid')"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"],
            "unknown_field": "should not be here"  # Extra field
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 422
        assert "unknown_field" in str(response.json()).lower() or "extra" in str(response.json()).lower()
    
    def test_create_note_with_valid_fields_only(self, client):
        """Test that only valid fields are accepted"""
        payload = {
            "title": "Valid Title",
            "content": "Valid content",
            "category": "personal",
            "tags": ["tag1"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201


# ============================================================================
# PATCH ENDPOINT TESTS (NoteUpdate Validation)
# ============================================================================

class TestPatchValidation:
    """Test NoteUpdate (PATCH) validation"""
    
    def test_patch_with_empty_body_succeeds(self, client):
        """Test that PATCH with {} succeeds (no changes)"""
        # Create a note first
        payload = {
            "title": "Original",
            "content": "Original content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert create_response.status_code == 201
        note_id = create_response.json()["id"]
        
        # PATCH with empty body
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Original"  # Unchanged
    
    def test_patch_with_invalid_title_fails(self, client):
        """Test that PATCH with invalid title returns 422"""
        # Create a note first
        payload = {
            "title": "Original",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Try to patch with short title
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"title": "ab"})
        assert response.status_code == 422
    
    def test_patch_with_empty_title_fails(self, client):
        """Test that PATCH with empty title returns 422"""
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
        """Test that PATCH with valid title succeeds"""
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
        """Test that PATCH with invalid tags returns 422"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Try to patch with invalid tag (too short)
        response = requests.patch(f"{BASE_URL}/notes/{note_id}", json={"tags": ["a"]})
        assert response.status_code == 422
    
    def test_patch_work_category_requires_work_tag(self, client):
        """Test that PATCH changing category to work requires work tag"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Try to change category to work without work tag
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"category": "work", "tags": ["meeting"]}
        )
        assert response.status_code == 422
    
    def test_patch_work_category_with_work_tag_succeeds(self, client):
        """Test that PATCH changing category to work WITH work tag succeeds"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["meeting"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Change category and tags together
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"category": "work", "tags": ["work", "meeting"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "work"
        assert "work" in data["tags"]
    
    def test_patch_forbids_extra_fields(self, client):
        """Test that PATCH rejects extra fields"""
        payload = {
            "title": "Test",
            "content": "Content",
            "category": "personal",
            "tags": ["tag1"]
        }
        create_response = requests.post(f"{BASE_URL}/notes", json=payload)
        note_id = create_response.json()["id"]
        
        # Try to patch with extra field
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"title": "Updated", "unknown_field": "bad"}
        )
        assert response.status_code == 422


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestValidationIntegration:
    """Integration tests combining multiple validation rules"""
    
    def test_full_valid_note_flow(self, client):
        """Test creating a valid note and updating it"""
        # Create note
        payload = {
            "title": "My Work Task",
            "content": "This is a detailed work task description",
            "category": "work",
            "tags": ["work", "urgent"]
        }
        response = requests.post(f"{BASE_URL}/notes", json=payload)
        assert response.status_code == 201
        note_id = response.json()["id"]
        
        # Update note
        response = requests.patch(
            f"{BASE_URL}/notes/{note_id}",
            json={"tags": ["work", "completed"]}
        )
        assert response.status_code == 200
    
    def test_comprehensive_validation_chain(self, client):
        """Test multiple validation rules in sequence"""
        # Invalid: empty title
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "", "content": "C", "category": "pc", "tags": ["t1"]}
        ).status_code == 422
        
        # Invalid: short category
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "p", "tags": ["t1"]}
        ).status_code == 422
        
        # Invalid: work note without work tag
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "work", "tags": ["meeting"]}
        ).status_code == 422
        
        # Valid: all constraints satisfied
        assert requests.post(
            f"{BASE_URL}/notes",
            json={"title": "Tit", "content": "C", "category": "work", "tags": ["work"]}
        ).status_code == 201
