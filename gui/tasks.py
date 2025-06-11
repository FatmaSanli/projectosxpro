from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QComboBox, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from gui.tasks_db import get_tasks, add_task, update_task_status, delete_task, edit_task

class DateDialog(QDialog):
    """
    Dialog zur Auswahl eines Fälligkeitsdatums.
    """
    def __init__(self, parent=None, initial_date=None):
        super().__init__(parent)
        self.setWindowTitle("Fälligkeitsdatum wählen")
        layout = QFormLayout(self)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        if initial_date:
            self.date_edit.setDate(QDate.fromString(initial_date, "yyyy-MM-dd"))
        else:
            self.date_edit.setDate(QDate.currentDate())
        layout.addRow("Fällig am:", self.date_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_date(self):
        """
        Gibt das gewählte Datum als String zurück.
        """
        return self.date_edit.date().toString("yyyy-MM-dd")

class TaskDialog(QDialog):
    """
    Dialog zum Erstellen oder Bearbeiten einer Aufgabe.
    """
    def __init__(self, parent=None, title="", start_date=None, end_date=None):
        super().__init__(parent)
        self.setWindowTitle("Aufgabe bearbeiten/erstellen")
        layout = QFormLayout(self)
        self.title_edit = QLineEdit(title)
        layout.addRow("Titel:", self.title_edit)
        self.start_edit = QDateEdit()
        self.start_edit.setCalendarPopup(True)
        self.start_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_edit.setDate(QDate.fromString(start_date, "yyyy-MM-dd") if start_date else QDate.currentDate())
        layout.addRow("Startdatum:", self.start_edit)
        self.end_edit = QDateEdit()
        self.end_edit.setCalendarPopup(True)
        self.end_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_edit.setDate(QDate.fromString(end_date, "yyyy-MM-dd") if end_date else QDate.currentDate())
        layout.addRow("Enddatum:", self.end_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        """
        Gibt die eingegebenen Daten als Tuple zurück.
        """
        return (
            self.title_edit.text().strip(),
            self.start_edit.date().toString("yyyy-MM-dd"),
            self.end_edit.date().toString("yyyy-MM-dd")
        )

class DescriptionDialog(QDialog):
    """
    Dialog zur Anzeige und Bearbeitung der Aufgabenbeschreibung.
    """
    def __init__(self, description="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aufgabenbeschreibung")
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(description or "")
        layout.addWidget(QLabel("Beschreibung:"))
        layout.addWidget(self.text_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_description(self):
        """
        Gibt die eingegebene Beschreibung zurück.
        """
        return self.text_edit.toPlainText().strip()

class TasksPage(QWidget):
    """
    Seite für das Aufgaben-Kanban-Board.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #23272e; color: #fff;")
        layout = QVBoxLayout(self)
        title = QLabel("Aufgaben (Kanban)")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Neue Aufgabe eingeben...")
        self.input.setStyleSheet("background: #2c313c; color: #fff; border-radius: 5px; padding: 5px;")
        add_btn = QPushButton("Hinzufügen")
        add_btn.setStyleSheet("background: #3b82f6; color: #fff; border-radius: 5px; padding: 5px 15px;")
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(self.input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Alle", "To Do", "In Progress", "Done"])
        self.filter_combo.currentTextChanged.connect(self.refresh)
        layout.addWidget(self.filter_combo)

        filter_layout = QHBoxLayout()
        self.start_filter = QDateEdit()
        self.start_filter.setCalendarPopup(True)
        self.start_filter.setDisplayFormat("yyyy-MM-dd")
        self.start_filter.setDate(QDate.currentDate().addMonths(-1))
        self.start_filter.dateChanged.connect(self.refresh)
        filter_layout.addWidget(QLabel("Von:"))
        filter_layout.addWidget(self.start_filter)
        self.end_filter = QDateEdit()
        self.end_filter.setCalendarPopup(True)
        self.end_filter.setDisplayFormat("yyyy-MM-dd")
        self.end_filter.setDate(QDate.currentDate())
        self.end_filter.dateChanged.connect(self.refresh)
        filter_layout.addWidget(QLabel("Bis:"))
        filter_layout.addWidget(self.end_filter)
        layout.addLayout(filter_layout)

        board_layout = QHBoxLayout()
        self.lists = {}
        for status in ["To Do", "In Progress", "Done"]:
            col = QVBoxLayout()
            label = QLabel(status)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3b82f6; margin-bottom: 8px;")
            col.addWidget(label)
            lw = KanbanListWidget(status, self)
            lw.setStyleSheet("""
                QListWidget { background: #2c313c; border-radius: 8px; }
                QListWidget::item { padding: 8px; margin: 4px; border-radius: 4px; }
                QListWidget::item:selected { background: #3b82f6; }
            """)
            col.addWidget(lw)
            self.lists[status] = lw
            board_layout.addLayout(col)
        layout.addLayout(board_layout)
        self.refresh()

        self.task_descriptions = {}
        for t in get_tasks():
            if len(t) == 7:
                task_id = t[0]
                description = t[6]
                self.task_descriptions[task_id] = description if description else ""

    def refresh(self):
        """
        Aktualisiert die Aufgabenlisten und Filter.
        """
        self.task_descriptions = {}
        for t in get_tasks():
            if len(t) == 7:
                task_id = t[0]
                description = t[6]
                self.task_descriptions[task_id] = description if description else ""
        status_filter = self.filter_combo.currentText()
        start_range = self.start_filter.date().toString("yyyy-MM-dd")
        end_range = self.end_filter.date().toString("yyyy-MM-dd")
        for lw in self.lists.values():
            lw.clear()
        tasks_by_status = {"To Do": [], "In Progress": [], "Done": []}
        for task in get_tasks():
            task_id, title, status, due_date, start_date, end_date, description = task
            if start_date:
                if not (start_range <= start_date <= end_range):
                    continue
            if status_filter != "Alle" and status != status_filter:
                continue
            tasks_by_status[status].append((task_id, title, due_date, start_date, end_date))
        for status, lw in self.lists.items():
            sorted_tasks = sorted(
                tasks_by_status[status],
                key=lambda t: (t[2] is None, t[2] if t[2] else "")
            )
            for task_id, title, due_date, start_date, end_date in sorted_tasks:
                text = f"{title}"
                if start_date and end_date:
                    text += f" ({start_date} → {end_date})"
                elif due_date:
                    text += f" (fällig: {due_date})"
                item = QListWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, task_id)
                item.setForeground(Qt.GlobalColor.white)
                item.setBackground(Qt.GlobalColor.black)
                lw.addItem(item)

    def add_task(self):
        """
        Fügt eine neue Aufgabe hinzu.
        """
        title = self.input.text().strip()
        if title:
            add_task(title)
            self.input.clear()
            self.refresh()
        else:
            dlg = TaskDialog(self)
            if dlg.exec():
                title, start_date, end_date = dlg.get_data()
                add_task(title, start_date=start_date, end_date=end_date)
                self.refresh()

    def move_task(self, task_id, new_status):
        """
        Verschiebt eine Aufgabe in einen anderen Status.
        """
        update_task_status(task_id, new_status)
        self.refresh()

    def delete_task(self, task_id):
        """
        Löscht eine Aufgabe.
        """
        delete_task(task_id)
        self.refresh()

    def edit_task(self, task_id, old_title, old_start=None, old_end=None):
        """
        Bearbeitet eine Aufgabe.
        """
        dlg = TaskDialog(self, title=old_title, start_date=old_start, end_date=old_end)
        if dlg.exec():
            new_title, new_start, new_end = dlg.get_data()
            edit_task(task_id, new_title, new_start_date=new_start, new_end_date=new_end)
            self.refresh()

    def show_description(self, task_id, old_description=None):
        """
        Zeigt und bearbeitet die Beschreibung einer Aufgabe.
        """
        desc = self.task_descriptions.get(task_id, "")
        dlg = DescriptionDialog(description=desc, parent=self)
        if dlg.exec():
            new_description = dlg.get_description()
            self.task_descriptions[task_id] = new_description
            for t in get_tasks():
                if t[0] == task_id:
                    if len(t) == 7:
                        _, title, _, _, start_date, end_date, _ = t
                    else:
                        _, title, _, _, start_date, end_date = t
                    break
            edit_task(task_id, title, start_date, end_date, new_description)
            self.refresh()

class KanbanListWidget(QListWidget):
    """
    Kanban-Board-Spalte für Aufgaben eines Status.
    """
    def __init__(self, status, parent):
        super().__init__()
        self.status = status
        self.parent = parent
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        item = self.currentItem()
        if item is None and self.count() > 0:
            item = self.item(self.count() - 1)
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.parent.move_task(task_id, self.status)
        super().dropEvent(event)

    def open_menu(self, pos):
        """
        Öffnet das Kontextmenü für eine Aufgabe.
        """
        item = self.itemAt(pos)
        if item:
            from PyQt6.QtWidgets import QMenu
            menu = QMenu()
            edit_action = menu.addAction("Bearbeiten")
            desc_action = menu.addAction("Beschreibung anzeigen/bearbeiten")
            delete_action = menu.addAction("Löschen")
            action = menu.exec(self.mapToGlobal(pos))
            task_id = item.data(Qt.ItemDataRole.UserRole)
            for t in get_tasks():
                if t[0] == task_id:
                    if len(t) == 7:
                        _, title, _, _, start_date, end_date, description = t
                    else:
                        _, title, _, _, start_date, end_date = t
                        description = ""
                    break
            if action == edit_action:
                self.parent.edit_task(task_id, title, start_date, end_date)
            elif action == desc_action:
                self.parent.show_description(task_id, description)
            elif action == delete_action:
                self.parent.delete_task(task_id)

    def mouseDoubleClickEvent(self, event):
        """
        Öffnet den Beschreibungsdialog per Doppelklick.
        """
        item = self.itemAt(event.pos())
        if item:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            for t in get_tasks():
                if t[0] == task_id:
                    if len(t) == 7:
                        _, title, _, _, start_date, end_date, description = t
                    else:
                        _, title, _, _, start_date, end_date = t
                        description = ""
                    break
            self.parent.show_description(task_id, description)
        super().mouseDoubleClickEvent(event)

