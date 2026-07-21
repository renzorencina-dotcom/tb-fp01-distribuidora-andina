from PySide6.QtWidgets import (
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

        self.setWindowTitle("Distribuidora Andina Fresh")
        self.resize(800, 500)

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

        sidebar = self._crear_sidebar()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        self.setCentralWidget(central_widget)

    def _crear_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)

        boton_dashboard = QPushButton("Dashboard")
        boton_pedidos = QPushButton("Pedidos")
        boton_clientes = QPushButton("Clientes")
        boton_stocks = QPushButton("Stock")
        boton_reportes = QPushButton("Reportes")

        boton_dashboard.clicked.connect(self._mostrar_dashboard)
        boton_pedidos.clicked.connect(self._mostrar_pedidos)
        boton_clientes.clicked.connect(lambda:self.pages.setCurrentIndex(2))
        boton_stocks.clicked.connect(lambda:self.pages.setCurrentIndex(3))
        boton_reportes.clicked.connect(lambda:self.pages.setCurrentIndex(4))

        sidebar_layout.addWidget(boton_dashboard)
        sidebar_layout.addWidget(boton_pedidos)
        sidebar_layout.addWidget(boton_clientes)
        sidebar_layout.addWidget(boton_stocks)
        sidebar_layout.addWidget(boton_reportes)
        sidebar_layout.addStretch()

        return sidebar

    def _mostrar_dashboard(self) -> None:
        self.dashboard.actualizar_datos()
        self.pages.setCurrentIndex(0)

    def _mostrar_pedidos(self) -> None:
        self.dashboard.actualizar_datos()
        self.pages.setCurrentIndex(1)
