from models.pedido import Pedido
from models.producto import Producto
from services.cliente_service import (
    borrar_cliente,
    buscar_cliente_por_ruc,
    listar_clientes,
    registrar_cliente,
)


def pedir_ruc():
    # Toda lectura desde teclado pertenece a la capa de interfaz.
    return input("Ingrese el RUC del cliente: ")


def pedir_razon_social():
    return input("Ingrese el nombre o razón social del cliente: ")


def mostrar_clientes(clientes):
    # Presenta los clientes que services devuelve como datos.
    print("\nClientes registrados:")
    for cliente in clientes:
        print(f"{cliente.id_cliente}. {cliente.nombre}")


def realizar_pedido(cliente):
    # Si no hay cliente seleccionado o registrado, no se puede generar el pedido.
    if cliente is None:
        return

    # Producto temporal para mantener el flujo de pedido funcionando en consola.
    producto = Producto(1, "Manzana", 100, 2.5)
    pedido = Pedido(1, cliente, producto, 20)

    print("\nResumen del pedido:")
    print(pedido)
    print(producto)


def registrar_cliente_desde_consola():
    # Pide datos al usuario y llama al servicio para validar y guardar.
    while True:
        ruc = pedir_ruc()
        razon_social = pedir_razon_social()
        fue_registrado, cliente, mensaje = registrar_cliente(ruc, razon_social)

        if fue_registrado:
            print("Cliente registrado correctamente.")
            return cliente

        # El mensaje viene desde la validacion, pero se muestra solo en la interfaz.
        print(mensaje)


def seleccionar_cliente_desde_consola():
    # Obtiene los clientes desde services y maneja la seleccion por consola.
    clientes = listar_clientes()

    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return None

    mostrar_clientes(clientes)
    ruc = pedir_ruc()
    cliente = buscar_cliente_por_ruc(ruc)

    if cliente is None:
        print("Cliente no encontrado.")
        return None

    return cliente


def eliminar_cliente_desde_consola():
    # Pide el RUC y deja que services determine si se pudo eliminar.
    ruc = pedir_ruc()
    fue_eliminado, cliente = borrar_cliente(ruc)

    if not fue_eliminado:
        print("Cliente no encontrado.")
        return None

    print("Cliente eliminado correctamente.")
    return cliente


def ejecutar_consola():
    # Menu principal de la aplicacion en modo consola.
    print("Sistema Distribuidora Andina")

    print("\nSeleccione una opción:")
    print("1. Registrar cliente nuevo")
    print("2. Seleccionar cliente existente")
    print("3. Borrar cliente")
    print("4. Salir")

    opcion = input("Opción: ")

    if opcion == "1":
        cliente = registrar_cliente_desde_consola()
        realizar_pedido(cliente)
    elif opcion == "2":
        cliente = seleccionar_cliente_desde_consola()
        realizar_pedido(cliente)
    elif opcion == "3":
        eliminar_cliente_desde_consola()
    elif opcion == "4":
        print("Saliendo del sistema.")
    else:
        print("Opción no válida.")
