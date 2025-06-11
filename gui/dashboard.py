from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QProgressBar, QSizePolicy, QMenu, QPushButton
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtCore import Qt
from gui.tasks_db import get_tasks

class DashboardPage(QWidget):
    """
    Dashboard-Ansicht mit Statistiken, Fortschrittsbalken und Profilmenü.
    """
    def __init__(self, username=""):
        """
        Initialisiert das Dashboard mit Statistiken und Profilanzeige.

        Args:
            username (str): Der Benutzername für das Profil-Icon.
        """
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)

        header = QHBoxLayout()
        title = QLabel("📊 Dashboard")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        header.addWidget(title)

        self.profile_btn = QPushButton()
        self.profile_btn.setFixedSize(48, 48)
        self.profile_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if username:
            initials = username[:2].upper()
            self.profile_btn.setText(f"👤 {initials}")
        else:
            self.profile_btn.setText("👤")
        self.profile_btn.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f8cff, stop:1 #3b82f6);
            color: white;
            border-radius: 24px;
            font-size: 22px;
            font-weight: bold;
            padding: 8px;
        """)
        self.profile_btn.clicked.connect(self.show_profile_menu)
        header.addWidget(self.profile_btn)
        main_layout.addLayout(header)

        stats_box = QHBoxLayout()
        tasks = get_tasks()
        total = len(tasks)
        todo = sum(1 for t in tasks if t[2] == "To Do")
        inprogress = sum(1 for t in tasks if t[2] == "In Progress")
        done = sum(1 for t in tasks if t[2] == "Done")

        stat_labels = [
            ("<span style='font-size:22px;'>📋</span><br>Gesamt", total, "#6366f1"),
            ("<span style='font-size:22px;'>🕒</span><br>Offen", todo, "#f59e42"),
            ("<span style='font-size:22px;'>🚧</span><br>In Arbeit", inprogress, "#3b82f6"),
            ("<span style='font-size:22px;'>✅</span><br>Erledigt", done, "#22c55e"),
        ]
        for label, value, color in stat_labels:
            box = QVBoxLayout()
            l = QLabel(label)
            l.setStyleSheet("font-size: 15px; color: #888; text-align: center;")
            l.setTextFormat(Qt.TextFormat.RichText)
            v = QLabel(str(value))
            v.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color}; text-align: center;")
            box.addWidget(l, alignment=Qt.AlignmentFlag.AlignCenter)
            box.addWidget(v, alignment=Qt.AlignmentFlag.AlignCenter)
            stats_box.addLayout(box)
        main_layout.addLayout(stats_box)

        progress = QProgressBar()
        progress.setValue(int(done / total * 100) if total else 0)
        progress.setFormat("Fortschritt: %p%")
        progress.setStyleSheet("""
            QProgressBar {
                border-radius: 8px;
                background: #222;
                height: 24px;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #22c55e;
                border-radius: 8px;
            }
        """)
        main_layout.addWidget(progress)

        next_due = min(
            (t for t in tasks if t[3]),
            key=lambda t: t[3],
            default=None
        )
        next_label = QLabel()
        if next_due:
            next_label.setText(f"Nächste Fälligkeit: <b>{next_due[1]}</b> am <b>{next_due[3]}</b>")
        else:
            next_label.setText("Keine fälligen Aufgaben.")
        next_label.setStyleSheet("font-size: 15px; margin-top: 18px;")
        main_layout.addWidget(next_label)

    def refresh(self):
        """
        Aktualisiert das Dashboard, indem es die Ansicht neu aufbaut.
        """
        self.__init__()  # Einfach neu aufbauen, damit alles aktuell ist

    def show_profile_menu(self):
        """
        Zeigt das Profilmenü mit der Option zum Abmelden an.
        """
        menu = QMenu()
        logout_action = QAction("Abmelden", self)
        logout_action.triggered.connect(self.logout)
        menu.addAction(logout_action)
        menu.exec(QCursor.pos())

    def logout(self):
        """
        Meldet den aktuellen Benutzer ab und zeigt den Login-Dialog.
        """
        from gui.login import LoginDialog
        app = self.window().parent()
        self.window().close()
        login = LoginDialog()
        if login.exec() == login.DialogCode.Accepted:
            username, password = login.get_credentials()
            from gui.tasks_db import check_user
            if check_user(username, password):
                from gui.main_window import MainWindow
                window = MainWindow()
                window.show()
