# Arquitectura del Sistema

## Visión General
El sistema está organizado por capas simples para separar responsabilidades:

- `ui/`: interfaces de usuario de consola y gráficas.
- `services/`: reglas de negocio y coordinación de operaciones.
- `models/`: representación de entidades del sistema.
- `utils/`: utilidades compartidas de validación, formato y manejo CSV.
- `config.py`: rutas centralizadas de los archivos CSV que usan los servicios.
- `data/`: archivos CSV de trabajo generados durante la ejecución.

Hay dos puntos de entrada: `main.py` delega el flujo de consola a
`ui/consola.py`, mientras que `qt_main.py` inicia `QApplication` y muestra la
interfaz gráfica PySide6/Qt6 mediante `ui/qt/main_window.py`.

## Flujo de consola
1. El usuario inicia el sistema desde `main.py`.
2. `ui/consola.py` muestra el menú principal y los submenús.
3. La interfaz solicita datos, valida entradas básicas y llama a servicios.
4. Los servicios aplican reglas de negocio y usan `utils/csv_manager.py`.
5. Los datos se guardan o consultan desde archivos CSV.

## Interfaz gráfica PySide6/Qt6
La GUI se encuentra en `ui/qt/` y se compone de:

- `main_window.py`: define `MainWindow`, una `QMainWindow` con navegación
  lateral.
- `pages/`: contiene `DashboardPage`, `PedidosPage`, `ClientesPage`,
  `StockPage` y `ReportesPage`.
- `QStackedWidget`: mantiene las cinco páginas y muestra una a la vez según la
  opción seleccionada en la barra lateral.

En el estado actual, `DashboardPage` y `PedidosPage` son las páginas Qt que
presentan información real. `DashboardPage` consume `services/reporte_service.py`
para mostrar tres tarjetas de resumen —total de pedidos, pedidos pendientes y
productos con stock bajo— y una tabla con los tres pedidos más recientes.
`PedidosPage` consume `services/pedido_service.py` para listar los últimos
pedidos registrados. Al abrir cada una desde la barra lateral, `MainWindow`
solicita que sus datos se vuelvan a consultar.

`ClientesPage`, `StockPage` y `ReportesPage` existen dentro del `QStackedWidget`,
pero actualmente solo muestran un título. La GUI todavía no implementa registro,
búsqueda, atención, cancelación ni modificación de pedidos u otras operaciones de
mantenimiento.

## Modelos
- `Cliente`: representa a un cliente identificado por RUC.
- `Producto`: representa un producto del inventario con tipo, stock y precio.
- `Pedido`: representa la cabecera de una orden.
- `DetallePedido`: representa cada producto solicitado dentro de un pedido.

## Servicios
### Clientes
`cliente_service.py` usa el RUC como identificador único. Permite registrar,
consultar y eliminar clientes.

### Productos y Stock
`producto_service.py` administra productos e inventario. La diferencia entre
productos perecibles y abarrotes afecta la validación del stock: los abarrotes
usan cantidades enteras y los perecibles pueden usar decimales.

### Pedidos
`pedido_service.py` separa la cabecera del pedido y sus detalles:

- `pedidos.csv`: código, cliente y estado.
- `detalle_pedidos.csv`: productos, cantidades, precios y subtotales.

Cuando un pedido pasa a `Pedido atendido`, el servicio descuenta stock antes de
actualizar el estado. Si el pedido ya fue atendido o cancelado, no se permite
volver a modificarlo para evitar inconsistencias.

### Reportes
`reporte_service.py` lee los CSV y genera información agregada:

- Conteo general de pedidos por estado.
- Pedidos filtrados por estado.
- Productos con bajo stock.
- Producto más solicitado.
- Clientes con pedidos en curso.
- Listado de pedidos recientes.

El Dashboard utiliza este servicio para sus indicadores y su tabla. La GUI no
accede directamente a los archivos CSV ni replica reglas de negocio.

## Utilidades
`csv_manager.py` centraliza lectura, escritura, búsqueda y eliminación de filas
CSV. Esto evita repetir lógica de archivos en cada servicio.

`validaciones.py` agrupa reglas de entrada como RUC, teléfono, tipo de producto,
stock, precio e identificadores de productos.

`formato.py` ofrece `formatear_numero`, que convierte números a texto sin
decimales innecesarios al escribirlos en los CSV; antes esta función estaba
duplicada en los servicios de pedidos y productos.

## Datos
Los archivos `data/*.csv` son datos de trabajo y no se versionan. Los archivos
de ejemplo ubicados en `data/ejemplos/` documentan los encabezados esperados por
el sistema. La persistencia actual continúa siendo CSV; los servicios usan
`utils/csv_manager.py` como acceso compartido a esos archivos tanto para la
consola como para la información consumida por la GUI.
