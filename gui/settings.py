import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QComboBox
from PyQt6.QtCore import pyqtSignal
from gui.tasks_db import export_tasks_to_csv, import_tasks_from_csv, export_tasks_to_pdf

SETTINGS_PATH = "settings.json"

def save_theme(theme):
    """
    Speichert das aktuelle Theme in der Settings-Datei.
    """
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump({"theme": theme}, f)

def load_theme():
    """
    Lädt das gespeicherte Theme aus der Settings-Datei.

    Returns:
        str: Name des Themes.
    """
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("theme", "Dark")
    return "Dark"

def save_settings(theme, language):
    """
    Speichert Theme und Sprache in der Settings-Datei.
    """
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump({"theme": theme, "language": language}, f)

def load_settings():
    """
    Lädt Theme und Sprache aus der Settings-Datei.

    Returns:
        tuple: (theme, language)
    """
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("theme", "Dark"), data.get("language", "Deutsch")
    return "Dark", "Deutsch"

class SettingsPage(QWidget):
    """
    Seite für Einstellungen wie Theme, Sprache und Export/Import.
    """
    theme_changed = pyqtSignal(str)

    def __init__(self):
        """
        Initialisiert die Einstellungsseite mit allen UI-Elementen.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Einstellungen")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        info = QLabel("Hier kannst du das Theme, Sprache und weitere Optionen ändern.")
        info.setStyleSheet("font-size: 16px; color: #aaa;")
        layout.addWidget(info)

        export_btn = QPushButton("Aufgaben als CSV exportieren")
        export_btn.clicked.connect(self.export_csv)
        layout.addWidget(export_btn)

        import_btn = QPushButton("Aufgaben aus CSV importieren")
        import_btn.clicked.connect(self.import_csv)
        layout.addWidget(import_btn)

        pdf_btn = QPushButton("Aufgaben als PDF exportieren")
        pdf_btn.clicked.connect(self.export_pdf)
        layout.addWidget(pdf_btn)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Blau"])

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Deutsch", "English"])

        theme, language = load_settings()
        self.theme_combo.setCurrentText(theme)
        self.language_combo.setCurrentText(language)

        self.theme_combo.currentTextChanged.connect(self.save_all_settings)
        self.language_combo.currentTextChanged.connect(self.save_all_settings)

        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_combo)
        layout.addWidget(QLabel("Sprache:"))
        layout.addWidget(self.language_combo)

    def export_csv(self):
        """
        Exportiert Aufgaben als CSV-Datei.
        """
        path, _ = QFileDialog.getSaveFileName(self, "CSV speichern", "tasks_export.csv", "CSV-Dateien (*.csv)")
        if path:
            export_tasks_to_csv(path)
            QMessageBox.information(self, "Export", "Aufgaben wurden exportiert!")

    def import_csv(self):
        """
        Importiert Aufgaben aus einer CSV-Datei.
        """
        path, _ = QFileDialog.getOpenFileName(self, "CSV auswählen", "", "CSV-Dateien (*.csv)")
        if path:
            import_tasks_from_csv(path)
            QMessageBox.information(self, "Import", "Aufgaben wurden importiert!")
            main_window = self.window()
            if hasattr(main_window, "stack"):
                tasks_page = main_window.stack.widget(1)
                if hasattr(tasks_page, "refresh"):
                    tasks_page.refresh()
                gantt_page = main_window.stack.widget(2)
                if hasattr(gantt_page, "plot_gantt"):
                    gantt_page.plot_gantt()

    def export_pdf(self):
        """
        Exportiert Aufgaben als PDF-Datei.
        """
        path, _ = QFileDialog.getSaveFileName(self, "PDF speichern", "tasks_export.pdf", "PDF-Dateien (*.pdf)")
        if path:
            export_tasks_to_pdf(path)
            QMessageBox.information(self, "Export", "Aufgaben wurden als PDF exportiert!")

    def change_theme(self, theme):
        """
        Wendet das gewählte Theme auf das Hauptfenster an und speichert es.
        """
        mw = self.window()
        if theme == "Light":
            mw.setStyleSheet("""
                QMainWindow { background: #f5f5f5; }
                QWidget { background: #f5f5f5; color: #222; }
                QPushButton { background: #e0e0e0; color: #222; border: none; padding: 8px; border-radius: 6px; }
                QPushButton:hover { background: #bdbdbd; }
                QLineEdit { background: #fff; color: #222; border-radius: 5px; padding: 5px; }
                QListWidget { background: #fff; color: #222; border-radius: 8px; }
            """)
        elif theme == "Blau":
            mw.setStyleSheet("""
                QMainWindow { background: #001f3f; }
                QWidget { background: #001f3f; color: #fff; }
                QPushButton { background: #007bff; color: #fff; border: none; padding: 8px; border-radius: 6px; }
                QPushButton:hover { background: #0056b3; }
                QLineEdit { background: #003366; color: #fff; border-radius: 5px; padding: 5px; }
                QListWidget { background: #003366; color: #fff; border-radius: 8px; }
            """)
        else:
            mw.setStyleSheet("""
                QMainWindow { background: #23272e; }
                QWidget { background: #23272e; color: #fff; }
                QPushButton { background: #23272e; color: #fff; border: none; padding: 8px; border-radius: 6px; }
                QPushButton:hover { background: #3b3f4a; }
                QLineEdit { background: #2c313c; color: #fff; border-radius: 5px; padding: 5px; }
                QListWidget { background: #2c313c; color: #fff; border-radius: 8px; }
            """)
        save_theme(theme)

    def save_all_settings(self):
        """
        Speichert alle Einstellungen und wendet sie an.
        """
        theme = self.theme_combo.currentText()
        language = self.language_combo.currentText()
        save_settings(theme, language)
        self.change_theme(theme)
        self.change_language(language)

    def change_language(self, language):
        """
        Platzhalter für spätere Übersetzungen.
        """
        pass

    def on_theme_change(self, theme):
        """
        Signalisiert eine Theme-Änderung.
        """
        self.theme_changed.emit(theme)
