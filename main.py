from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog
import sys
from gui.main_window import MainWindow
from gui.login import LoginDialog
from logic.tasks_db import init_db, init_user_db, check_user, add_task
from gui.dashboard import DashboardPage
from datetime import datetime, timedelta
import sqlite3

DB_PATH = "tasks.db"

def init_db():
    """
    Initialisiert die Aufgaben-Datenbank und führt ggf. Migrationen durch.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in c.fetchall()]
    if "description" not in columns:
        try:
            c.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

def get_tasks():
    """
    Gibt alle Aufgaben als Liste von Tupeln zurück.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, status, due_date, start_date, end_date, description FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def main():
    """
    Startet die Anwendung, initialisiert die Datenbanken und zeigt das Login-Fenster.
    """
    init_db()
    init_user_db()

    # Aufgaben nur beim ersten Start einfügen!
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]
    if count == 0:
        start = datetime(2025, 5, 14)
        deadline = datetime(2025, 6, 10)
        aufgaben = [
            ("Idee", "To Do", start.strftime("%Y-%m-%d"), (start + timedelta(days=2)).strftime("%Y-%m-%d")),
            ("Entwurf", "To Do", (start + timedelta(days=3)).strftime("%Y-%m-%d"), (start + timedelta(days=5)).strftime("%Y-%m-%d")),
            ("Layout", "In Progress", (start + timedelta(days=6)).strftime("%Y-%m-%d"), (start + timedelta(days=9)).strftime("%Y-%m-%d")),
            ("Kernfunktion", "In Progress", (start + timedelta(days=10)).strftime("%Y-%m-%d"), (start + timedelta(days=14)).strftime("%Y-%m-%d")),
            ("Daten", "To Do", (start + timedelta(days=15)).strftime("%Y-%m-%d"), (start + timedelta(days=18)).strftime("%Y-%m-%d")),
            ("Feinschliff", "To Do", (start + timedelta(days=19)).strftime("%Y-%m-%d"), (start + timedelta(days=21)).strftime("%Y-%m-%d")),
            ("Doku", "To Do", (start + timedelta(days=22)).strftime("%Y-%m-%d"), deadline.strftime("%Y-%m-%d")),
        ]
        for title, status, s, e in aufgaben:
            add_task(title, status=status, start_date=s, end_date=e)
    conn.close()

    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted:
        username, password = login.get_credentials()
        if check_user(username, password):
            window = MainWindow()
            window.dashboard_page = DashboardPage(username)
            window.show()
            sys.exit(app.exec())
        else:
            QMessageBox.critical(None, "Fehler", "Login fehlgeschlagen!")
    else:
        sys.exit()

if __name__ == "__main__":
    main()
