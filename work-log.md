# Work Log

**Student Name:** Lauritz Jäger

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

Heute habe ich mich mit den Grundlagen des Moduls und der Vorbereitung meiner Entwicklungsumgebung beschäftigt. Dazu gehörte zunächst, das Projekt-Repository einzurichten, die benötigten Tools zu installieren und mich mit der Struktur eines Python-Projekts vertraut zu machen. Ich habe gelernt, wie wichtig eine funktionierende Entwicklungsumgebung ist, bevor man mit der eigentlichen Implementierung beginnt.

Außerdem habe ich erste einfache Funktionen und Endpunkte ausprobiert. Dazu gehörten grundlegende FastAPI-Funktionen wie ein Root-Endpunkt und einfache Parameter-Endpunkte, zum Beispiel zur Ausgabe einer Begrüßung oder zur Verarbeitung eines Zahlenwertes. Dadurch konnte ich nachvollziehen, wie eine API aufgebaut ist, wie Requests an das Backend gesendet werden und wie eine Response im JSON-Format zurückgegeben wird.

Ein weiterer wichtiger Punkt war der Umgang mit Git und GitHub. Ich habe begonnen, meine Änderungen regelmäßig im Repository zu sichern. Dadurch konnte ich erste praktische Erfahrungen mit Versionskontrolle sammeln und verstehen, warum Commits für die Nachvollziehbarkeit eines Projekts wichtig sind.

#### 2. 🚧 What challenges did I face?

Zu Beginn hatte ich Schwierigkeiten mit der Einrichtung der Entwicklungsumgebung. Besonders problematisch war, dass mein macOS-System veraltet war und dadurch bestimmte Installationen oder Befehle nicht wie erwartet funktioniert haben. Dadurch konnten benötigte Komponenten zunächst nicht korrekt installiert werden.

Außerdem war es am Anfang ungewohnt, mehrere Werkzeuge gleichzeitig zu verwenden. Ich musste mich mit Python, dem Terminal, GitHub, dem Code-Editor und der Projektstruktur beschäftigen. Dadurch war es teilweise schwierig zu erkennen, ob ein Fehler aus dem Code, aus der Installation oder aus der Umgebung kam.

Auch das Verständnis von FastAPI war anfangs neu für mich. Besonders die Frage, wie Endpunkte definiert werden und wie Daten zwischen Client und Server ausgetauscht werden, musste ich erst Schritt für Schritt verstehen.

#### 3. 💡 How did I overcome them?

Ich habe zunächst mein macOS-System aktualisiert und anschließend die Installation erneut durchgeführt. Dadurch konnten die benötigten Pakete und Abhängigkeiten korrekt eingerichtet werden. Zusätzlich habe ich mit Kommilitonen zusammengearbeitet, um Installationsprobleme gemeinsam zu analysieren.

Bei Problemen mit der Projektstruktur und den Befehlen habe ich Schritt für Schritt getestet, welche Teile bereits funktionieren. Dadurch konnte ich Fehler besser eingrenzen. Außerdem habe ich Dokumentationen und KI-Unterstützung genutzt, um die Grundlagen von FastAPI und Git besser zu verstehen.

Am Ende konnte ich die Entwicklungsumgebung erfolgreich einrichten und erste einfache API-Endpunkte ausführen. Dadurch hatte ich eine stabile Grundlage für die weiteren Projekttage.

---

### Day 2

#### 1. ✅ What did I accomplish?

Heute habe ich mit der eigentlichen NotesAPI begonnen und ein erstes Notiz-Management-System entwickelt. Dabei ging es darum, Notizen nicht nur als einfache Daten zu betrachten, sondern sie strukturiert mit Eigenschaften wie Titel, Inhalt, Kategorie, Tags und Erstellungsdatum zu verwalten.

