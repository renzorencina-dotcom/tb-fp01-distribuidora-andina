from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)

from services.pedido_service import obtener_pedidos


class PedidosPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("pedidosPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(4)

        titulo = QLabel("Gestión y seguimineto de pedidos")
        titulo.setObjectName("pageTitle")
        layout.addWidget(titulo)

        controles = self._crear_controles()
        layout.addWidget(controles)

        subtitulo = QLabel("Pedidos")
        subtitulo.setObjectName("sectionTitle")
        layout.addWidget(subtitulo)

        self.pedidos_lista = QTableWidget(0, 4)
        self.pedidos_lista.setObjectName("pedidosTable")

        self.pedidos_lista.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.pedidos_lista.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.pedidos_lista.setAlternatingRowColors(True)
        self.pedidos_lista.setShowGrid(False)
        self.pedidos_lista.setWordWrap(False)

        self.pedidos_lista.setHorizontalHeaderLabels(
            ["Codigo", "RUC", "Cliente", "Estado"]
        )
        encabezado = self.pedidos_lista.horizontalHeader()
        encabezado.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        encabezado.setMinimumHeight(42)
        encabezado.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        encabezado.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        self.pedidos_lista.setColumnWidth(0, 100)
        self.pedidos_lista.setColumnWidth(1, 130)
        self.pedidos_lista.setColumnWidth(3, 190)

        self.pedidos_lista.setMinimumHeight(300)
        self.pedidos_lista.setMaximumHeight(400)
        self.pedidos_lista.verticalHeader().setVisible(False)
        self.pedidos_lista.verticalHeader().setDefaultSectionSize(40)

        layout.addWidget(self.pedidos_lista)

        layout.addStretch()
        self._aplicar_estilos()

    def _crear_controles(self) -> QWidget:
        controles = QWidget()
        controles.setObjectName("crearControles")

        controles_layout = QHBoxLayout(controles)

        control_buscador = QLineEdit()
        control_buscador.setMinimumHeight(26)
        control_buscador.setObjectName("controlBuscador")
        control_buscador.setPlaceholderText("Buscar por código, RUC o cliente")

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

        controles_layout.addWidget(control_buscador,1)
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
            QLabel#sectionTitle {
                color: palette(window-text);
                font-size: 17px;
                font-weight: 600;
                margin-top: 4px;
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

    def actualizar_datos(self) -> None:
        pedidos_lista = obtener_pedidos()

        pedidos_mostrados = pedidos_lista[-5:]
        self.pedidos_lista.setRowCount(len(pedidos_mostrados))

        for fila, pedido in enumerate(reversed(pedidos_mostrados)):
            datos_pedido = [
                pedido.codigo_pedido,
                pedido.ruc_cliente,
                pedido.razon_social,
                pedido.estado,
            ]

            for columna, valor in enumerate(datos_pedido):
                item = QTableWidgetItem(str(valor))
                alineacion = Qt.AlignmentFlag.AlignVCenter

                if columna in (0, 1, 3):
                    alineacion |= Qt.AlignmentFlag.AlignHCenter
                else:
                    alineacion |= Qt.AlignmentFlag.AlignLeft

                item.setTextAlignment(alineacion)
                self.pedidos_lista.setItem(fila, columna, item)
