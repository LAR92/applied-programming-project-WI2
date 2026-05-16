import requests

URL ="http://127.0.0.1:8000"

def test_get_root():
    response = requests.get(f"{URL}/")
    if response.status_code == 200:
        print("GET / war erfolgreich")
    else:
        print("GET / ist fehlgeschlagen")
    
if __name__ == "__main__":
    test_get_root()

def test_post_creation():
    payload = {
        "title": "Test Note",
        "content": "This is a test note.",
        "category": "Test",
        "tags": ["/tag1", "/tag2"]
    }
    response = requests.post(f"{URL}/notes", json=payload)
    if response.status_code == 201:
        print("POST /notes war erfolgreich")
    else:
        print("POST /notes ist fehlgeschlagen")

# Hier koennte man danach noch response.json()["title"] pruefen.
