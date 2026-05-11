from models.cliente import Cliente
from utils.csv_manager import cargar_clientes, guardar_cliente, guardar_clientes
from utils.validaciones import validar_ruc_cliente


def listar_clientes():
    # Devuelve todos los clientes registrados sin mostrarlos en pantalla.
    return cargar_clientes()


def existe_ruc(ruc, clientes=None):
    # Permite validar si un RUC ya esta registrado; se puede reutilizar una lista ya cargada.
    if clientes is None:
        clientes = cargar_clientes()

    for cliente in clientes:
        if str(cliente.id_cliente) == str(ruc):
            return True

    return False


def registrar_cliente(ruc, razon_social):
    # Valida el RUC antes de crear y guardar el cliente.
    clientes = cargar_clientes()
    es_valido, mensaje = validar_ruc_cliente(ruc, clientes)

    if not es_valido:
        # Devuelve el error para que la interfaz decida como mostrarlo.
        return False, None, mensaje

    cliente = Cliente(ruc, razon_social)
    guardar_cliente(cliente)
    # Devuelve exito y el cliente creado, sin imprimir mensajes desde services.
    return True, cliente, ""


def buscar_cliente_por_ruc(ruc):
    # Busca un cliente especifico por RUC y devuelve None si no existe.
    clientes = cargar_clientes()

    for cliente in clientes:
        if str(cliente.id_cliente) == str(ruc):
            return cliente

    return None


def borrar_cliente(ruc):
    # Para borrar, se reconstruye la lista excluyendo al cliente con el RUC indicado.
    clientes = cargar_clientes()
    clientes_actualizados = []
    cliente_eliminado = None

    for cliente in clientes:
        if str(cliente.id_cliente) == str(ruc):
            cliente_eliminado = cliente
        else:
            clientes_actualizados.append(cliente)

    if cliente_eliminado is None:
        # La interfaz usara este resultado para mostrar "Cliente no encontrado".
        return False, None

    # Guarda la lista actualizada para reemplazar el contenido anterior del CSV.
    guardar_clientes(clientes_actualizados)
    return True, cliente_eliminado
