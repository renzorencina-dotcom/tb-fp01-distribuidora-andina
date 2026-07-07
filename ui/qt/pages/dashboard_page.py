from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        titulo = QLabel("Resumen general")

        layout.addWidget(titulo)
        layout.addStretch()