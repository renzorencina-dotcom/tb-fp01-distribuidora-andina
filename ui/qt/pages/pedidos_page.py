from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
)


class PedidosPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("pedidosPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(4)

        titulo = QLabel("Gestión y seguimineto de pedidos")
        titulo.setObjectName("pageTitle")

        controles = self._crear_controles()

        layout.addWidget(titulo)
        layout.addWidget(controles)

        layout.addStretch()
        self._aplicar_estilos()

    def _crear_controles(self) -> QWidget:
        controles = QWidget()
        controles.setObjectName("crearControles")

        controles_layout = QHBoxLayout(controles)

        control_buscador = QLineEdit()
        control_buscador.setMinimumHeight(26)
        control_buscador.setObjectName("controlBuscador")
        control_buscador.setPlaceholderText("Buscar por codigo, RUC o cliente")

        control_filtro = QComboBox()
        control_filtro.setObjectName("controlFiltro")
        control_filtro.addItems([
            "Todos los estados",
            "Registrados",
            "Atendidos",
            "Cancelados"
        ])

        control_nuevo = QPushButton("Nuevo pedido")
        control_nuevo.setObjectName("controlNuevo")

        controles_layout.addWidget(control_buscador)
        controles_layout.addWidget(control_filtro)
        controles_layout.addWidget(control_nuevo)

        return controles

    def _aplicar_estilos(self) -> None:
        self.setStyleSheet(
            """
            QWidget#pedidosPage {
            background-color: palette(window);
            }
            
            QLabel#pageTitle {
            color: palette(window-text);
            font-size: 26px;
            font-weight: 700;
            }
            
            QLineEdit#controlBuscador {
            color: palette(window-text);
            border-radius: 5px;
            border-style: solid;
            border-width: 1px;
            border-color: white;
            }
            """
        )
