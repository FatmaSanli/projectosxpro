import sqlite3
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DB_PATH = "tasks.db"

def init_db():
    """
    Initialisiert die Aufgaben-Datenbank und führt ggf. Migrationen durch.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Migration: Spalten hinzufügen, falls sie fehlen
    c.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in c.fetchall()]
    if "description" not in columns:
        try:
            c.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
        except sqlite3.OperationalError:
            pass
    # Tabelle anlegen (falls noch nicht vorhanden)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT,
            start_date TEXT,
            end_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def init_user_db():
    """
    Initialisiert die User-Datenbank (Tabelle users).
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_tasks():
    """
    Gibt alle Aufgaben als Liste von Tupeln zurück.
    Returns:
        list: [(id, title, status, due_date, start_date, end_date, description), ...]
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, status, due_date, start_date, end_date, description FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task(title, status="To Do", due_date=None, start_date=None, end_date=None, description=None):
    """
    Fügt eine neue Aufgabe hinzu.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (title, status, due_date, start_date, end_date, description) VALUES (?, ?, ?, ?, ?, ?)",
        (title, status, due_date, start_date, end_date, description)
    )
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    """
    Aktualisiert den Status einer Aufgabe.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """
    Löscht eine Aufgabe anhand ihrer ID.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def edit_task(task_id, new_title, new_start_date=None, new_end_date=None, new_description=None):
    """
    Bearbeitet eine Aufgabe (Titel, Start-/Enddatum, Beschreibung).
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if new_description is not None:
        c.execute(
            "UPDATE tasks SET title=?, start_date=?, end_date=?, description=? WHERE id=?",
            (new_title, new_start_date, new_end_date, new_description, task_id)
        )
    else:
        c.execute(
            "UPDATE tasks SET title=?, start_date=?, end_date=? WHERE id=?",
            (new_title, new_start_date, new_end_date, task_id)
        )
    conn.commit()
    conn.close()

def export_tasks_to_csv(filepath="tasks_export.csv"):
    """
    Exportiert alle Aufgaben als CSV-Datei.
    """
    tasks = get_tasks()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Titel", "Status", "Fälligkeitsdatum", "Startdatum", "Enddatum", "Beschreibung"])
        for task in tasks:
            writer.writerow(task)

def import_tasks_from_csv(filepath):
    """
    Importiert Aufgaben aus einer CSV-Datei.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("Titel") or row.get("Title") or ""
            status = row.get("Status", "To Do")
            due_date = row.get("Fälligkeitsdatum") or row.get("Due Date") or None
            start_date = row.get("Startdatum") or row.get("Start Date") or None
            end_date = row.get("Enddatum") or row.get("End Date") or None
            description = row.get("Beschreibung") or row.get("Description") or None
            add_task(
                title,
                status=status,
                due_date=due_date,
                start_date=start_date,
                end_date=end_date,
                description=description
            )

def export_tasks_to_pdf(filepath="tasks_export.pdf"):
    """
    Exportiert alle Aufgaben als PDF-Datei.
    """
    tasks = get_tasks()
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Aufgabenliste")
    y -= 30
    c.setFont("Helvetica", 10)
    headers = ["ID", "Titel", "Status", "Fälligkeitsdatum", "Startdatum", "Enddatum", "Beschreibung"]
    c.drawString(40, y, " | ".join(headers))
    y -= 20
    for task in tasks:
        line = " | ".join(str(x) if x else "" for x in task)
        c.drawString(40, y, line)
        y -= 18
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()

def check_user(username, password):
    """
    Prüft, ob ein Benutzer mit den angegebenen Zugangsdaten existiert.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    """
    Legt einen neuen Benutzer an.
    Returns:
        bool: True bei Erfolg, False falls Benutzername existiert.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success