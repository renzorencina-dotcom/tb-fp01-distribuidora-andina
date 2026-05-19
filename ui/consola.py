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

        if opcion in ("1", "2", "3"):
            mostrar_funcionalidad_pendiente()
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