Ich habe gelernt, wie man Eingabemodelle und Ausgabemodelle mit Pydantic erstellt. Dadurch konnte ich festlegen, welche Daten eine neue Notiz enthalten muss und in welcher Form die API eine Notiz wieder zurückgeben soll. Besonders wichtig war dabei, dass Daten nicht ungeprüft übernommen werden, sondern über Felder wie `title`, `content`, `category` und `tags` strukturiert verarbeitet werden.

Außerdem habe ich erste Endpunkte zum Erstellen und Anzeigen von Notizen umgesetzt. Dabei konnte ich praktisch nachvollziehen, wie ein POST-Request zum Anlegen einer Notiz funktioniert und wie ein GET-Request verwendet wird, um gespeicherte Notizen wieder abzurufen. Zusätzlich habe ich mich mit der Speicherung von Daten beschäftigt und gesehen, wie Daten dauerhaft abgelegt und später erneut geladen werden können.

#### 2. 🚧 What challenges did I face?

Während der Entwicklung traten verschiedene Fehler auf, besonders bei der Verarbeitung und Anzeige von Notizen. Teilweise wurden Daten nicht korrekt geladen oder nicht in der erwarteten Struktur zurückgegeben. Dadurch kam es zu Fehlermeldungen in der Benutzeroberfläche beziehungsweise beim Testen der API.

Eine Herausforderung war auch, die richtige Datenstruktur für Notizen zu finden. Am Anfang war nicht immer klar, welche Felder verpflichtend sein sollten und wie optionale Informationen wie Tags am besten verarbeitet werden. Besonders bei Listen wie Tags musste ich darauf achten, dass die Eingaben später gut weiterverarbeitet werden können.

Zusätzlich war es ungewohnt, zwischen API-Logik, Datenmodell und Response-Struktur zu unterscheiden. Ich musste erst verstehen, dass ein internes Datenmodell nicht immer exakt gleich aussehen muss wie das Modell, das über die API zurückgegeben wird.

#### 3. 💡 How did I overcome them?

Ich habe den Code schrittweise analysiert und einzelne Funktionen separat getestet. Dadurch konnte ich besser erkennen, ob ein Fehler beim Erstellen, Speichern oder Abrufen der Notizen entsteht. Besonders hilfreich war es, Fehlermeldungen genau zu lesen und die API-Antworten zu überprüfen.

Außerdem habe ich die Datenmodelle klarer strukturiert und darauf geachtet, dass die Eingaben über Pydantic validiert werden. Dadurch wurde die Anwendung stabiler und Fehler konnten früher abgefangen werden.

Durch Debugging, mehrfaches Testen und Vergleichen der erwarteten mit der tatsächlichen Ausgabe konnte ich die Probleme beheben. Dabei habe ich gelernt, wie wichtig saubere Datenstrukturen und verständliche API-Responses für ein Backend-Projekt sind.

---

### Day 3

#### 1. ✅ What did I accomplish?

Heute habe ich die NotesAPI um weitere wichtige Funktionen erweitert. Besonders im Mittelpunkt standen Tags, Kategorien sowie neue Endpunkte zum Aktualisieren und Löschen von Notizen. Dadurch wurde die API deutlich vollständiger, weil Notizen nicht mehr nur erstellt und angezeigt, sondern auch verändert und entfernt werden konnten.

Ich habe PUT- und DELETE-Endpunkte implementiert. Mit dem PUT-Endpunkt können bestehende Notizen vollständig aktualisiert werden, während der DELETE-Endpunkt dazu dient, eine Notiz anhand ihrer ID zu löschen. Dadurch habe ich ein besseres Verständnis für die typischen CRUD-Operationen bekommen: Create, Read, Update und Delete.

Außerdem habe ich mich intensiver mit Tags und Kategorien beschäftigt. Ich habe gelernt, wie Notizen gefiltert werden können und wie man zusätzliche Endpunkte erstellt, um zum Beispiel alle Notizen einer Kategorie oder alle Notizen mit einem bestimmten Tag abzurufen. Dadurch wurde die API praxisnäher, weil Nutzer Notizen nicht nur speichern, sondern auch sinnvoll organisieren können.

