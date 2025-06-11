from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

class TaskCard(QWidget):
    """
    Widget für die Darstellung einer einzelnen Aufgabe als Karte.
    """
    def __init__(self, title, subtitle=""):
        """
        Erstellt eine TaskCard mit Titel und optionalem Untertitel.

        Args:
            title (str): Der Titel der Aufgabe.
            subtitle (str, optional): Zusatzinfo oder Untertitel.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(title_label)
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color: #888; font-size: 12px;")
            layout.addWidget(subtitle_label)
        self.setStyleSheet("""
            background: #fff;
            border-radius: 12px;
            padding: 10px 12px;
            margin: 8px 0;
        """)