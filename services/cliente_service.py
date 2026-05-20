from models.cliente import Cliente
from utils.csv_manager import (
    agregar_fila_csv,
    buscar_por_campo,
    eliminar_fila_csv,
)
from utils.validaciones import ruc_solo_numeros, telefono_solo_numeros, texto_no_vacio


RUTA_CLIENTES = "data/clientes.csv"
CAMPOS_CLIENTE = ["ruc", "razon_social", "telefono", "direccion"]


def convertir_fila_a_cliente(fila):
    return Cliente(
        fila["ruc"],
        fila["razon_social"],
        fila["telefono"],
        fila["direccion"],
    )


def validar_datos_cliente(ruc, razon_social, telefono, direccion):
    if not texto_no_vacio(ruc):
        return False, "El RUC no puede estar vacío."

    if not ruc_solo_numeros(ruc):
        return False, "El RUC debe contener solo números."

    if not texto_no_vacio(razon_social):
        return False, "La razón social no puede estar vacía."

    if not texto_no_vacio(telefono):
        return False, "El teléfono no puede estar vacío."

    if not telefono_solo_numeros(telefono):
        return False, "El teléfono debe contener solo números."

    if not texto_no_vacio(direccion):
        return False, "La dirección no puede estar vacía."

    return True, ""


def registrar_cliente(ruc, razon_social, telefono, direccion):
    es_valido, mensaje = validar_datos_cliente(ruc, razon_social, telefono, direccion)

    if not es_valido:
        return False, None, mensaje

    if buscar_por_campo(RUTA_CLIENTES, "ruc", ruc) is not None:
        return False, None, "Ya existe un cliente registrado con ese RUC."

    fila = {
        "ruc": ruc,
        "razon_social": razon_social,
        "telefono": telefono,
        "direccion": direccion,
    }
    agregar_fila_csv(RUTA_CLIENTES, fila, CAMPOS_CLIENTE)
    return True, convertir_fila_a_cliente(fila), "Cliente registrado correctamente."


def buscar_cliente_por_ruc(ruc):
    fila = buscar_por_campo(RUTA_CLIENTES, "ruc", ruc)

    if fila is None:
        return None

    return convertir_fila_a_cliente(fila)


def consultar_cliente(ruc):
    if not texto_no_vacio(ruc):
        return False, None, "El RUC no puede estar vacío."

    cliente = buscar_cliente_por_ruc(ruc)

    if cliente is None:
        return False, None, "Cliente no encontrado."

    return True, cliente, "Cliente encontrado."


def eliminar_cliente(ruc):
    if not texto_no_vacio(ruc):
        return False, None, "El RUC no puede estar vacío."

    fila_eliminada = eliminar_fila_csv(RUTA_CLIENTES, "ruc", ruc, CAMPOS_CLIENTE)

    if fila_eliminada is None:
        return False, None, "Cliente no encontrado."

    return True, convertir_fila_a_cliente(fila_eliminada), "Cliente eliminado correctamente."
