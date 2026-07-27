from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.qt.pages.dashboard_page import DashboardPage
from ui.qt.pages.clientes_page import ClientesPage
from ui.qt.pages.pedidos_page import PedidosPage
from ui.qt.pages.reportes_page import ReportesPage
from ui.qt.pages.stock_page import StockPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("AnsERP")
        self.resize(1000, 600)

        self.pages = QStackedWidget()

        self._crear_paginas()
        self._configurar_interfaz()

    def _crear_paginas(self) -> None:
        self.dashboard = DashboardPage()
        self.pedidos = PedidosPage()
        clientes = ClientesPage()
        stock = StockPage()
        reportes = ReportesPage()

        self.pages.addWidget(self.dashboard)
        self.pages.addWidget(self.pedidos)
        self.pages.addWidget(clientes)
        self.pages.addWidget(stock)
        self.pages.addWidget(reportes)

    def _configurar_interfaz(self) -> None:
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self._crear_sidebar()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        self.setCentralWidget(central_widget)

    def _crear_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(180)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 16)
        sidebar_layout.setSpacing(6)

        boton_dashboard = QPushButton("Dashboard")
        boton_pedidos = QPushButton("Pedidos")
        boton_clientes = QPushButton("Clientes")
        boton_stocks = QPushButton("Stock")
        boton_reportes = QPushButton("Reportes")

        botones = [
            boton_dashboard,
            boton_pedidos,
            boton_clientes,
            boton_stocks,
            boton_reportes,
        ]

        # Grupo exclusivo: el botón de la página activa queda resaltado.
        self._grupo_navegacion = QButtonGroup(self)
        self._grupo_navegacion.setExclusive(True)

        for boton in botones:
            boton.setObjectName("navButton")
            boton.setCheckable(True)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            self._grupo_navegacion.addButton(boton)

        boton_dashboard.setChecked(True)

        boton_dashboard.clicked.connect(self._mostrar_dashboard)
        boton_pedidos.clicked.connect(self._mostrar_pedidos)
        boton_clientes.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        boton_stocks.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        boton_reportes.clicked.connect(lambda: self.pages.setCurrentIndex(4))

        for boton in botones:
            sidebar_layout.addWidget(boton)
        sidebar_layout.addStretch()

        sidebar.setStyleSheet(
            """
            QWidget#sidebar {
                background-color: palette(base);
                border-right: 1px solid palette(mid);
            }
            QPushButton#navButton {
                color: palette(window-text);
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton#navButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
            QPushButton#navButton:checked {
                background-color: #3b82f6;
                color: #ffffff;
                font-weight: 600;
            }
            """
        )

        return sidebar

    def _mostrar_dashboard(self) -> None:
        self.dashboard.actualizar_datos()
        self.pages.setCurrentIndex(0)

    def _mostrar_pedidos(self) -> None:
        self.pedidos.actualizar_datos()
        self.pages.setCurrentIndex(1)
