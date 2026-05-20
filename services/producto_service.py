"""Lógica de negocio para productos e inventario."""

from models.producto import Producto
from services.inventario_service import descontar_stock, sumar_stock
from utils.csv_manager import (
    buscar_por_campo,
    eliminar_fila_csv,
    escribir_csv,
    leer_csv,
)
from utils.validaciones import (
    id_producto_valido,
    precio_unitario_valido,
    stock_valido,
    texto_no_vacio,
    tipo_producto_valido,
)


RUTA_PRODUCTOS = "data/productos.csv"
CAMPOS_PRODUCTO = [
    "id_producto",
    "descripcion",
    "tipo",
    "stock",
    "precio_unitario",
]


def formatear_numero(valor):
    """Devuelve números sin decimales innecesarios para guardarlos en CSV."""
    valor = float(valor)

    if valor.is_integer():
        return str(int(valor))

    return str(valor)


def normalizar_tipo(tipo):
    """Normaliza el tipo de producto para comparar perecible y abarrote."""
    return tipo.strip().lower()


def convertir_fila_a_producto(fila):
    """Convierte una fila del CSV de productos en un objeto Producto."""
    return Producto(
        fila["id_producto"],
        fila["descripcion"],
        fila["tipo"],
        float(fila["stock"]),
        float(fila["precio_unitario"]),
    )


def convertir_producto_a_fila(producto):
    """Convierte un Producto en diccionario listo para escribirse en CSV."""
    return {
        "id_producto": producto.id_producto,
        "descripcion": producto.descripcion,
        "tipo": producto.tipo,
        "stock": formatear_numero(producto.stock),
        "precio_unitario": formatear_numero(producto.precio_unitario),
    }


def listar_productos():
    """Obtiene todos los productos registrados en el archivo CSV."""
    return [convertir_fila_a_producto(fila) for fila in leer_csv(RUTA_PRODUCTOS)]


def guardar_productos(productos):
    """Guarda la lista completa de productos después de una actualización."""
    filas = [convertir_producto_a_fila(producto) for producto in productos]
    escribir_csv(RUTA_PRODUCTOS, filas, CAMPOS_PRODUCTO)


def validar_datos_producto(id_producto, descripcion, tipo, stock, precio_unitario):
    """Valida los datos requeridos para registrar o actualizar un producto."""
    if not texto_no_vacio(id_producto):
        return False, "El ID del producto no puede estar vacío."

    if not texto_no_vacio(descripcion):
        return False, "La descripción del producto no puede estar vacía."

    if not tipo_producto_valido(tipo):
        return False, "El tipo de producto debe ser perecible o abarrote."

    if not id_producto_valido(id_producto, tipo):
        if normalizar_tipo(tipo) == "perecible":
            return False, "El ID de un producto perecible debe iniciar con PER-."

        return False, "El ID de un producto abarrote debe iniciar con ABA-."

    if not stock_valido(stock, tipo):
        return False, "El stock ingresado no es válido."

    if not precio_unitario_valido(precio_unitario):
        return False, "El precio unitario debe ser mayor que cero."

    return True, ""


def buscar_producto_por_id(id_producto):
    """Busca un producto por ID normalizando el código a mayúsculas."""
    fila = buscar_por_campo(RUTA_PRODUCTOS, "id_producto", id_producto.strip().upper())

    if fila is None:
        return None

    return convertir_fila_a_producto(fila)


def consultar_producto(id_producto):
    """Consulta un producto por ID y devuelve estado, objeto y mensaje."""
    producto = buscar_producto_por_id(id_producto)

    if producto is None:
        return False, None, "Producto no encontrado."

    return True, producto, "Producto encontrado."


def registrar_producto(id_producto, descripcion, tipo, stock, precio_unitario):
    """Registra un producto nuevo o suma stock si el producto ya existe."""
    id_producto = id_producto.strip().upper()
    descripcion = descripcion.strip()
    tipo = normalizar_tipo(tipo)
    stock = stock.strip()
    precio_unitario = precio_unitario.strip()

    es_valido, mensaje = validar_datos_producto(
        id_producto,
        descripcion,
        tipo,
        stock,
        precio_unitario,
    )

    if not es_valido:
        return False, None, mensaje

    producto_existente = buscar_producto_por_id(id_producto)

    # Si el producto ya existe, no se duplica la fila: se suma el stock
    # ingresado al registro existente para mantener un único inventario por ID.
    if producto_existente is not None:
        return agregar_stock(id_producto, stock)

    producto = Producto(
        id_producto,
        descripcion,
        tipo,
        float(stock),
        float(precio_unitario),
    )
    productos = listar_productos()
    productos.append(producto)
    guardar_productos(productos)
    return True, producto, "Producto registrado correctamente."


