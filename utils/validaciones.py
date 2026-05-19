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
