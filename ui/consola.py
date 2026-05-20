from services.cliente_service import (
    consultar_cliente,
    eliminar_cliente,
    registrar_cliente,
)
from services.producto_service import (
    agregar_stock,
    actualizar_stock,
    consultar_producto,
    eliminar_producto,
    registrar_producto,
    restar_stock,
)
from utils.validaciones import (
    id_producto_valido,
    mensaje_error_ruc,
    mensaje_error_id_producto,
    mensaje_error_precio_unitario,
    mensaje_error_stock,
    mensaje_error_telefono,
    mensaje_error_tipo_producto,
    precio_unitario_valido,
    ruc_valido,
    stock_valido,
    telefono_solo_numeros,
    tipo_producto_valido,
    texto_no_vacio,
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


def mostrar_menu_actualizar_stock():
    print("\nActualizar cantidad de producto en stock")
    print("1. Añadir stock a un producto")
    print("2. Restar stock a un producto")
    print("3. Actualizar stock completo")
    print("4. Volver al menú de stock")


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


def pedir_dato_stock(mensaje):
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


def pedir_tipo_producto():
    while True:
        tipo = pedir_dato_stock("Ingrese el tipo de producto (perecible/abarrote): ")

        if tipo is None:
            return None

        if tipo_producto_valido(tipo):
            return tipo.strip().lower()

        print(mensaje_error_tipo_producto(tipo))


def pedir_id_producto_registro(tipo):
    while True:
        id_producto = pedir_dato_stock("Ingrese el ID del producto: ")

        if id_producto is None:
            return None

        if id_producto_valido(id_producto, tipo):
            return id_producto.strip().upper()

        print(mensaje_error_id_producto(id_producto, tipo))


def pedir_id_producto_busqueda(mensaje):
    while True:
        id_producto = pedir_dato_stock(mensaje)

        if id_producto is None:
            return None

        id_producto = id_producto.strip().upper()

        if id_producto.startswith("PER-") or id_producto.startswith("ABA-"):
            return id_producto

        print("El ID del producto debe iniciar con PER- o ABA-.")


def pedir_producto_existente(mensaje):
    while True:
        id_producto = pedir_id_producto_busqueda(mensaje)

        if id_producto is None:
            return None, None

        fue_encontrado, producto, mensaje_busqueda = consultar_producto(id_producto)

        if fue_encontrado:
            return id_producto, producto

        print(mensaje_busqueda)


def pedir_texto_obligatorio(mensaje, nombre_campo):
    while True:
        valor = pedir_dato_stock(mensaje)

        if valor is None:
            return None

        if texto_no_vacio(valor):
            return valor

        print(f"{nombre_campo} no puede estar vacía.")


def pedir_stock_producto(tipo, mensaje):
    while True:
        stock = pedir_dato_stock(mensaje)

        if stock is None:
            return None

        if stock_valido(stock, tipo):
            return stock

        print(mensaje_error_stock(stock, tipo))


def pedir_cantidad_stock(tipo, mensaje, stock_disponible=None):
    while True:
        cantidad = pedir_stock_producto(tipo, mensaje)

        if cantidad is None:
            return None

        if stock_disponible is None or float(cantidad) <= stock_disponible:
            return cantidad

        print("La cantidad a restar no puede ser mayor que el stock actual.")


def pedir_precio_unitario():
    while True:
        precio_unitario = pedir_dato_stock("Ingrese el precio unitario: ")

        if precio_unitario is None:
            return None

        if precio_unitario_valido(precio_unitario):
            return precio_unitario

        print(mensaje_error_precio_unitario(precio_unitario))


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


def mostrar_producto(producto):
    print(f"ID: {producto.id_producto}")
    print(f"Descripción: {producto.descripcion}")
    print(f"Tipo: {producto.tipo}")
    print(f"Stock: {producto.stock}")
    print(f"Precio unitario: S/ {producto.precio_unitario:.2f}")


def interfaz_registrar_producto():
    print("\nRegistrar productos en stock")
    print('Escriba "cancelar" para volver al menú de stock.')

    tipo = pedir_tipo_producto()
    if tipo is None:
        mostrar_operacion_cancelada()
        return

    id_producto = pedir_id_producto_registro(tipo)
    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    descripcion = pedir_texto_obligatorio("Ingrese la descripción: ", "La descripción")
    if descripcion is None:
        mostrar_operacion_cancelada()
        return

    stock = pedir_stock_producto(tipo, "Ingrese el stock: ")
    if stock is None:
        mostrar_operacion_cancelada()
        return

    precio_unitario = pedir_precio_unitario()
    if precio_unitario is None:
        mostrar_operacion_cancelada()
        return

    fue_registrado, producto, mensaje = registrar_producto(
        id_producto,
        descripcion,
        tipo,
        stock,
        precio_unitario,
    )
    print(mensaje)

    if fue_registrado:
        mostrar_producto(producto)


def interfaz_eliminar_producto():
    print("\nEliminar productos del stock")
    print('Escriba "cancelar" para volver al menú de stock.')

    id_producto, producto = pedir_producto_existente("Ingrese el ID del producto a eliminar: ")

    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    mostrar_producto(producto)
    confirmacion = input("¿Confirma la eliminación? (s/n): ").strip().lower()

    if entrada_cancelada(confirmacion) or confirmacion != "s":
        print("Eliminación cancelada.")
        return

    fue_eliminado, producto_eliminado, mensaje = eliminar_producto(id_producto)
    print(mensaje)

    if fue_eliminado:
        mostrar_producto(producto_eliminado)


def interfaz_agregar_stock():
    print("\nAñadir stock a un producto")
    print('Escriba "cancelar" para volver al menú de stock.')

    id_producto, producto = pedir_producto_existente("Ingrese el ID del producto: ")

    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    mostrar_producto(producto)
    cantidad = pedir_cantidad_stock(producto.tipo, "Ingrese la cantidad a añadir: ")

    if cantidad is None:
        mostrar_operacion_cancelada()
        return

    fue_actualizado, producto_actualizado, mensaje = agregar_stock(id_producto, cantidad)
    print(mensaje)

    if fue_actualizado:
        mostrar_producto(producto_actualizado)


def interfaz_restar_stock():
    print("\nRestar stock a un producto")
    print('Escriba "cancelar" para volver al menú de stock.')

    id_producto, producto = pedir_producto_existente("Ingrese el ID del producto: ")

    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    mostrar_producto(producto)
    cantidad = pedir_cantidad_stock(
        producto.tipo,
        "Ingrese la cantidad a restar: ",
        producto.stock,
    )

    if cantidad is None:
        mostrar_operacion_cancelada()
        return

    fue_actualizado, producto_actualizado, mensaje = restar_stock(id_producto, cantidad)
    print(mensaje)

    if fue_actualizado:
        mostrar_producto(producto_actualizado)


def interfaz_actualizar_stock_completo():
    print("\nActualizar stock completo")
    print('Escriba "cancelar" para volver al menú de stock.')

    id_producto, producto = pedir_producto_existente("Ingrese el ID del producto: ")

    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    mostrar_producto(producto)
    nuevo_stock = pedir_stock_producto(producto.tipo, "Ingrese el nuevo stock: ")

    if nuevo_stock is None:
        mostrar_operacion_cancelada()
        return

    fue_actualizado, producto_actualizado, mensaje = actualizar_stock(
        id_producto,
        nuevo_stock,
    )
    print(mensaje)

    if fue_actualizado:
        mostrar_producto(producto_actualizado)


def interfaz_actualizar_stock():
    while True:
        mostrar_menu_actualizar_stock()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_agregar_stock()
        elif opcion == "2":
            interfaz_restar_stock()
        elif opcion == "3":
            interfaz_actualizar_stock_completo()
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def interfaz_consultar_producto():
    print("\nConsultar producto")
    print('Escriba "cancelar" para volver al menú de stock.')

    id_producto, producto = pedir_producto_existente("Ingrese el ID del producto: ")

    if id_producto is None:
        mostrar_operacion_cancelada()
        return

    print("Producto encontrado.")
    mostrar_producto(producto)


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

        if opcion == "1":
            interfaz_registrar_producto()
        elif opcion == "2":
            interfaz_eliminar_producto()
        elif opcion == "3":
            interfaz_actualizar_stock()
        elif opcion == "4":
            interfaz_consultar_producto()
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