#### 2. 🚧 What challenges did I face?

Während der Entwicklung traten mehrere Fehler auf, darunter auch Internal Server Errors mit dem HTTP-Statuscode 500. Diese Fehler waren besonders schwierig, weil sie zunächst nur gezeigt haben, dass im Backend etwas schiefgelaufen ist, aber nicht sofort klar war, an welcher Stelle das Problem liegt.

Ein Problem war die korrekte Verarbeitung von IDs. Wenn eine Notiz nicht existierte oder eine ID falsch übergeben wurde, musste die API sinnvoll reagieren. Dabei war es wichtig, passende HTTP-Fehler wie 404 für nicht gefundene Notizen oder 422 für ungültige Eingaben zu verwenden.

Außerdem war die Arbeit mit Tags komplexer als erwartet. Tags mussten richtig normalisiert, gespeichert und später wieder mit den Notizen verknüpft werden. Dabei konnten Fehler entstehen, wenn Tags doppelt vorkamen oder nicht im erwarteten Format eingegeben wurden.

#### 3. 💡 How did I overcome them?

Ich habe die betroffenen Endpunkte einzeln getestet und die Fehlermeldungen genau analysiert. Dabei habe ich überprüft, ob die Daten korrekt ankommen, ob die Notiz in der Datenbank gefunden wird und ob die Response richtig aufgebaut ist.

Zusätzlich habe ich Dokumentationen und KI-Tools genutzt, um besser zu verstehen, wie FastAPI mit HTTPException, Statuscodes und Request-Validierung arbeitet. Anschließend habe ich die problematischen Codebereiche angepasst und erneut getestet.

Durch diese Vorgehensweise konnte ich die Fehler Schritt für Schritt beheben. Ich habe gelernt, dass gute Fehlerbehandlung ein wichtiger Teil einer API ist, weil Nutzer und Entwickler dadurch besser verstehen können, was bei einer Anfrage schiefgelaufen ist.

---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?

Heute habe ich die API weiter ausgebaut und zusätzliche POST- beziehungsweise API-Funktionen ergänzt. Außerdem habe ich begonnen, automatisierte Tests mit Pytest zu verwenden. Dadurch konnte ich überprüfen, ob die wichtigsten Endpunkte der Anwendung korrekt funktionieren.

Ein wichtiger Schwerpunkt war die Datenüberprüfung. Ich habe mich intensiver mit Pydantic-Modellen beschäftigt und festgelegt, welche Eingaben erlaubt sind. Zum Beispiel sollten Titel, Inhalt und Kategorie bestimmte Mindest- und Maximallängen haben. Dadurch wird verhindert, dass unvollständige oder fehlerhafte Daten in die Anwendung gelangen.

Außerdem habe ich erste Testfälle geschrieben beziehungsweise eine Test-Suite ausprobiert. Dabei konnte ich lernen, wie man API-Endpunkte automatisch testet, anstatt jede Funktion manuell im Browser oder über ein anderes Tool zu überprüfen. Das war ein wichtiger Schritt, um die Stabilität der Anwendung besser einschätzen zu können.

#### 2. 🚧 What challenges did I face?

Einige Tests wurden zunächst nicht bestanden. Besonders schwierig war es, die Ursachen der fehlerhaften Testausgaben richtig zu interpretieren. Manchmal lag das Problem nicht direkt im getesteten Endpunkt, sondern in der Datenstruktur, der Validierung oder der erwarteten Response.

Außerdem musste ich verstehen, wie Pytest arbeitet und wie Testfälle aufgebaut sind. Es war zunächst ungewohnt, dass Tests sehr genau prüfen, ob Statuscodes, JSON-Antworten und Fehlermeldungen exakt den Erwartungen entsprechen.

