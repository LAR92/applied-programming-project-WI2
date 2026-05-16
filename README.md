# Applied Programming Project WI2 – Notes API

Eine Python-basierte Notes-App mit **FastAPI**, **SQLModel**, **SQLite**, **Pydantic**, **Pytest** und einem einfachen **Streamlit-Frontend**. Das Projekt wurde im Rahmen des Moduls **Applied Programming** entwickelt und demonstriert grundlegende Konzepte moderner Softwareentwicklung: REST-APIs, Datenvalidierung, Datenbankanbindung, CRUD-Operationen, Testing und Frontend-Integration.

---

## Überblick

Dieses Projekt stellt eine kleine Notes API bereit. Benutzerinnen und Benutzer können Notizen erstellen, anzeigen, filtern, aktualisieren und löschen. Jede Notiz besitzt einen Titel, einen Inhalt, eine Kategorie, ein Erstellungsdatum und optional mehrere Tags.

Die Anwendung besteht aus zwei Teilen:

1. einem **FastAPI-Backend** mit SQLite-Datenbank
2. einem einfachen **Streamlit-Frontend** zur Anzeige und Erstellung von Notizen

Die API speichert Notizen dauerhaft in einer lokalen SQLite-Datenbank. Tags werden als eigene Entitäten modelliert und über eine Many-to-Many-Beziehung mit Notizen verknüpft.

---

## Features

* REST API mit FastAPI
* SQLite-Datenbank mit SQLModel
* CRUD-Funktionalität für Notizen
* Tags mit Many-to-Many-Beziehung
* Kategorien für Notizen
* Filterung nach Kategorie, Tag, Suchbegriff und Erstellungsdatum
* Statistik-Endpunkt für Notizen, Kategorien und Tags
* Eingabevalidierung mit Pydantic
* Vollständige Aktualisierung über `PUT`
* Teilweise Aktualisierung über `PATCH`
* Fehlerbehandlung mit passenden HTTP-Statuscodes
* Automatische API-Dokumentation über Swagger UI
* Einfaches Streamlit-Frontend
* Automatisierte Tests mit Pytest

---

## Verwendete Technologien

| Technologie | Zweck                                            |
| ----------- | ------------------------------------------------ |
| Python      | Programmiersprache                               |
| FastAPI     | Backend und REST API                             |
| Pydantic    | Validierung von Eingabe- und Ausgabedaten        |
| SQLModel    | ORM und Datenbankmodellierung                    |
| SQLite      | Lokale relationale Datenbank                     |
| Streamlit   | Einfaches Frontend                               |
| Requests    | HTTP-Kommunikation zwischen Frontend und Backend |
| Pytest      | Automatisierte Tests                             |
| uv          | Paket- und Projektverwaltung                     |

---

## Projektstruktur

```text
applied-programming-project-WI2/
├── data/
│   └── notes.json              # Legacy-/JSON-Datei aus früheren Entwicklungsständen
├── exploration/                # Übungen, Experimente und Zwischenschritte
├── .gitignore
├── .python-version
├── README.md
├── frontend.py                 # Streamlit-Frontend
├── main.py                     # FastAPI-App, Datenmodelle und API-Endpunkte
├── notes.db                    # Lokale SQLite-Datenbank
├── pyproject.toml              # Projektkonfiguration und Abhängigkeiten
├── test_main.py                # Pytest-Tests für die API
├── uv.lock                     # Lockfile für reproduzierbare Installation
└── work-log.md                 # Dokumentation des Lern- und Entwicklungsprozesses
```

