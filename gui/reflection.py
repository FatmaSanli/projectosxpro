from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QDateEdit, QHBoxLayout
from PyQt6.QtCore import QDate
import sqlite3

DB_PATH = "reflection.db"

def init_reflection_db():
    """
    Initialisiert die Datenbank für Reflexionen, falls sie noch nicht existiert.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            date TEXT PRIMARY KEY,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_reflection(date, text):
    """
    Speichert oder aktualisiert eine Reflexion für ein bestimmtes Datum.

    Args:
        date (str): Das Datum im Format 'YYYY-MM-DD'.
        text (str): Der Reflexionstext.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO reflections (date, text) VALUES (?, ?)", (date, text))
    conn.commit()
    conn.close()

def load_reflection(date):
    """
    Lädt die Reflexion für ein bestimmtes Datum.

    Args:
        date (str): Das Datum im Format 'YYYY-MM-DD'.

    Returns:
        str: Der gespeicherte Reflexionstext oder ein leerer String.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT text FROM reflections WHERE date=?", (date,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

class ReflectionPage(QWidget):
    """
    Seite für das Reflexionstagebuch mit Datumsauswahl und Notizfeld.
    """
    def __init__(self):
        """
        Initialisiert die Reflexionsseite mit UI-Elementen.
        """
        super().__init__()
        init_reflection_db()
        layout = QVBoxLayout(self)
        title = QLabel("Reflexionstagebuch")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        date_layout = QHBoxLayout()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.dateChanged.connect(self.load_note)
        date_layout.addWidget(QLabel("Datum:"))
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Deine Notiz für das gewählte Datum ...")
        layout.addWidget(self.text_edit)

        save_btn = QPushButton("Speichern")
        save_btn.clicked.connect(self.save_note)
        layout.addWidget(save_btn)

        self.load_note()

    def load_note(self):
        """
        Lädt die Notiz für das aktuell gewählte Datum und zeigt sie an.
        """
        date = self.date_edit.date().toString("yyyy-MM-dd")
        note = load_reflection(date)
        self.text_edit.setText(note if note else "")

    def save_note(self):
        """
        Speichert die aktuelle Notiz für das gewählte Datum.
        """
        date = self.date_edit.date().toString("yyyy-MM-dd")
        text = self.text_edit.toPlainText()
        save_reflection(date, text)
        QMessageBox.information(self, "Gespeichert", "Deine Notiz wurde gespeichert!")
