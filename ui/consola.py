from services.cliente_service import (
    consultar_cliente,
    eliminar_cliente,
    registrar_cliente,
)
from utils.validaciones import (
    mensaje_error_ruc,
    mensaje_error_telefono,
    ruc_valido,
    telefono_solo_numeros,
)


def mostrar_bienvenida():
    print("Bienvenido al Sistema Distribuidora Andina")


def mostrar_menu_principal():
    print("\nMenú principal")
    print("1. Manejar pedidos")
    print("2. Manejar stock")
    print("3. Manejar clientes")
    print("4. Reportes")
    print("5. Salir")


def mostrar_menu_pedidos():
    print("\nManejar pedidos")
    print("1. Registrar nuevo pedido")
    print("2. Cancelar un pedido")
    print("3. Manejar estado de los pedidos")
    print("4. Volver al menú principal")


def mostrar_menu_stock():
    print("\nManejar stock")
    print("1. Registrar productos en stock")
    print("2. Eliminar productos del stock")
    print("3. Actualizar cantidad de producto en stock")
    print("4. Consultar producto")
    print("5. Volver al menú principal")


def mostrar_menu_clientes():
    print("\nManejar clientes")
    print("1. Consultar clientes")
    print("2. Registrar clientes")
    print("3. Eliminar clientes")
    print("4. Volver al menú principal")


def mostrar_menu_reportes():
    print("\nReportes")
    print("1. Reporte general de pedidos")
    print("2. Reporte de pedidos por estado")
    print("3. Reporte de productos con bajo stock")
    print("4. Reporte de productos más solicitados")
    print("5. Reporte de clientes con pedidos en curso")
    print("6. Volver al menú principal")


def mostrar_funcionalidad_pendiente():
    print("\nFuncionalidad pendiente de implementación.")


def mostrar_operacion_cancelada():
    print("Operación cancelada.")


def entrada_cancelada(valor):
    return valor.strip().lower() == "cancelar"


def pedir_dato_cliente(mensaje):
    valor = input(mensaje)

    if entrada_cancelada(valor):
        return None

    return valor.strip()


def pedir_ruc_cliente(mensaje):
    while True:
        ruc = pedir_dato_cliente(mensaje)

        if ruc is None:
            return None

        if ruc_valido(ruc):
            return ruc

        print(mensaje_error_ruc(ruc))


def mostrar_cliente(cliente):
    print(f"RUC: {cliente.ruc}")
    print(f"Razón social: {cliente.razon_social}")
    print(f"Teléfono: {cliente.telefono}")
    print(f"Dirección: {cliente.direccion}")


def interfaz_consultar_cliente():
    print("\nConsultar cliente")
    print('Escriba "cancelar" para volver al menú de clientes.')

    ruc = pedir_ruc_cliente("Ingrese el RUC del cliente: ")

    if ruc is None:
        return

    fue_encontrado, cliente, mensaje = consultar_cliente(ruc)
    print(mensaje)

    if fue_encontrado:
        mostrar_cliente(cliente)


def interfaz_registrar_cliente():
    print("\nRegistrar cliente")
    print('Escriba "cancelar" para volver al menú de clientes.')

    ruc = pedir_ruc_cliente("Ingrese el RUC: ")
    if ruc is None:
        mostrar_operacion_cancelada()
        return

    razon_social = pedir_dato_cliente("Ingrese la razón social: ")
    if razon_social is None:
        mostrar_operacion_cancelada()
        return

    while True:
        telefono = pedir_dato_cliente("Ingrese el teléfono: ")

        if telefono is None:
            mostrar_operacion_cancelada()
            return

        if telefono_solo_numeros(telefono):
            break

        print(mensaje_error_telefono(telefono))

    direccion = pedir_dato_cliente("Ingrese la dirección: ")
    if direccion is None:
        mostrar_operacion_cancelada()
        return

    fue_registrado, cliente, mensaje = registrar_cliente(
        ruc,
        razon_social,
        telefono,
        direccion,
    )
    print(mensaje)

    if fue_registrado:
        mostrar_cliente(cliente)


def interfaz_eliminar_cliente():
    print("\nEliminar cliente")
    print('Escriba "cancelar" para volver al menú de clientes.')

    ruc = pedir_ruc_cliente("Ingrese el RUC del cliente a eliminar: ")

    if ruc is None:
        return

    fue_encontrado, cliente, mensaje = consultar_cliente(ruc)

    if not fue_encontrado:
        print(mensaje)
        return

    mostrar_cliente(cliente)
    confirmacion = input("¿Confirma la eliminación? (s/n): ").strip().lower()

    if entrada_cancelada(confirmacion) or confirmacion != "s":
        print("Eliminación cancelada.")
        return

    fue_eliminado, cliente_eliminado, mensaje = eliminar_cliente(ruc)
    print(mensaje)

    if fue_eliminado:
        mostrar_cliente(cliente_eliminado)


def manejar_pedidos():
    while True:
        mostrar_menu_pedidos()
        opcion = input("Seleccione una opción: ")

        if opcion in ("1", "2", "3"):
            mostrar_funcionalidad_pendiente()
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def manejar_stock():
    while True:
        mostrar_menu_stock()
        opcion = input("Seleccione una opción: ")

        if opcion in ("1", "2", "3", "4"):
            mostrar_funcionalidad_pendiente()
        elif opcion == "5":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def manejar_clientes():
    while True:
        mostrar_menu_clientes()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_consultar_cliente()
        elif opcion == "2":
            interfaz_registrar_cliente()
        elif opcion == "3":
            interfaz_eliminar_cliente()
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def manejar_reportes():
    while True:
        mostrar_menu_reportes()
        opcion = input("Seleccione una opción: ")

        if opcion in ("1", "2", "3", "4", "5"):
            mostrar_funcionalidad_pendiente()
        elif opcion == "6":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def iniciar_consola():
    mostrar_bienvenida()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            manejar_pedidos()
        elif opcion == "2":
            manejar_stock()
        elif opcion == "3":
            manejar_clientes()
        elif opcion == "4":
            manejar_reportes()
        elif opcion == "5":
            print("\nSaliendo del sistema.")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
