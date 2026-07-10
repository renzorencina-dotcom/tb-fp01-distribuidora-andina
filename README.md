# Distribuidora Andina Fresh S.A.C.

Sistema en Python para gestionar clientes, productos, pedidos, stock y reportes
de una distribuidora. El proyecto mantiene la interfaz de consola e incorpora
una interfaz gráfica en PySide6/Qt6 cuyo Dashboard ya presenta datos reales.

## Objetivo
Desarrollar un sistema que permita:

- Registrar, consultar y eliminar clientes.
- Registrar, consultar, eliminar y actualizar productos en stock.
- Registrar pedidos con cabecera y detalle de productos.
- Cancelar pedidos y actualizar sus estados.
- Descontar stock cuando un pedido pasa a `Pedido atendido`.
- Generar reportes básicos desde la información almacenada en CSV.

## Tecnologías
- Python 3
- PySide6 / Qt6 para la interfaz gráfica actual
- CSV como almacenamiento local
- PyCharm
- Git y GitHub

## Estructura general
- `main.py`: punto de entrada de la interfaz de consola.
- `qt_main.py`: punto de entrada de la interfaz gráfica PySide6/Qt6.
- `models/`: clases que representan entidades del dominio.
- `services/`: lógica de negocio y acceso a datos mediante utilidades CSV.
- `ui/`: interfaces de usuario de consola y gráficas.
- `ui/qt/`: ventana principal y páginas de la interfaz Qt.
- `utils/`: validaciones y funciones reutilizables para archivos CSV.
- `data/`: archivos CSV de trabajo generados durante la ejecución.
- `data/ejemplos/`: encabezados de ejemplo versionados para los CSV.
- `docs/`: documentación técnica del proyecto.

## Módulos
- **Clientes:** registro, consulta y eliminación por RUC.
- **Stock:** registro de productos, actualización de cantidades y consulta.
- **Pedidos:** registro de cabecera y detalle, cancelación, consulta y cambio de estado.
- **Reportes:** resumen de pedidos, pedidos por estado, bajo stock, producto más solicitado y clientes con pedidos en curso.

## Datos CSV
Los CSV reales dentro de `data/*.csv` se consideran archivos de trabajo y no se
versionan. Para conservar la estructura esperada, el proyecto incluye archivos
de ejemplo en `data/ejemplos/`. Esta persistencia continúa basada en CSV: la
interfaz gráfica no lee esos archivos directamente, sino que obtiene los datos
mediante la capa `services/`.

## Interfaz gráfica Qt
`qt_main.py` crea la aplicación Qt y abre `MainWindow`, definida en
`ui/qt/main_window.py`. La ventana organiza la navegación lateral y un
`QStackedWidget` con estas páginas:

- `DashboardPage`: página funcional que consume `services/reporte_service.py`.
  Muestra tarjetas con el total de pedidos, pedidos pendientes y productos con
  stock bajo, además de una tabla con los tres pedidos más recientes.
- `PedidosPage`, `ClientesPage`, `StockPage` y `ReportesPage`: páginas presentes
  en la navegación, actualmente limitadas a un título informativo. No ofrecen
  todavía operaciones de registro, búsqueda, atención, cancelación o edición.

## Ejecución
Interfaz de consola:

```bash
python3 main.py
```

Interfaz gráfica PySide6/Qt6:

```bash
python3 qt_main.py
```