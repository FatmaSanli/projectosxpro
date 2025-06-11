from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QSizePolicy
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from gui.dashboard import DashboardPage
from gui.tasks import TasksPage
from gui.gantt import GanttPage
from gui.reflection import ReflectionPage
from gui.settings import SettingsPage, load_theme

class MainWindow(QMainWindow):
    """
    Hauptfenster der Anwendung mit Navigation und Seiten-Stack.
    """
    def __init__(self):
        """
        Initialisiert das Hauptfenster mit Navigation und allen Seiten.
        """
        super().__init__()
        self.sidebar_buttons = []
        self.settings_page = SettingsPage()
        self.settings_page.theme_changed.connect(self.apply_theme)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        nav_layout = QHBoxLayout()
        button_infos = [
            ("🏠 Dashboard", self.show_dashboard),
            ("✅ Aufgaben", self.show_tasks),
            ("📊 Gantt", self.show_gantt),
            ("📝 Reflexion", self.show_reflection),
            ("⚙️ Einstellungen", self.show_settings),
        ]
        for text, slot in button_infos:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(slot)
            btn.setStyleSheet("font-size: 16px; padding: 8px 18px; border-radius: 8px;")
            nav_layout.addWidget(btn)
            self.sidebar_buttons.append(btn)
        main_layout.addLayout(nav_layout)

        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.tasks_page = TasksPage()
        self.gantt_page = GanttPage()
        self.reflection_page = ReflectionPage()
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.tasks_page)
        self.stack.addWidget(self.gantt_page)
        self.stack.addWidget(self.reflection_page)
        self.stack.addWidget(self.settings_page)
        main_layout.addWidget(self.stack)

        self.show_dashboard()

    def show_dashboard(self):
        """
        Zeigt die Dashboard-Seite an.
        """
        self.stack.setCurrentIndex(0)
        self._set_active_button(0)

    def show_tasks(self):
        """
        Zeigt die Aufgaben-Seite an.
        """
        self.stack.setCurrentIndex(1)
        self._set_active_button(1)

    def show_gantt(self):
        """
        Zeigt die Gantt-Chart-Seite an.
        """
        self.stack.setCurrentIndex(2)
        self._set_active_button(2)

    def show_reflection(self):
        """
        Zeigt die Reflexions-Seite an.
        """
        self.stack.setCurrentIndex(3)
        self._set_active_button(3)

    def show_settings(self):
        """
        Zeigt die Einstellungen-Seite an.
        """
        self.stack.setCurrentIndex(4)
        self._set_active_button(4)

    def _set_active_button(self, idx):
        """
        Markiert den aktiven Navigationsbutton.
        """
        for i, btn in enumerate(self.sidebar_buttons):
            btn.setChecked(i == idx)

    def apply_theme(self, theme):
        """
        Wendet das gewählte Farbschema auf das Hauptfenster an.

        Args:
            theme (str): Name des gewählten Themes.
        """
        if theme == "Hell":
            self.setStyleSheet("""
                QWidget { background: #f4f6fa; color: #222; }
                QPushButton { background: #3b82f6; color: #fff; }
            """)
        elif theme == "Dunkel":
            self.setStyleSheet("""
                QWidget { background: #23272e; color: #fff; }
                QPushButton { background: #3b82f6; color: #fff; }
            """)
        elif theme == "Blau":
            self.setStyleSheet("""
                QWidget { background: #e0eaff; color: #1a237e; }
                QPushButton { background: #1976d2; color: #fff; }
            """)
        for btn in self.sidebar_buttons:
            btn.setStyleSheet("")
