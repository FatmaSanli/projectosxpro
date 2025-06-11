# ProjectOS X Pro

Ein modulares Projektmanagement-Tool mit PyQt6.

## Features

- **Mehrseitige Navigation**: Dashboard, Aufgaben (Kanban), Gantt, Reflexion, Einstellungen
- **Aufgaben/Kanban-Board**: Drag & Drop, Fälligkeitsdatum, Start-/Enddatum, Bearbeiten/Löschen, Beschreibung
- **Gantt-Chart**: Übersicht aller Aufgaben-Zeiträume mit matplotlib
- **Reflexionstagebuch**: Kalender, tägliche Notizen, Speicherung pro Tag
- **Einstellungen**: Theme-Wechsel (Dark/Light/Blau), Sprache (Platzhalter), Export/Import (CSV, PDF)
- **Dauerhafte Speicherung**: Aufgaben und Einstellungen in `.db` (SQLite) und `.json`
- **Login-System**: Benutzerverwaltung, Registrierung, Login
- **Fehlerbehandlung**: Grundlegende Hinweise und Dialoge bei Fehlern
- **Projekt-Checkliste**: Übersicht aller Pflichtbestandteile als eigene Seite

## Installation

```bash
pip install -r requirements.txt
```

## Starten

```bash
python main.py
```

## Hinweise

- Das Projekt speichert Einstellungen und Daten lokal als `.db` und `.json` Dateien.
- Für Mehrsprachigkeit ist das Grundgerüst vorbereitet.
- Das Gantt-Chart zeigt alle Aufgaben mit Start- und Enddatum (max. 20 Zeichen im Titel).
- Im Bereich **Einstellungen** kannst du das Farbschema (Theme) der App live wechseln und Aufgaben importieren/exportieren.
- Aufgaben werden beim ersten Start automatisch für den Projektzeitraum (14.05.2025–10.06.2025) angelegt.
- Die Projekt-Checkliste findest du als eigene Seite im Code (ToDoChecklistPage).

## Screenshots

*(Füge hier Screenshots deiner Anwendung ein)*

## Ausblick/Reflexion

- Weitere Features wie Benachrichtigungen, Teamarbeit oder Cloud-Speicherung sind denkbar.
- Die Sprachumschaltung ist vorbereitet, aber noch nicht vollständig umgesetzt.
