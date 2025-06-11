from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class RegisterDialog(QDialog):
    """
    Dialogfenster für die Benutzerregistrierung.
    """
    def __init__(self, parent=None):
        """
        Initialisiert das Registrierungsdialogfenster.
        """
        super().__init__(parent)
        self.setWindowTitle("Registrieren")
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

    def get_credentials(self):
        """
        Gibt die eingegebenen Registrierungsdaten zurück.

        Returns:
            tuple: (Benutzername, Passwort)
        """
        return self.username.text(), self.password.text()