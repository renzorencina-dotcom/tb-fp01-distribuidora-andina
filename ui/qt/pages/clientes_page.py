from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ClientesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        titulo = QLabel("Modulo de clientes")

        layout.addWidget(titulo)
        layout.addStretch()
