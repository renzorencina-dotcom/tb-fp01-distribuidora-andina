import re


def texto_no_vacio(texto):
    return texto.strip() != ""


def ruc_solo_numeros(ruc):
    return ruc.isdigit()


def ruc_valido(ruc):
    ruc = ruc.strip()

    return re.fullmatch(r"^(10|20)\d{9}$", ruc) is not None


def mensaje_error_ruc(ruc):
    ruc = ruc.strip()

    if ruc == "":
        return "El RUC no puede estar vacío."

    if not ruc.isdigit():
        return "El RUC debe contener solo números."

    if len(ruc) != 11:
        return "El RUC debe tener exactamente 11 dígitos."

    if not ruc.startswith("10") and not ruc.startswith("20"):
        return "El RUC debe comenzar con 10 o con 20."

    return ""


def telefono_solo_numeros(telefono):
    telefono = telefono.strip()

    return re.fullmatch(r"(9\d{8}|01\d{7})", telefono) is not None


def mensaje_error_telefono(telefono):
    telefono = telefono.strip()

    if telefono == "":
        return "El teléfono no puede estar vacío."

    if not telefono.isdigit():
        return "El teléfono debe contener solo números."

    if len(telefono) == 7:
        return "Los teléfonos fijos deben comenzar con 01."

    if len(telefono) != 9:
        return "El teléfono debe tener exactamente 9 dígitos."

    if not telefono.startswith("9") and not telefono.startswith("01"):
        return "El teléfono debe iniciar con 9 si es celular o con 01 si es fijo."

    return ""


def tipo_producto_valido(tipo):
    return tipo.strip().lower() in ("perecible", "abarrote")


def id_producto_valido(id_producto, tipo):
    id_producto = id_producto.strip().upper()
    tipo = tipo.strip().lower()

    if tipo == "perecible":
        return id_producto.startswith("PER-")

    if tipo == "abarrote":
        return id_producto.startswith("ABA-")

    return False


def stock_valido(stock, tipo):
    stock = stock.strip()
    tipo = tipo.strip().lower()

    try:
        cantidad = float(stock)
    except ValueError:
        return False

    if cantidad < 0:
        return False

    if tipo == "abarrote" and not cantidad.is_integer():
        return False

    return True


def precio_unitario_valido(precio_unitario):
    precio_unitario = precio_unitario.strip()

    try:
        precio = float(precio_unitario)
    except ValueError:
        return False

    return precio > 0


def mensaje_error_tipo_producto(tipo):
    if tipo.strip() == "":
        return "El tipo de producto no puede estar vacío."

    return "El tipo de producto debe ser perecible o abarrote."


def mensaje_error_id_producto(id_producto, tipo):
    if id_producto.strip() == "":
        return "El ID del producto no puede estar vacío."

    if tipo.strip().lower() == "perecible":
        return "El ID de un producto perecible debe iniciar con PER-."

    if tipo.strip().lower() == "abarrote":
        return "El ID de un producto abarrote debe iniciar con ABA-."

    return "Primero debe ingresar un tipo de producto válido."


def mensaje_error_stock(stock, tipo):
    stock = stock.strip()

    if stock == "":
        return "El stock no puede estar vacío."

    try:
        cantidad = float(stock)
    except ValueError:
        return "El stock debe ser un número."

    if cantidad < 0:
        return "El stock no puede ser negativo."

    if tipo.strip().lower() == "abarrote" and not cantidad.is_integer():
        return "El stock de un producto abarrote debe ser una cantidad entera."

    return ""


def mensaje_error_precio_unitario(precio_unitario):
    precio_unitario = precio_unitario.strip()

    if precio_unitario == "":
        return "El precio unitario no puede estar vacío."

    try:
        precio = float(precio_unitario)
    except ValueError:
        return "El precio unitario debe ser un número."

    if precio <= 0:
        return "El precio unitario debe ser mayor que cero."

    return ""
