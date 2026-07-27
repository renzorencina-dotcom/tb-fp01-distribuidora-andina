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

from models import pedido
from services.pedido_service import obtener_pedidos


class PedidosPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("pedidosPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(4)

        titulo = QLabel("Gestión y seguimiento de pedidos")
        titulo.setObjectName("pageTitle")
        layout.addWidget(titulo)

        controles = self._crear_controles()
        layout.addWidget(controles)

        subtitulo = QLabel("Pedidos")
        subtitulo.setObjectName("sectionTitle")
        layout.addWidget(subtitulo)

        pedidos_lista = self._crear_tabla()
        layout.addWidget(pedidos_lista)

        layout.addStretch()
        
        self._aplicar_estilos()
        self._conectar_senales()
        self.actualizar_datos()

    def _crear_controles(self) -> QWidget:
        controles = QWidget()
        controles.setObjectName("crearControles")

        controles_layout = QHBoxLayout(controles)

        self.control_buscador = QLineEdit()
        self.control_buscador.setMinimumHeight(26)
        self.control_buscador.setObjectName("controlBuscador")
        self.control_buscador.setPlaceholderText("Buscar por código, RUC o cliente")

        self.control_filtro = QComboBox()
        self.control_filtro.setObjectName("controlFiltro")
        self.control_filtro.addItems([
            "Todos los estados",
            "Registrados",
            "Atendidos",
            "Cancelados"
        ])

        self.control_nuevo = QPushButton("Nuevo pedido")
        self.control_nuevo.setObjectName("controlNuevo")

        controles_layout.addWidget(self.control_buscador,1)
        controles_layout.addWidget(self.control_filtro)
        controles_layout.addWidget(self.control_nuevo)

        return controles

    def _crear_tabla(self) -> QTableWidget:
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
            ["Código", "RUC", "Cliente", "Estado"]
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

        self.pedidos_lista.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.pedidos_lista.verticalHeader().setVisible(False)
        self.pedidos_lista.verticalHeader().setDefaultSectionSize(40)

        return self.pedidos_lista

    def _filtrar_pedidos(self, pedidos):
        texto_busqueda = self.control_buscador.text().strip().lower()
        estado = self.control_filtro.currentText()

        pedidos_filtrados = []

        for pedido in pedidos:

            coincide_busqueda = (
                    texto_busqueda in str(pedido.codigo_pedido).lower()
                    or texto_busqueda in str(pedido.ruc_cliente).lower()
                    or texto_busqueda in pedido.razon_social.lower()
                    or texto_busqueda in pedido.estado.lower()
            )

            if coincide_busqueda:
                pedidos_filtrados.append(pedido)

        return pedidos_filtrados

    def _conectar_senales(self) -> None:
        self.control_buscador.textChanged.connect(
            self.actualizar_datos
        )
        self.control_filtro.currentTextChanged.connect(
            self.actualizar_datos
        )

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
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
                padding: 0 10px;
            }
            QLineEdit#controlBuscador:focus {
                border: 1px solid #3b82f6;
            }
            QComboBox#controlFiltro {
                color: palette(window-text);
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
                padding: 0 10px;
                min-height: 26px;
            }
            QPushButton#controlNuevo {
                color: #ffffff;
                background-color: #3b82f6;
                border: none;
                border-radius: 6px;
                padding: 0 14px;
                min-height: 28px;
                font-weight: 600;
            }
            QPushButton#controlNuevo:hover {
                background-color: #2f6fe0;
            }
            QPushButton#controlNuevo:pressed {
                background-color: #2861c9;
            }
            QTableWidget#pedidosTable {
                background-color: palette(base);
                alternate-background-color: palette(base);
                color: palette(text);
                border: 1px solid palette(mid);
                border-radius: 10px;
                padding: 0;
                selection-background-color: #2f5c9e;
                selection-color: #ffffff;
            }
            QTableWidget#pedidosTable::item {
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
                padding: 0 10px;
            }
            QTableWidget#pedidosTable::item:selected {
                background-color: #2f5c9e;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: palette(button);
                color: palette(button-text);
                border: none;
                border-bottom: 1px solid palette(mid);
                padding: 8px 10px;
                font-size: 13px;
                font-weight: 600;
            }
            """
        )

    def _ajustar_altura_tabla(self) -> None:
        """Ajusta la altura de la tabla al número de filas mostradas."""
        tabla = self.pedidos_lista
        alto_encabezado = max(
            tabla.horizontalHeader().height(),
            tabla.horizontalHeader().minimumHeight(),
        )
        alto_filas = tabla.verticalHeader().defaultSectionSize() * tabla.rowCount()
        marco = 2 * tabla.frameWidth()
        tabla.setFixedHeight(alto_encabezado + alto_filas + marco)

    def actualizar_datos(self) -> None:
        pedidos_lista = obtener_pedidos()
        pedidos_filtrados = self._filtrar_pedidos(pedidos_lista)

        pedidos_mostrados = pedidos_filtrados[-8:]
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

        self._ajustar_altura_tabla()
