from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.reporte_service import (
    obtener_pedidos_recientes,
    obtener_productos_bajo_stock,
    obtener_reporte_general_pedidos,
)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dashboardPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        titulo = QLabel("Resumen general")
        titulo.setObjectName("pageTitle")
        layout.addWidget(titulo)

        tarjetas_layout = QHBoxLayout()
        tarjetas_layout.setSpacing(16)

        tarjeta_total, self.total_pedidos_label = self._crear_tarjeta("Pedidos")
        tarjeta_pendientes, self.pedidos_pendientes_label = self._crear_tarjeta(
            "Pendientes"
        )
        tarjeta_stock_bajo, self.stock_bajo_label = self._crear_tarjeta(
            "Stock bajo"
        )

        tarjetas_layout.addWidget(tarjeta_total, 1)
        tarjetas_layout.addWidget(tarjeta_pendientes, 1)
        tarjetas_layout.addWidget(tarjeta_stock_bajo, 1)

        layout.addLayout(tarjetas_layout)

        subtitulo = QLabel("Pedidos recientes")
        subtitulo.setObjectName("sectionTitle")
        layout.addWidget(subtitulo)

        self.pedidos_recientes = QTableWidget(0, 4)
        self.pedidos_recientes.setObjectName("recentOrdersTable")

        self.pedidos_recientes.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.pedidos_recientes.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.pedidos_recientes.setAlternatingRowColors(True)
        self.pedidos_recientes.setShowGrid(False)
        self.pedidos_recientes.setWordWrap(False)

        self.pedidos_recientes.setHorizontalHeaderLabels(
            ["Código", "RUC", "Cliente", "Estado"]
        )
        encabezado = self.pedidos_recientes.horizontalHeader()
        encabezado.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        encabezado.setMinimumHeight(42)
        encabezado.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        encabezado.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        encabezado.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

        self.pedidos_recientes.setColumnWidth(0, 100)
        self.pedidos_recientes.setColumnWidth(1, 130)
        self.pedidos_recientes.setColumnWidth(3, 190)

        self.pedidos_recientes.setMinimumHeight(210)
        self.pedidos_recientes.setMaximumHeight(400)
        self.pedidos_recientes.verticalHeader().setVisible(False)
        self.pedidos_recientes.verticalHeader().setDefaultSectionSize(44)

        layout.addWidget(self.pedidos_recientes)

        self.actualizar_datos()

        layout.addStretch()
        self._aplicar_estilos()

    def _crear_tarjeta(self, texto: str) -> tuple[QFrame, QLabel]:
        tarjeta = QFrame()
        tarjeta.setObjectName("summaryCard")
        tarjeta.setMinimumHeight(112)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)

        valor_label = QLabel("0")
        valor_label.setObjectName("summaryValue")
        texto_label = QLabel(texto)
        texto_label.setObjectName("summaryLabel")

        layout.addWidget(valor_label)
        layout.addWidget(texto_label)
        layout.addStretch()

        return tarjeta, valor_label

    def _aplicar_estilos(self) -> None:
        """Define estilos visuales que respetan la paleta activa de Qt."""
        self.setStyleSheet(
            """
            QWidget#dashboardPage {
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
            QFrame#summaryCard {
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 12px;
            }
            QLabel#summaryValue {
                color: palette(text);
                font-size: 28px;
                font-weight: 700;
            }
            QLabel#summaryLabel {
                color: palette(text);
                font-size: 13px;
                font-weight: 500;
            }
            QTableWidget#recentOrdersTable {
                background-color: palette(base);
                alternate-background-color: palette(alternate-base);
                color: palette(text);
                border: 1px solid palette(mid);
                border-radius: 10px;
                padding: 0;
                selection-background-color: palette(highlight);
                selection-color: palette(highlighted-text);
            }
            QTableWidget#recentOrdersTable::item {
                border: none;
                padding: 0 10px;
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

    def actualizar_datos(self) -> None:
        reporte = obtener_reporte_general_pedidos()
        stock = obtener_productos_bajo_stock()
        pedidos_recientes = obtener_pedidos_recientes()

        self.total_pedidos_label.setText(str(reporte["total_pedidos"]))

        self.pedidos_pendientes_label.setText(str(reporte["Pedido pendiente"]))

        self.stock_bajo_label.setText(str(len(stock)))

        pedidos_mostrados = pedidos_recientes[-3:]
        self.pedidos_recientes.setRowCount(len(pedidos_mostrados))

        for fila, pedido in enumerate(reversed(pedidos_mostrados)):
            datos_pedido = [
                pedido.get("codigo_pedido", ""),
                pedido.get("ruc_cliente", ""),
                pedido.get("razon_social", ""),
                pedido.get("estado", ""),
            ]

            for columna, valor in enumerate(datos_pedido):
                item = QTableWidgetItem(str(valor))
                alineacion = Qt.AlignmentFlag.AlignVCenter

                if columna in (0, 1, 3):
                    alineacion |= Qt.AlignmentFlag.AlignHCenter
                else:
                    alineacion |= Qt.AlignmentFlag.AlignLeft

                item.setTextAlignment(alineacion)
                self.pedidos_recientes.setItem(fila, columna, item)
