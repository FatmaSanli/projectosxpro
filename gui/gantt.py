import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from gui.tasks_db import get_tasks
import pandas as pd
import matplotlib.dates as mdates

class GanttPage(QWidget):
    """
    Seite für die Anzeige eines Gantt-Charts aller Aufgaben mit Start- und Enddatum.
    """
    def __init__(self):
        """
        Initialisiert die Gantt-Chart-Seite und zeigt das Diagramm an.
        """
        super().__init__()
        self.layout = QVBoxLayout(self)
        title = QLabel("Gantt-Chart (Projektübersicht)")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        self.layout.addWidget(title)
        self.canvas = None
        self.plot_gantt()

    def plot_gantt(self):
        """
        Erstellt und zeigt das Gantt-Chart für alle Aufgaben mit Start- und Enddatum.
        """
        tasks = [
            (t[1], t[4], t[5])  # (title, start_date, end_date)
            for t in get_tasks()
            if t[4] and t[5] and len(t[1]) <= 20
        ]
        # Sortiere nach Startdatum
        tasks.sort(key=lambda x: x[1])

        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.setParent(None)

        if not tasks:
            label = QLabel("Keine Aufgaben mit Start- und Enddatum vorhanden.")
            self.layout.addWidget(label)
            return

        fig, ax = plt.subplots(figsize=(9, max(3, len(tasks) * 0.5)))
        yticks = []
        ylabels = []
        for i, (title, start, end) in enumerate(tasks):
            start_dt = pd.to_datetime(start)
            end_dt = pd.to_datetime(end)
            ax.barh(i, (end_dt - start_dt).days, left=start_dt,
                    height=0.5, color="#3b82f6", edgecolor="#222", alpha=0.85)
            yticks.append(i)
            ylabels.append(title)
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels, fontsize=12)
        ax.set_xlabel("Datum", fontsize=12)
        ax.set_title("Gantt-Chart (Aufgaben mit Start-/Enddatum)", fontsize=15, fontweight="bold")
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        fig.tight_layout(pad=2.0)

        # Datumsformatierung und bessere Lesbarkeit
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        fig.autofmt_xdate(rotation=30)

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)
