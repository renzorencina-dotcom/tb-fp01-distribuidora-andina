# AnsERP

> **Nombre provisional.** "AnsERP" es un nombre tentativo mientras el proyecto
> toma forma; puede cambiar más adelante.

AnsERP es un proyecto personal en Python: un sistema de gestión que empieza
pequeño, con la aspiración de crecer hacia un ERP. Se construye alrededor del
caso de una distribuidora y administra clientes, productos, pedidos, stock y
reportes. El proyecto evoluciona desde una interfaz de consola completa hacia
una interfaz gráfica en PySide6/Qt6, cuyas páginas de Dashboard y Pedidos ya
presentan datos reales.

## Alcance actual
El sistema permite:

- Registrar, consultar y eliminar clientes.
- Registrar, consultar, eliminar y actualizar productos en stock.
- Registrar pedidos con cabecera y detalle de productos.
- Cancelar pedidos y actualizar sus estados.
- Descontar stock cuando un pedido pasa a `Pedido atendido`.
- Generar reportes desde la información almacenada en CSV.

## Tecnologías
- Python 3
- PySide6 / Qt6 para la interfaz gráfica actual
- CSV como almacenamiento local
- PyCharm
- Git y GitHub

## Estructura general
- `main.py`: punto de entrada de la interfaz de consola.
- `qt_main.py`: punto de entrada de la interfaz gráfica PySide6/Qt6.
- `config.py`: rutas centralizadas de los archivos CSV.
- `models/`: clases que representan entidades del dominio.
- `services/`: lógica de negocio y acceso a datos mediante utilidades CSV.
- `ui/`: interfaces de usuario de consola y gráficas.
- `ui/qt/`: ventana principal y páginas de la interfaz Qt.
- `utils/`: validaciones, formateo de números y utilidades para archivos CSV.
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
- `PedidosPage`: muestra una tabla con los últimos pedidos registrados,
  obtenidos desde `services/pedido_service.py`. Sus controles de búsqueda y
  filtro todavía no operan sobre los datos.
- `ClientesPage`, `StockPage` y `ReportesPage`: páginas presentes en la
  navegación, actualmente limitadas a un título informativo. No ofrecen todavía
  operaciones de registro, búsqueda, atención, cancelación o edición.

## Instalación
Crear y activar un entorno virtual, luego instalar las dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
Interfaz de consola:

```bash
python3 main.py
```

Interfaz gráfica PySide6/Qt6:

```bash
python3 qt_main.py
```