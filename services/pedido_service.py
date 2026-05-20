from models.pedido import DetallePedido, Pedido
from services.producto_service import descontar_stock_por_detalles
from utils.csv_manager import agregar_fila_csv, buscar_por_campo, escribir_csv, leer_csv


RUTA_PEDIDOS = "data/pedidos.csv"
RUTA_DETALLE_PEDIDOS = "data/detalle_pedidos.csv"

CAMPOS_PEDIDO = [
    "codigo_pedido",
    "ruc_cliente",
    "razon_social",
    "estado",
]

CAMPOS_DETALLE_PEDIDO = [
    "codigo_pedido",
    "id_producto",
    "descripcion",
    "cantidad",
    "precio_unitario",
    "subtotal",
]


def formatear_numero(valor):
    valor = float(valor)

    if valor.is_integer():
        return str(int(valor))

    return str(valor)


def convertir_fila_a_pedido(fila):
    return Pedido(
        fila["codigo_pedido"],
        fila["ruc_cliente"],
        fila["razon_social"],
        fila.get("estado") or "Pedido registrado",
    )


def convertir_fila_a_detalle_pedido(fila):
    return DetallePedido(
        fila["codigo_pedido"],
        fila["id_producto"],
        fila["descripcion"],
        float(fila["cantidad"]),
        float(fila["precio_unitario"]),
    )


def convertir_pedido_a_fila(pedido):
    return {
        "codigo_pedido": pedido.codigo_pedido,
        "ruc_cliente": pedido.ruc_cliente,
        "razon_social": pedido.razon_social,
        "estado": pedido.estado,
    }


def convertir_detalle_a_fila(detalle):
    return {
        "codigo_pedido": detalle.codigo_pedido,
        "id_producto": detalle.id_producto,
        "descripcion": detalle.descripcion,
        "cantidad": formatear_numero(detalle.cantidad),
        "precio_unitario": formatear_numero(detalle.precio_unitario),
        "subtotal": formatear_numero(detalle.subtotal),
    }


def convertir_detalle_desde_diccionario(detalle):
    return DetallePedido(
        detalle["codigo_pedido"],
        detalle["id_producto"],
        detalle["descripcion"],
        float(detalle["cantidad"]),
        float(detalle["precio_unitario"]),
    )


def normalizar_detalle(detalle):
    if isinstance(detalle, DetallePedido):
        return detalle

    return convertir_detalle_desde_diccionario(detalle)


def buscar_pedido_por_codigo(codigo_pedido):
    fila = buscar_por_campo(RUTA_PEDIDOS, "codigo_pedido", codigo_pedido)

    if fila is None:
        return None

    return convertir_fila_a_pedido(fila)


def codigo_pedido_existe(codigo_pedido):
    return buscar_pedido_por_codigo(codigo_pedido) is not None


def actualizar_estado_pedido(codigo_pedido, nuevo_estado):
    pedidos = leer_csv(RUTA_PEDIDOS)
    pedido_actualizado = None

    for pedido in pedidos:
        if pedido.get("codigo_pedido") == codigo_pedido:
            pedido["estado"] = nuevo_estado
            pedido_actualizado = convertir_fila_a_pedido(pedido)
            break

    if pedido_actualizado is None:
        return False, None, "Pedido no encontrado."

    escribir_csv(RUTA_PEDIDOS, pedidos, CAMPOS_PEDIDO)
    return True, pedido_actualizado, "Estado del pedido actualizado correctamente."


def obtener_detalles_por_codigo(codigo_pedido):
    return [
        convertir_fila_a_detalle_pedido(fila)
        for fila in leer_csv(RUTA_DETALLE_PEDIDOS)
        if fila.get("codigo_pedido") == codigo_pedido
    ]


def atender_pedido(codigo_pedido):
    pedido = buscar_pedido_por_codigo(codigo_pedido)

    if pedido is None:
        return False, None, "Pedido no encontrado."

    if pedido.estado == "Pedido atendido":
        return False, pedido, "Este pedido ya fue atendido y el stock ya fue descontado."

    if pedido.estado == "Pedido cancelado":
        return False, pedido, "No se puede actualizar el estado de este pedido porque ha sido cancelado."

    detalles = obtener_detalles_por_codigo(codigo_pedido)

    if len(detalles) == 0:
        return False, pedido, "No se encontraron productos registrados para este pedido."

    fue_descontado, _, mensaje_stock = descontar_stock_por_detalles(detalles)

    if not fue_descontado:
        return False, pedido, mensaje_stock

    return actualizar_estado_pedido(codigo_pedido, "Pedido atendido")


def registrar_cabecera_pedido(
    codigo_pedido,
    ruc_cliente,
    razon_social,
    estado="Pedido registrado",
):
    if codigo_pedido_existe(codigo_pedido):
        pedido = buscar_pedido_por_codigo(codigo_pedido)
        return False, pedido, "Ya existe un pedido registrado con ese código."

    pedido = Pedido(codigo_pedido, ruc_cliente, razon_social, estado)
    agregar_fila_csv(RUTA_PEDIDOS, convertir_pedido_a_fila(pedido), CAMPOS_PEDIDO)
    return True, pedido, "Cabecera de pedido registrada correctamente."


def registrar_detalle_pedido(codigo_pedido, detalles):
    detalles_normalizados = []

    for detalle in detalles:
        detalle_normalizado = normalizar_detalle(detalle)
        detalle_normalizado.codigo_pedido = codigo_pedido
        detalles_normalizados.append(detalle_normalizado)

    filas_existentes = leer_csv(RUTA_DETALLE_PEDIDOS)
    filas_nuevas = [
        convertir_detalle_a_fila(detalle)
        for detalle in detalles_normalizados
    ]

    escribir_csv(
        RUTA_DETALLE_PEDIDOS,
        filas_existentes + filas_nuevas,
        CAMPOS_DETALLE_PEDIDO,
    )
    return True, detalles_normalizados, "Detalle de pedido registrado correctamente."


def obtener_pedidos():
    return [
        convertir_fila_a_pedido(fila)
        for fila in leer_csv(RUTA_PEDIDOS)
    ]


def obtener_detalles_pedidos():
    return [
        convertir_fila_a_detalle_pedido(fila)
        for fila in leer_csv(RUTA_DETALLE_PEDIDOS)
    ]
