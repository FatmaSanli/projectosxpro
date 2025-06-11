from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPushButton
from .register_dialog import RegisterDialog

class LoginDialog(QDialog):
    """
    Dialogfenster für den Login eines Benutzers.
    """
    def __init__(self, parent=None):
        """
        Initialisiert das Login-Dialogfenster.
        """
        super().__init__(parent)
        self.setWindowTitle("Login")
        layout = QFormLayout(self)
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Benutzername:", self.username)
        layout.addRow("Passwort:", self.password)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.register_btn = QPushButton("Registrieren")
        self.register_btn.clicked.connect(self.open_register)
        layout.addWidget(self.register_btn)

    def get_credentials(self):
        """
        Gibt die eingegebenen Zugangsdaten zurück.

        Returns:
            tuple: (Benutzername, Passwort)
        """
        return self.username.text(), self.password.text()

    def open_register(self):
        """
        Öffnet den Registrierungsdialog und legt ggf. einen neuen Benutzer an.
        """
        from gui.tasks_db import add_user
        dlg = RegisterDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            username, password = dlg.get_credentials()
            if add_user(username, password):
                QMessageBox.information(self, "Erfolg", "Benutzer wurde angelegt!")
            else:
                QMessageBox.warning(self, "Fehler", "Benutzername existiert bereits!")