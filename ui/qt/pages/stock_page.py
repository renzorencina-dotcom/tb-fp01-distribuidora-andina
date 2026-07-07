from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class StockPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        titulo = QLabel("Modulo de stocks")

        layout.addWidget(titulo)
        layout.addStretch()
