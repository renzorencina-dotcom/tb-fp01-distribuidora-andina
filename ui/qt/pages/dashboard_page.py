from services.reporte_service import (
    obtener_reporte_general_pedidos,
    obtener_productos_bajo_stock,
    obtener_pedidos_recientes)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        titulo = QLabel("Resumen general")
        layout.addWidget(titulo)

        tarjetas_layout = QHBoxLayout()

        tarjeta_total, self.total_pedidos_label = self._crear_tarjeta("Pedidos")
        tarjeta_pendientes, self.pedidos_pendientes_label = self._crear_tarjeta("Pendientes")
        tarjeta_stock_bajo, self.stock_bajo_label = self._crear_tarjeta("Stock bajo")

        tarjetas_layout.addWidget(tarjeta_total)
        tarjetas_layout.addWidget(tarjeta_pendientes)
        tarjetas_layout.addWidget(tarjeta_stock_bajo)
        tarjetas_layout.addStretch()

        layout.addLayout(tarjetas_layout)

        subtitulo = QLabel("Pedidos recientes")
        layout.addWidget(subtitulo)

        self.pedidos_recientes = QTableWidget(3, 4)

        self.pedidos_recientes.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.pedidos_recientes.setHorizontalHeaderLabels(
            ["Código", "RUC", "Cliente", "Estado"]
        )
        self.pedidos_recientes.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Fixed
        )

        self.pedidos_recientes.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

        self.pedidos_recientes.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )

        self.pedidos_recientes.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Fixed
        )

        self.pedidos_recientes.setColumnWidth(0,80)
        self.pedidos_recientes.setColumnWidth(3,160)

        self.pedidos_recientes.setMaximumHeight(400)

        self.pedidos_recientes.verticalHeader().setDefaultSectionSize(40)


        layout.addWidget(self.pedidos_recientes)

        self.actualizar_datos()

        layout.addStretch()

    def _crear_tarjeta(self, texto: str) -> tuple[QFrame, QLabel]:
        tarjeta = QFrame()
        tarjeta.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(tarjeta)

        valor_label = QLabel()
        texto_label = QLabel(texto)

        layout.addWidget(valor_label)
        layout.addWidget(texto_label)

        return tarjeta, valor_label

    def actualizar_datos(self) -> None:
        reporte = obtener_reporte_general_pedidos()
        stock = obtener_productos_bajo_stock()
        pedidos_recientes = obtener_pedidos_recientes()


        self.total_pedidos_label.setText(
            str(reporte["total_pedidos"])
        )

        self.pedidos_pendientes_label.setText(
            str(reporte["Pedido pendiente"])
        )

        self.stock_bajo_label.setText(
            str(len(stock))
        )

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
                self.pedidos_recientes.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(str(valor)),
                )