Eine weitere Herausforderung war, dass Änderungen an der API Auswirkungen auf mehrere Tests haben konnten. Wenn zum Beispiel ein Datenmodell angepasst wurde, mussten auch die dazugehörigen Tests zur neuen Struktur passen.

#### 3. 💡 How did I overcome them?

Ich habe die Testausgaben sorgfältig gelesen und versucht, die Fehlermeldungen Schritt für Schritt nachzuvollziehen. Dabei habe ich geprüft, welcher Test fehlschlägt, welche Antwort erwartet wurde und welche Antwort die API tatsächlich geliefert hat.

Durch Google-Recherche, Dokumentationen und KI-Unterstützung konnte ich besser verstehen, wie Pytest und FastAPI-Testfälle funktionieren. Anschließend habe ich die betroffenen Endpunkte und Modelle angepasst.

Ich habe gelernt, dass Tests nicht nur dazu da sind, Fehler zu finden, sondern auch helfen, den eigenen Code besser zu verstehen. Durch die Tests konnte ich genauer erkennen, welche Anforderungen meine API erfüllen muss.

---

### Day 5

#### 1. ✅ What did I accomplish?

Heute habe ich verschiedene Validator-Funktionen implementiert, um Eingaben in der API genauer zu überprüfen. Besonders wichtig war dabei die Validierung von Tags. Tags sollen nicht beliebig gespeichert werden, sondern vor der Speicherung bereinigt und in ein einheitliches Format gebracht werden.

Ich habe gelernt, wie man Eingaben normalisiert, zum Beispiel indem Leerzeichen entfernt und Texte in Kleinbuchstaben umgewandelt werden. Außerdem habe ich Regeln definiert, damit Tags nur bestimmte Zeichen enthalten dürfen. Dadurch wird verhindert, dass ungültige oder uneinheitliche Tags in der Datenbank landen.

Zusätzlich habe ich mich mit Pydantic-Validatoren beschäftigt. Dabei habe ich verstanden, wie `field_validator` verwendet werden kann, um einzelne Felder zu prüfen, und wie eine zusätzliche Funktion zur Validierung und Normalisierung mehrfach im Code verwendet werden kann. Dadurch wurde die API robuster und die Datenqualität besser.

#### 2. 🚧 What challenges did I face?

Teilweise war der Code schwer verständlich, besonders die Logik hinter den Validatoren und deren Zusammenspiel mit anderen Komponenten der Anwendung. Es war nicht immer sofort klar, an welcher Stelle eine Eingabe geprüft wird und wann ein Fehler ausgelöst werden soll.

Besonders herausfordernd war die Arbeit mit Tag-Listen. Ich musste berücksichtigen, dass Tags leer sein können, doppelt vorkommen können oder in einem ungültigen Format eingegeben werden. Gleichzeitig sollte die API nicht unnötig kompliziert werden.

Außerdem musste ich darauf achten, dass die Validierung sowohl beim Erstellen neuer Notizen als auch beim Aktualisieren bestehender Notizen funktioniert. Dadurch war es wichtig, die Validierungslogik möglichst wiederverwendbar zu gestalten.

#### 3. 💡 How did I overcome them?

Ich habe die Validatoren Schritt für Schritt aufgebaut und mit verschiedenen Beispielen getestet. Dabei habe ich bewusst gültige und ungültige Eingaben ausprobiert, um zu sehen, ob die API richtig reagiert.

Zusätzlich habe ich recherchiert, wie Pydantic-Validatoren funktionieren und wie man Eingaben vor der Speicherung bereinigt. KI-Unterstützung und Dokumentation haben mir geholfen, die Logik besser zu verstehen.

Durch praktisches Ausprobieren konnte ich nachvollziehen, wie aus einer ungeordneten Eingabe ein sauber normalisierter Wert wird. Am Ende hatte ich ein besseres Verständnis dafür, warum Validierung ein wichtiger Bestandteil professioneller Backend-Entwicklung ist.

