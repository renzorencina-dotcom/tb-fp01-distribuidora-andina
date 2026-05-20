from utils.csv_manager import leer_csv


RUTA_PEDIDOS = "data/pedidos.csv"
RUTA_DETALLE_PEDIDOS = "data/detalle_pedidos.csv"
RUTA_PRODUCTOS = "data/productos.csv"

ESTADOS_PEDIDO = [
    "Pedido registrado",
    "Pedido recibido",
    "Pedido pendiente",
    "Pedido atendido parcialmente",
    "Pedido atendido",
    "Pedido cancelado",
]

ESTADOS_PEDIDOS_EN_CURSO = [
    "Pedido registrado",
    "Pedido recibido",
    "Pedido pendiente",
]


def convertir_a_numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0


def formatear_numero(valor):
    valor = float(valor)

    if valor.is_integer():
        return int(valor)

    return round(valor, 2)


def obtener_reporte_general_pedidos():
    pedidos = leer_csv(RUTA_PEDIDOS)
    reporte = {
        "total_pedidos": len(pedidos),
    }

    for estado in ESTADOS_PEDIDO:
        reporte[estado] = 0

    for pedido in pedidos:
        estado = pedido.get("estado", "")

        if estado in reporte:
            reporte[estado] += 1

    return reporte


def obtener_pedidos_por_estado(estado):
    pedidos = leer_csv(RUTA_PEDIDOS)

    return [
        {
            "codigo_pedido": pedido.get("codigo_pedido", ""),
            "ruc_cliente": pedido.get("ruc_cliente", ""),
            "razon_social": pedido.get("razon_social", ""),
            "estado": pedido.get("estado", ""),
        }
        for pedido in pedidos
        if pedido.get("estado") == estado
    ]


def obtener_productos_bajo_stock(limite=5):
    productos = leer_csv(RUTA_PRODUCTOS)
    limite = convertir_a_numero(limite)
    productos_bajo_stock = []

    for producto in productos:
        stock = convertir_a_numero(producto.get("stock"))

        if stock <= limite:
            productos_bajo_stock.append(
                {
                    "id_producto": producto.get("id_producto", ""),
                    "descripcion": producto.get("descripcion", ""),
                    "tipo": producto.get("tipo", ""),
                    "stock": formatear_numero(stock),
                    "precio_unitario": convertir_a_numero(
                        producto.get("precio_unitario")
                    ),
                }
            )

    return productos_bajo_stock


def obtener_producto_mas_solicitado():
    detalles = leer_csv(RUTA_DETALLE_PEDIDOS)

    if len(detalles) == 0:
        return None

    productos_solicitados = {}

    for detalle in detalles:
        id_producto = detalle.get("id_producto", "")

        if not id_producto:
            continue

        if id_producto not in productos_solicitados:
            productos_solicitados[id_producto] = {
                "id_producto": id_producto,
                "descripcion": detalle.get("descripcion", ""),
                "cantidad_total": 0,
            }

        productos_solicitados[id_producto]["cantidad_total"] += convertir_a_numero(
            detalle.get("cantidad")
        )

    if len(productos_solicitados) == 0:
        return None

    producto_mas_solicitado = max(
        productos_solicitados.values(),
        key=lambda producto: producto["cantidad_total"],
    )
    producto_mas_solicitado["cantidad_total"] = formatear_numero(
        producto_mas_solicitado["cantidad_total"]
    )

    return producto_mas_solicitado


def obtener_clientes_con_pedidos_en_curso():
    pedidos = leer_csv(RUTA_PEDIDOS)
    clientes = {}

    for pedido in pedidos:
        if pedido.get("estado") not in ESTADOS_PEDIDOS_EN_CURSO:
            continue

        ruc_cliente = pedido.get("ruc_cliente", "")

        if not ruc_cliente:
            continue

        if ruc_cliente not in clientes:
            clientes[ruc_cliente] = {
                "ruc_cliente": ruc_cliente,
                "razon_social": pedido.get("razon_social", ""),
                "cantidad_pedidos_en_curso": 0,
            }

        clientes[ruc_cliente]["cantidad_pedidos_en_curso"] += 1

    return list(clientes.values())