---

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/LAR92/applied-programming-project-WI2.git
cd applied-programming-project-WI2
```

### 2. Abhängigkeiten installieren

Empfohlen mit `uv`:

```bash
uv sync
```

Falls `uv` nicht verwendet wird, können die wichtigsten Abhängigkeiten alternativ mit `pip` installiert werden:

```bash
pip install "fastapi[standard]" sqlmodel streamlit requests pytest faker icecream
```

---

## Backend starten

Das FastAPI-Backend wird mit folgendem Befehl gestartet:

```bash
uv run fastapi dev main.py
```

Alternativ:

```bash
fastapi dev main.py
```

Nach dem Start ist die API standardmäßig hier erreichbar:

```text
http://127.0.0.1:8000
```

Die automatisch generierte API-Dokumentation befindet sich unter:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend starten

Das Streamlit-Frontend kann in einem zweiten Terminal gestartet werden:

```bash
uv run streamlit run frontend.py
```

Alternativ:

```bash
streamlit run frontend.py
```

Das Frontend greift lokal auf das Backend unter folgender Adresse zu:

```text
http://localhost:8000
```

Wichtig: Das Backend muss laufen, bevor das Frontend sinnvoll verwendet werden kann.

---

## API-Endpunkte

### Allgemeine Endpunkte

| Methode | Pfad                  | Beschreibung                               |
| ------- | --------------------- | ------------------------------------------ |
| `GET`   | `/`                   | Gibt eine einfache Begrüßung zurück        |
| `GET`   | `/name/{name}`        | Gibt eine personalisierte Begrüßung zurück |
| `GET`   | `/calculate/{number}` | Führt eine einfache Beispielrechnung aus   |

### Notes-Endpunkte

| Methode  | Pfad                         | Beschreibung                                            |
| -------- | ---------------------------- | ------------------------------------------------------- |
| `POST`   | `/notes`                     | Erstellt eine neue Notiz                                |
| `GET`    | `/notes`                     | Gibt alle Notizen zurück; unterstützt Filter            |
| `GET`    | `/notes/{note_id}`           | Gibt eine einzelne Notiz anhand ihrer ID zurück         |
| `PUT`    | `/notes/{note_id}`           | Aktualisiert eine komplette Notiz                       |
| `PATCH`  | `/notes/{note_id}`           | Aktualisiert einzelne Felder einer Notiz                |
| `DELETE` | `/notes/{note_id}`           | Löscht eine Notiz                                       |
| `GET`    | `/notes/stats`               | Gibt Statistiken zu Notizen, Kategorien und Tags zurück |
| `GET`    | `/notes/category/{category}` | Gibt Notizen einer bestimmten Kategorie zurück          |

### Tag- und Kategorie-Endpunkte

| Methode | Pfad                                | Beschreibung                                        |
| ------- | ----------------------------------- | --------------------------------------------------- |
| `GET`   | `/tags`                             | Gibt alle vorhandenen Tags zurück                   |
| `GET`   | `/tags/{tag_name}/notes`            | Gibt alle Notizen mit einem bestimmten Tag zurück   |
| `GET`   | `/categories`                       | Gibt alle vorhandenen Kategorien zurück             |
| `GET`   | `/categories/{category_name}/notes` | Gibt alle Notizen einer bestimmten Kategorie zurück |

---

## Filtermöglichkeiten

Der Endpunkt `GET /notes` unterstützt folgende optionale Query-Parameter:

| Parameter        | Beschreibung                                                                 |
| ---------------- | ---------------------------------------------------------------------------- |
| `category`       | Filtert Notizen nach Kategorie                                               |
| `search`         | Sucht im Titel und Inhalt einer Notiz                                        |
| `tag`            | Filtert Notizen nach Tag                                                     |
| `created_after`  | Gibt nur Notizen zurück, die nach einem bestimmten Zeitpunkt erstellt wurden |
| `created_before` | Gibt nur Notizen zurück, die vor einem bestimmten Zeitpunkt erstellt wurden  |

Beispiel:

```text
GET /notes?category=study&tag=python&search=api
```

---

## Beispiel-Requests

### Neue Notiz erstellen

```bash
curl -X POST "http://127.0.0.1:8000/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI lernen",
    "content": "Heute habe ich REST-Endpunkte mit FastAPI erstellt.",
    "category": "study",
    "tags": ["python", "api", "fastapi"]
  }'
```

### Alle Notizen abrufen

```bash
curl "http://127.0.0.1:8000/notes"
```

### Einzelne Notiz abrufen

```bash
curl "http://127.0.0.1:8000/notes/1"
```

### Notiz vollständig aktualisieren

```bash
curl -X PUT "http://127.0.0.1:8000/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI vertiefen",
    "content": "Diese Notiz wurde vollständig aktualisiert.",
    "category": "study",
    "tags": ["python", "backend"]
  }'
```

### Notiz teilweise aktualisieren

```bash
curl -X PATCH "http://127.0.0.1:8000/notes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Nur der Inhalt wurde geändert."
  }'