---

### Day 6

#### 1. ✅ What did I accomplish?

Heute habe ich mich mit erweiterten Python-Konzepten wie Decorators beschäftigt und die bestehende Test-Suite weiter ausprobiert. Dabei ging es darum zu verstehen, wie Funktionen erweitert werden können, ohne ihre eigentliche Logik direkt zu verändern.

Außerdem habe ich überprüft, ob die bisherigen API-Funktionen weiterhin korrekt arbeiten. Dazu gehörten das Erstellen, Abrufen, Aktualisieren und Löschen von Notizen sowie die Verarbeitung von Tags und Kategorien. Durch das erneute Ausführen der Tests konnte ich sicherstellen, dass neue Änderungen keine bereits funktionierenden Teile beschädigt haben.

Ein weiterer wichtiger Punkt war das Verständnis für den Zusammenhang zwischen sauberem Code und Testbarkeit. Ich habe gesehen, dass Funktionen und Endpunkte besser getestet werden können, wenn sie klar strukturiert sind und eindeutige Eingaben und Ausgaben haben.

#### 2. 🚧 What challenges did I face?

An diesem Tag traten keine größeren technischen Probleme auf. Trotzdem war es eine Herausforderung, die neuen Konzepte vollständig zu verstehen. Decorators sind zunächst abstrakt, weil sie Funktionen verändern oder erweitern können, ohne dass man die ursprüngliche Funktion direkt anpasst.

Außerdem musste ich weiterhin darauf achten, dass Änderungen am Code nicht dazu führen, dass bestehende Tests fehlschlagen. Auch kleine Anpassungen an Modellen oder Responses können Auswirkungen auf die Testergebnisse haben.

Eine weitere Herausforderung war es, die Übersicht über die verschiedenen Bestandteile des Projekts zu behalten: API-Endpunkte, Datenmodelle, Validierung, Tests und Datenbanklogik greifen alle ineinander.

#### 3. 💡 How did I overcome them?

Ich habe die Konzepte anhand kleiner Beispiele nachvollzogen und anschließend auf mein Projekt übertragen. Dadurch konnte ich besser verstehen, wie Decorators grundsätzlich funktionieren und warum sie in Python nützlich sein können.

Da keine größeren Fehler aufgetreten sind, konnte ich mich stärker auf das Verständnis und die Wiederholung konzentrieren. Ich habe die Tests genutzt, um Vertrauen in den aktuellen Stand des Codes zu bekommen.

Durch das strukturierte Überprüfen der bisherigen Funktionen konnte ich sicherstellen, dass mein Projekt stabil bleibt. Außerdem habe ich gelernt, dass regelmäßiges Testen wichtig ist, auch wenn gerade keine offensichtlichen Fehler auftreten.

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?

Heute habe ich begonnen, ein Frontend für meine NotesAPI mit Streamlit zu erstellen. Ziel war es, die API nicht nur über Endpunkte zu testen, sondern eine einfache Benutzeroberfläche zu bauen, über die Notizen angezeigt und später auch erstellt werden können.

Ich habe gelernt, wie Streamlit grundsätzlich funktioniert und wie man Eingabefelder, Buttons, Überschriften und Ausgabebereiche erstellt. Außerdem habe ich erste Funktionen eingebaut, um Daten aus einer API abzurufen. Dafür habe ich mit dem Python-Paket `requests` gearbeitet, um HTTP-Anfragen an das Backend zu senden.

Ein wichtiger Lernfortschritt war das Verständnis dafür, wie Backend und Frontend zusammenarbeiten. Das Backend stellt die Daten und Logik bereit, während das Frontend diese Daten für den Nutzer sichtbar und bedienbar macht. Dadurch wurde mein Projekt vollständiger, weil es nicht mehr nur aus einer API bestand, sondern auch eine einfache Oberfläche bekam.

#### 2. 🚧 What challenges did I face?

