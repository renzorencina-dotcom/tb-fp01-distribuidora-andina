# Distribuidora Andina Fresh S.A.C.

Sistema de consola en Python para gestionar clientes, productos, pedidos,
stock y reportes de una distribuidora.

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
- CSV como almacenamiento local
- PyCharm
- Git y GitHub
- Tkinter como módulo reservado para futura interfaz gráfica

## Estructura general
- `main.py`: punto de entrada del sistema.
- `models/`: clases que representan entidades del dominio.
- `services/`: lógica de negocio y acceso a datos mediante utilidades CSV.
- `ui/`: interfaz de consola y módulo reservado para GUI.
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
de ejemplo en `data/ejemplos/`.

## Ejecución
```bash
python3 main.py
```

## Integrantes
- Gino Aquino
- Renzo Encina
- Sommer Rios