```

### Notiz löschen

```bash
curl -X DELETE "http://127.0.0.1:8000/notes/1"
```

### Statistiken abrufen

```bash
curl "http://127.0.0.1:8000/notes/stats"
```

---

## Datenmodell

### Note

Eine Notiz besteht aus folgenden Feldern:

| Feld         | Typ            | Beschreibung             |
| ------------ | -------------- | ------------------------ |
| `id`         | Integer        | Eindeutige ID der Notiz  |
| `title`      | String         | Titel der Notiz          |
| `content`    | String         | Inhalt der Notiz         |
| `category`   | String         | Kategorie der Notiz      |
| `created_at` | DateTime       | Zeitpunkt der Erstellung |
| `tags`       | Liste von Tags | Zugeordnete Tags         |

### Tag

Ein Tag besteht aus folgenden Feldern:

| Feld   | Typ     | Beschreibung           |
| ------ | ------- | ---------------------- |
| `id`   | Integer | Eindeutige ID des Tags |
| `name` | String  | Name des Tags          |

Zwischen `Note` und `Tag` besteht eine **Many-to-Many-Beziehung**. Eine Notiz kann mehrere Tags besitzen. Gleichzeitig kann ein Tag mehreren Notizen zugeordnet sein.

---

## Validierung

Die API validiert Eingaben über Pydantic. Dadurch werden fehlerhafte oder unvollständige Daten frühzeitig abgefangen.

Wichtige Validierungsregeln:

* `title` muss zwischen 3 und 100 Zeichen lang sein.
* `content` muss zwischen 1 und 10.000 Zeichen lang sein.
* `category` muss zwischen 2 und 30 Zeichen lang sein.
* Pro Notiz sind maximal 10 Tags erlaubt.
* Tags müssen Strings sein.
* Tags werden automatisch normalisiert.
* Tags werden in Kleinbuchstaben umgewandelt.
* Tags dürfen nur Kleinbuchstaben, Zahlen und Bindestriche enthalten.
* Doppelte Tags werden entfernt.
* Nicht erlaubte zusätzliche Felder werden abgelehnt.
* Beim `PATCH`-Endpunkt werden nur die übergebenen Felder aktualisiert.

Zusätzlich enthält das Projekt eine Cross-Field-Validation: Wenn eine Notiz als Kategorie `work` verwendet und gleichzeitig Tags übergeben werden, muss der Tag `work` enthalten sein.

---

## Tests

Die API wird mit Pytest getestet. Die Testdatei heißt:

```text
test_main.py
```

Alle Tests können mit folgendem Befehl ausgeführt werden:

```bash
uv run pytest
```

Alternativ:

```bash
pytest
```

Nur die API-Tests ausführen:

```bash
pytest test_main.py
```

---

## Streamlit-Frontend

Das Frontend in `frontend.py` bietet eine einfache grafische Oberfläche für die Notes API.

Aktuelle Funktionen:

* Laden aller vorhandenen Notizen
* Auswahl einer Notiz über ein Dropdown-Menü
* Anzeige von Titel, Inhalt, Kategorie, Tags und Erstellungsdatum
* Erstellen neuer Notizen über ein Formular
* Kommunikation mit dem FastAPI-Backend über HTTP-Requests

---

## Entwicklung und Lernfortschritt

Der Entwicklungsprozess ist zusätzlich in `work-log.md` dokumentiert. Dort werden einzelne Arbeitsschritte, Lerninhalte und Fortschritte im Rahmen des Moduls festgehalten.

Im Projekt wurden unter anderem folgende Themen praktisch angewendet:

* Aufbau einer FastAPI-Anwendung
* Definition von API-Endpunkten
* Arbeiten mit Path- und Query-Parametern
* Request- und Response-Modelle mit Pydantic
* Persistenz mit SQLite und SQLModel
* Modellierung relationaler Daten
* Many-to-Many-Beziehungen
* Validierung und Fehlerbehandlung
* PUT, PATCH und DELETE in REST APIs
* Testen mit Pytest
* Aufbau eines einfachen Streamlit-Frontends

---

## Mögliche Erweiterungen

Folgende Erweiterungen wären für eine Weiterentwicklung sinnvoll:

* Bearbeiten und Löschen von Notizen direkt im Streamlit-Frontend
* Such- und Filterfunktionen im Frontend
* Verbesserte Benutzerführung und Fehlermeldungen
* Authentifizierung und Benutzerkonten
* Deployment von Backend und Frontend
* Trennung von Datenbankmodellen, Schemas und Routen in mehrere Dateien
* Erweiterte Testabdeckung
* Exportfunktion für Notizen
* Docker-Unterstützung

---

## Hinweise zur lokalen Datenbank

Die Datei `notes.db` enthält die lokale SQLite-Datenbank. Beim Start der Anwendung werden die benötigten Tabellen automatisch erstellt, falls sie noch nicht existieren.

Für eine frische lokale Datenbank kann die Datei `notes.db` gelöscht werden. Beim nächsten Start der Anwendung wird sie erneut angelegt.

---

## Autor

**Lauritz Jäger**
Studienprojekt im Modul **Applied Programming**

---

## Lizenz

Dieses Projekt wurde zu Lern- und Studienzwecken erstellt.