Beim Aufbau des Frontends gab es verschiedene Probleme. Besonders schwierig war die Verbindung zwischen dem lokal laufenden FastAPI-Backend und der Streamlit-Anwendung. Wenn das Backend nicht gestartet war oder die URL nicht korrekt verwendet wurde, konnte das Frontend keine Daten laden.

Außerdem war die Darstellung der Daten nicht sofort so, wie ich es erwartet hatte. Die API gibt Daten im JSON-Format zurück, aber diese müssen im Frontend sinnvoll angezeigt werden. Ich musste also entscheiden, welche Informationen angezeigt werden und wie Nutzer einzelne Notizen auswählen können.

Auch der Umgang mit dem Session State in Streamlit war neu. Ich musste verstehen, wie Daten im Frontend zwischengespeichert werden können, damit sie nicht bei jeder Aktion verloren gehen.

#### 3. 💡 How did I overcome them?

Ich habe zunächst die API-Endpunkte separat getestet, um sicherzustellen, dass das Backend korrekt funktioniert. Danach habe ich im Frontend geprüft, ob die Requests an die richtige URL gesendet werden und ob die Antworten korrekt verarbeitet werden.

Durch schrittweises Testen konnte ich Fehler in der Verbindung zwischen Frontend und Backend besser eingrenzen. Außerdem habe ich Streamlit-Fehlermeldungen genutzt, um zu erkennen, wo Probleme bei der Anzeige oder beim Laden der Daten entstanden sind.

Mit Hilfe von Internetrecherche und KI-Unterstützung konnte ich die Funktionsweise von Streamlit besser verstehen. Am Ende konnte ich ein erstes funktionierendes Frontend erstellen, das mit der NotesAPI verbunden ist.

---

### Day 8

#### 1. ✅ What did I accomplish?

Heute habe ich das Streamlit-Frontend weiter ausgearbeitet und stärker mit der NotesAPI verbunden. Ich habe Funktionen eingebaut, mit denen alle vorhandenen Notizen aus dem Backend geladen und im Frontend angezeigt werden können. Nutzer können über einen Button die Notizen aktualisieren und anschließend eine bestimmte Notiz auswählen, um Details wie Titel, Inhalt, Kategorie, Tags und Erstellungsdatum zu sehen.

Außerdem habe ich ein Formular erstellt, mit dem neue Notizen über die Benutzeroberfläche angelegt werden können. Das Formular enthält Eingabefelder für Titel, Inhalt, Kategorie und Tags. Die Tags werden als kommaseparierte Eingabe verarbeitet und anschließend als Liste an das Backend gesendet.

Dadurch konnte ich praktisch lernen, wie HTTP-Requests aus einem Frontend heraus funktionieren. Besonders wichtig war dabei der Unterschied zwischen GET-Requests zum Abrufen von Daten und POST-Requests zum Erstellen neuer Daten. Zusätzlich habe ich verstanden, wie API-Responses im Frontend weiterverarbeitet und für Nutzer verständlich dargestellt werden.

#### 2. 🚧 What challenges did I face?

Eine Herausforderung war die Aktualisierung der angezeigten Notizen nach dem Erstellen einer neuen Notiz. Zunächst wurden neue Einträge nicht immer direkt angezeigt, weil die Daten im Frontend erneut geladen werden mussten. Dadurch musste ich besser verstehen, wie Streamlit mit Zuständen und Neuladen der Oberfläche arbeitet.

Außerdem musste ich sicherstellen, dass leere Eingaben nicht zu Fehlern führen. Besonders Titel, Inhalt und Kategorie sollten nicht leer sein, da das Backend diese Felder benötigt. Auch die Verarbeitung von Tags musste sauber funktionieren, damit aus einer Texteingabe eine korrekte Liste wird.

Zusätzlich war es wichtig, Fehlermeldungen verständlich auszugeben. Wenn das Backend nicht erreichbar ist oder ein Request fehlschlägt, sollte das Frontend nicht einfach abstürzen, sondern eine passende Fehlermeldung anzeigen.

