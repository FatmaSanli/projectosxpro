# ProjectOS X Pro

**ProjectOS X Pro** ist ein modulares, modernes Projektmanagement-Tool, das mit [PyQt6](https://riverbankcomputing.com/software/pyqt/intro) entwickelt wurde. Es richtet sich an Einzelpersonen, Schüler:innen und kleine Teams, die ihre Projekte übersichtlich und effizient organisieren möchten.

## Einführung

Mit ProjectOS X Pro kannst du deine Aufgaben, Fortschritte und Reflexionen rund um ein Projekt an einem Ort verwalten. Die Anwendung bietet eine intuitive grafische Oberfläche mit mehreren Seiten (Tabs), darunter ein Kanban-Board, ein Gantt-Diagramm, ein Reflexionstagebuch und eine Projekt-Checkliste.  
Durch die Speicherung aller Daten in einer lokalen SQLite-Datenbank und einer JSON-Datei bleiben deine Aufgaben und Einstellungen auch nach einem Neustart erhalten.

Das Tool unterstützt grundlegende Projektmanagement-Funktionen wie Aufgabenverwaltung (inkl. Drag & Drop), Fortschrittsanzeige, Export/Import von Aufgaben, verschiedene Themes sowie ein Login-System für mehrere Benutzer.  
ProjectOS X Pro eignet sich besonders für schulische Softwareprojekte, da es alle Pflichtbestandteile (wie Dokumentation, Fehlerbehandlung, strukturierte Codebasis) abdeckt und leicht erweitert werden kann.

---

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
