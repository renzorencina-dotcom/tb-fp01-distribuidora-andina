def validar_ruc(ruc):
    if not ruc.isdigit():
        return False, "El RUC debe contener solo números."

    if len(ruc) != 11:
        return False, "El RUC debe tener exactamente 11 dígitos."

    return True, ""


def validar_ruc_cliente(ruc, clientes):
    es_valido, mensaje = validar_ruc(ruc)

    if not es_valido:
        return False, mensaje

    for cliente in clientes:
        if str(cliente.id_cliente) == ruc:
            return False, "Ya existe un cliente registrado con ese RUC."

    return True, ""