#### 3. 💡 How did I overcome them?

Ich habe die Funktionen im Frontend klarer aufgeteilt: eine Funktion zum Laden aller Notizen und eine Funktion zum Erstellen einer neuen Notiz. Dadurch wurde der Code übersichtlicher und leichter zu testen.

Nach dem Erstellen einer neuen Notiz habe ich die Notizen erneut aus dem Backend geladen, damit der neue Eintrag direkt sichtbar wird. Außerdem habe ich mit `st.session_state` gearbeitet, um Daten im Frontend zwischenzuspeichern und die Anzeige kontrollierter zu aktualisieren.

Bei den Eingaben habe ich zusätzliche Prüfungen eingebaut, damit Pflichtfelder nicht leer abgeschickt werden. Dadurch wurde das Frontend stabiler und benutzerfreundlicher. Insgesamt habe ich gelernt, wie wichtig die Abstimmung zwischen Frontend, Backend und Validierung ist.

---

### Day 9

#### 1. ✅ What did I accomplish?

Heute habe ich das Projekt weiter aufgeräumt, überprüft und für die Abgabe vorbereitet. Dabei habe ich kontrolliert, ob die wichtigsten Projektbestandteile vorhanden sind: das FastAPI-Backend, die SQLModel-Datenmodelle, die Pydantic-Validierung, die SQLite-Datenbank, die Pytest-Testdatei und das Streamlit-Frontend.

Außerdem habe ich mein Worklog ergänzt und ausführlicher dokumentiert, welche Aufgaben ich an den einzelnen Kurstagen bearbeitet habe. Dabei habe ich darauf geachtet, nicht nur Ergebnisse aufzuschreiben, sondern auch Herausforderungen und Lösungswege zu beschreiben.

Ein weiterer wichtiger Punkt war die Arbeit mit GitHub. Ich habe den aktuellen Projektstand gesichert und nachvollzogen, welche Entwicklungsschritte im Repository sichtbar sind. Dadurch ist der Fortschritt meines Projekts besser dokumentiert und für die Abgabe nachvollziehbarer.

#### 2. 🚧 What challenges did I face?

Die größte Herausforderung war es, den Überblick über alle erledigten Aufgaben zu behalten. Über mehrere Tage hinweg sind viele einzelne Funktionen entstanden, zum Beispiel CRUD-Endpunkte, Tags, Kategorien, Validierung, Tests und das Frontend. Diese Arbeitsschritte sinnvoll und chronologisch im Worklog zu beschreiben, war nicht ganz einfach.

Zusätzlich war es wichtig, das Repository sauber wirken zu lassen. Nicht benötigte Vorlagen oder unklare Dateien sollten möglichst vermieden werden, damit der Projektstand verständlich bleibt.

#### 3. 💡 How did I overcome them?

Ich habe die Dateien und bisherigen Commits im Repository noch einmal durchgesehen und die Arbeitsschritte den einzelnen Tagen zugeordnet. Dadurch konnte ich besser nachvollziehen, welche Funktionen zu welchem Zeitpunkt entstanden sind.

Anschließend habe ich das Worklog systematisch überarbeitet. Ich habe für jeden Tag beschrieben, was ich umgesetzt habe, welche Probleme aufgetreten sind und wie ich diese gelöst habe. Dabei habe ich besonders darauf geachtet, Fachbegriffe wie API, Endpunkte, Validierung, Tests, Datenbank und Frontend sinnvoll einzubauen.

Durch diese abschließende Dokumentation konnte ich den Lernfortschritt im Modul besser darstellen. Gleichzeitig habe ich mein Projekt reflektiert und verstanden, wie die einzelnen technischen Bestandteile zusammen ein vollständigeres API-Projekt ergeben.

---

# 🎉 Congratulations! You did it! 🎓✨