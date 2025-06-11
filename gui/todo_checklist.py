from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class ToDoChecklistPage(QWidget):
    """
    Seite mit einer Checkliste der Projekt-Pflichtbestandteile.
    """
    def __init__(self):
        """
        Initialisiert die Checklisten-Seite.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Projekt-Checkliste (Pflichtbestandteile)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        checklist = """
1. Grobentwurf
   - [ ] Projektidee und Funktionsskizze oder Beschreibung (mind. 1/2 Seite)
   - [ ] Ziel(e) des Tools klar formuliert

2. GUI-Grundstruktur
   - [ ] Oberfläche mit Tabs oder klar gegliederten Bereichen (z.B. Sidebar)
   - [ ] Navigation zwischen den Bereichen möglich

3. Interaktive Funktion
   - [ ] Aufgabenverwaltung (z.B. Kanban-Board)
   - [ ] Aufgaben können hinzugefügt, bearbeitet, gelöscht werden
   - [ ] Aufgabenstatus kann geändert werden (To Do, In Progress, Done)

4. Datenhaltung
   - [ ] Aufgaben werden gespeichert und geladen (SQLite oder JSON)
   - [ ] Daten bleiben nach Neustart erhalten

5. Strukturierter Code
   - [ ] Trennung von GUI, Logik und Daten (mind. 2-3 Dateien/Module)
   - [ ] Übersichtliche und wartbare Struktur

6. Dokumentation
   - [ ] README.md mit Projektbeschreibung
   - [ ] Screenshots der Anwendung
   - [ ] Ausblick/Reflexion

7. Fehlerbehandlung
   - [ ] Grundlegendes Logging oder Fehlermeldungen im Programmablauf
   - [ ] Verständliche Hinweise bei Fehlern (z.B. beim Login, beim Speichern)
"""
        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(checklist)
        layout.addWidget(text)