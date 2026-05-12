import streamlit as st
import requests

URL = "https://naas.isalman.dev/no"

def request_no():
    response = requests.get(URL)
    response_json = response.json()
    return response_json["reason"]

# Initialization
if 'text1' not in st.session_state:
    st.session_state['text1'] = request_no()
    print("init Text1")

if 'text' not in st.session_state:
    st.session_state['text'] = request_no()
    print("init Text")


name = st.text_input('Name', placeholder="Hier Name eingeben...")
st.write(name)


if st.button("Neuer Text1"):
    st.session_state['text1'] = request_no()

st.write(st.session_state["text1"])


if st.button("Neuer Text"):
    st.session_state['text'] = request_no()

st.write(st.session_state["text"])


with st.expander('session state'):
    st.write(st.session_state)

API_BASE_URL = "http://localhost:8000"
    
st.title("Notes API Frontend")

# Function to fetch all notes
def get_all_notes():
    try:
        response = requests.get(f"{API_BASE_URL}/notes")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching notes: {e}")
        return []

# Function to create a new note
def create_note(title, content, category, tags):
    note_data = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags if tags else []
    }
    try:
        response = requests.post(f"{API_BASE_URL}/notes", json=note_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating note: {e}")
        return None

# Initialize session state for notes cache
if 'notes' not in st.session_state:
    st.session_state.notes = []

# Function 1: Show all notes
st.header("All Notes")

# Button to refresh notes
if st.button("Refresh Notes"):
    st.session_state.notes = get_all_notes()
    st.rerun()

# Display notes if available
if st.session_state.notes:
    # Create a selectbox for note titles
    note_titles = [note['title'] for note in st.session_state.notes]
    selected_title = st.selectbox("Select a note to view details:", note_titles)

    # Find the selected note
    selected_note = next((note for note in st.session_state.notes if note['title'] == selected_title), None)

    if selected_note:
        st.subheader(f"Note: {selected_note['title']}")
        st.write(f"**Content:** {selected_note['content']}")
        st.write(f"**Category:** {selected_note['category']}")
        st.write(f"**Tags:** {', '.join(selected_note['tags']) if selected_note['tags'] else 'None'}")
        st.write(f"**Created At:** {selected_note['created_at']}")
else:
    st.write("No notes available. Click 'Refresh Notes' to load them.")

# Function 2: Create a new note
st.header("Create New Note")

with st.form("create_note_form"):
    title = st.text_input("Title", max_chars=100)
    content = st.text_area("Content", max_chars=10000)
    category = st.text_input("Category", max_chars=30)
    tags_input = st.text_input("Tags (comma-separated)", placeholder="tag1, tag2, tag3")

    submitted = st.form_submit_button("Create Note")

    if submitted:
        if not title or not content or not category:
            st.error("Title, Content, and Category are required!")
        else:
            # Parse tags
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

            # Create the note
            new_note = create_note(title, content, category, tags)
            if new_note:
                st.success(f"Note '{new_note['title']}' created successfully!")

                # Refresh the notes list to include the new note
                st.session_state.notes = get_all_notes()
                st.rerun()