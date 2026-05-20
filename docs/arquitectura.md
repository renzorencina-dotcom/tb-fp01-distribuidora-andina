# Arquitectura del Sistema

## Visión General
El sistema está organizado por capas simples para separar responsabilidades:

- `ui/`: interacción con el usuario desde consola.
- `services/`: reglas de negocio y coordinación de operaciones.
- `models/`: representación de entidades del sistema.
- `utils/`: utilidades compartidas de validación y manejo CSV.
- `data/`: archivos CSV de trabajo generados durante la ejecución.

`main.py` es el punto de entrada y delega el control a `ui/consola.py`.

## Flujo General
1. El usuario inicia el sistema desde `main.py`.
2. `ui/consola.py` muestra el menú principal y los submenús.
3. La interfaz solicita datos, valida entradas básicas y llama a servicios.
4. Los servicios aplican reglas de negocio y usan `utils/csv_manager.py`.
5. Los datos se guardan o consultan desde archivos CSV.

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

## Utilidades
`csv_manager.py` centraliza lectura, escritura, búsqueda y eliminación de filas
CSV. Esto evita repetir lógica de archivos en cada servicio.

`validaciones.py` agrupa reglas de entrada como RUC, teléfono, tipo de producto,
stock, precio e identificadores de productos.

## Datos
Los archivos `data/*.csv` son datos de trabajo y no se versionan. Los archivos
de ejemplo ubicados en `data/ejemplos/` documentan los encabezados esperados por
el sistema.