def eliminar_producto(id_producto):
    """Elimina un producto del inventario usando su ID."""
    fila_eliminada = eliminar_fila_csv(
        RUTA_PRODUCTOS,
        "id_producto",
        id_producto.strip().upper(),
        CAMPOS_PRODUCTO,
    )

    if fila_eliminada is None:
        return False, None, "Producto no encontrado."

    return True, convertir_fila_a_producto(fila_eliminada), "Producto eliminado correctamente."


def actualizar_stock(id_producto, nuevo_stock):
    """Reemplaza el stock completo de un producto existente."""
    producto = buscar_producto_por_id(id_producto)

    if producto is None:
        return False, None, "Producto no encontrado."

    if not stock_valido(nuevo_stock, producto.tipo):
        return False, None, "El stock ingresado no es válido."

    productos = listar_productos()

    # Se recorre la lista cargada desde CSV para modificar solo el producto
    # encontrado antes de reescribir el inventario completo.
    for producto_actual in productos:
        if producto_actual.id_producto == producto.id_producto:
            producto_actual.stock = float(nuevo_stock)
            producto = producto_actual
            break

    guardar_productos(productos)
    return True, producto, "Stock actualizado correctamente."


def agregar_stock(id_producto, cantidad):
    """Suma una cantidad al stock actual de un producto."""
    producto = buscar_producto_por_id(id_producto)

    if producto is None:
        return False, None, "Producto no encontrado."

    if not stock_valido(cantidad, producto.tipo):
        return False, None, "La cantidad ingresada no es válida."

    productos = listar_productos()

    # La suma usa inventario_service para mantener aislada la operación
    # aritmética del manejo de archivos CSV.
    for producto_actual in productos:
        if producto_actual.id_producto == producto.id_producto:
            producto_actual.stock = sumar_stock(producto_actual.stock, float(cantidad))
            producto = producto_actual
            break

    guardar_productos(productos)
    return True, producto, "Producto existente. Stock actualizado correctamente."


def restar_stock(id_producto, cantidad):
    """Resta stock evitando que el inventario quede en negativo."""
    producto = buscar_producto_por_id(id_producto)

    if producto is None:
        return False, None, "Producto no encontrado."

    if not stock_valido(cantidad, producto.tipo):
        return False, None, "La cantidad ingresada no es válida."

    productos = listar_productos()

    # Si descontar_stock devuelve None, la operación se detiene para impedir
    # que el producto quede con stock negativo.
    for producto_actual in productos:
        if producto_actual.id_producto == producto.id_producto:
            nuevo_stock = descontar_stock(producto_actual.stock, float(cantidad))

            if nuevo_stock is None:
                return False, None, "No hay stock suficiente para restar esa cantidad."

            producto_actual.stock = nuevo_stock
            producto = producto_actual
            break

    guardar_productos(productos)
    return True, producto, "Stock descontado correctamente."


def descontar_stock_por_detalles(detalles):
    """Descuenta stock para todos los productos incluidos en un pedido."""
    productos = listar_productos()
    # Diccionario auxiliar para buscar productos por ID sin recorrer toda la
    # lista de inventario por cada detalle del pedido.
    productos_por_id = {
        producto.id_producto.strip().upper(): producto
        for producto in productos
    }
    productos_actualizados = []

    for detalle in detalles:
        id_producto = detalle.id_producto.strip().upper()
        producto = productos_por_id.get(id_producto)

        if producto is None:
            return False, [], f"Producto {id_producto} no encontrado."

        cantidad = float(detalle.cantidad)

        if cantidad <= 0:
            return False, [], f"La cantidad del producto {id_producto} no es válida."

        # Los abarrotes se manejan en unidades enteras; los perecibles pueden
        # aceptar cantidades decimales.
        if producto.tipo.strip().lower() == "abarrote" and not cantidad.is_integer():
            return False, [], f"La cantidad del producto {id_producto} debe ser entera."

        nuevo_stock = descontar_stock(producto.stock, cantidad)

        if nuevo_stock is None:
            return False, [], f"Stock insuficiente para atender el producto {id_producto}."

        producto.stock = nuevo_stock
        productos_actualizados.append(producto)

    guardar_productos(productos)
    return True, productos_actualizados, "Stock descontado correctamente."
