from services.cliente_service import (
    consultar_cliente,
    eliminar_cliente,
    registrar_cliente,
)
from services.pedido_service import (
    actualizar_estado_pedido,
    atender_pedido,
    buscar_pedido_por_codigo,
    codigo_pedido_existe,
    registrar_cabecera_pedido,
    registrar_detalle_pedido,
)
from services.producto_service import (
    agregar_stock,
    actualizar_stock,
    consultar_producto,
    eliminar_producto,
    registrar_producto,
    restar_stock,
)
from services.reporte_service import (
    obtener_clientes_con_pedidos_en_curso,
    obtener_pedidos_por_estado,
    obtener_producto_mas_solicitado,
    obtener_productos_bajo_stock,
    obtener_reporte_general_pedidos,
)
from models.cliente import Cliente
from models.pedido import DetallePedido
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


def mostrar_menu_registrar_pedido():
    print("\nRegistrar nuevo pedido")
    print("1. Pedido para cliente existente")
    print("2. Pedido para cliente nuevo")
    print("3. Volver al menú anterior")


def mostrar_menu_estado_pedidos():
    print("\nManejar estado de los pedidos")
    print("1. Actualizar estado de un pedido")
    print("2. Consultar estado de un pedido")
    print("3. Volver al menú anterior")


def mostrar_menu_actualizar_estado_pedido():
    print("\nSeleccione el nuevo estado del pedido")
    print("1. Pedido recibido")
    print("2. Pedido pendiente")
    print("3. Pedido atendido parcialmente")
    print("4. Pedido atendido")
    print("5. Volver")


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


def mostrar_menu_estados_reporte():
    print("\nReporte de pedidos por estado")
    print("1. Pedido registrado")
    print("2. Pedido recibido")
    print("3. Pedido pendiente")
    print("4. Pedido atendido parcialmente")
    print("5. Pedido atendido")
    print("6. Pedido cancelado")
    print("7. Volver")


def mostrar_operacion_cancelada():
    print("Operación cancelada.")


def entrada_cancelada(valor):
    """Detecta el comando usado para cancelar operaciones de consola."""
    return valor.strip().lower() == "cancelar"


def pedir_dato_cliente(mensaje):
    """Pide un dato de cliente y permite cancelar escribiendo "cancelar"."""
    valor = input(mensaje)

    if entrada_cancelada(valor):
        return None

    return valor.strip()


def pedir_dato_stock(mensaje):
    """Pide un dato de stock y permite cancelar escribiendo "cancelar"."""
    valor = input(mensaje)

    if entrada_cancelada(valor):
        return None

    return valor.strip()


def pedir_ruc_cliente(mensaje):
    """Solicita un RUC válido hasta recibirlo o hasta que se cancele."""
    # Este ciclo evita cancelar la operación por errores de digitación; solo
    # termina cuando el RUC cumple la regla o el usuario escribe "cancelar".
    while True:
        ruc = pedir_dato_cliente(mensaje)

        if ruc is None:
            return None

        if ruc_valido(ruc):
            return ruc

        print(mensaje_error_ruc(ruc))


def pedir_tipo_producto():
    """Solicita el tipo de producto aceptando solo perecible o abarrote."""
    while True:
        tipo = pedir_dato_stock("Ingrese el tipo de producto (perecible/abarrote): ")

        if tipo is None:
            return None

        if tipo_producto_valido(tipo):
            return tipo.strip().lower()

        print(mensaje_error_tipo_producto(tipo))


def pedir_id_producto_registro(tipo):
    """Solicita un ID de producto compatible con el tipo seleccionado."""
    while True:
        id_producto = pedir_dato_stock("Ingrese el ID del producto: ")

        if id_producto is None:
            return None

        if id_producto_valido(id_producto, tipo):
            return id_producto.strip().upper()

        print(mensaje_error_id_producto(id_producto, tipo))


def pedir_id_producto_busqueda(mensaje):
    """Solicita un ID de producto con prefijo válido para operaciones de búsqueda."""
    while True:
        id_producto = pedir_dato_stock(mensaje)

        if id_producto is None:
            return None

        id_producto = id_producto.strip().upper()

        if id_producto.startswith("PER-") or id_producto.startswith("ABA-"):
            return id_producto

        print("El ID del producto debe iniciar con PER- o ABA-.")


def pedir_producto_existente(mensaje):
    """Pide un ID y repite la solicitud hasta encontrar el producto o cancelar."""
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


def pedir_confirmacion(mensaje):
    respuesta = input(mensaje).strip().lower()
    return respuesta in ("s", "si", "sí")


def pedir_codigo_pedido():
    """Solicita un código nuevo de pedido de 4 dígitos y no repetido."""
    while True:
        codigo_pedido = pedir_dato_stock("Ingrese el código de pedido (4 dígitos): ")

        if codigo_pedido is None:
            return None

        if not codigo_pedido.isdigit():
            print("El código de pedido debe contener solo números.")
            continue

        if len(codigo_pedido) != 4:
            print("El código de pedido debe tener exactamente 4 dígitos.")
            continue

        if codigo_pedido_existe(codigo_pedido):
            print("Ya existe un pedido registrado con ese código.")
            continue

        return codigo_pedido


def pedir_codigo_pedido_existente():
    """Solicita un código de pedido existente o permite cancelar la operación."""
    # Los errores de formato o búsqueda no cancelan el flujo; el usuario puede
    # seguir intentando hasta escribir "cancelar".
    while True:
        codigo_pedido = pedir_dato_stock("\nIngrese el código del pedido: ")

        if codigo_pedido is None:
            return None, None

        if not codigo_pedido.isdigit():
            print("El código de pedido debe contener solo números.")
            continue

        if len(codigo_pedido) != 4:
            print("El código de pedido debe tener exactamente 4 dígitos.")
            continue

        pedido = buscar_pedido_por_codigo(codigo_pedido)

        if pedido is None:
            print("Pedido no encontrado")
            continue

        return codigo_pedido, pedido


def pedir_cliente_existente_para_pedido() -> Cliente | None:
    """Busca un cliente registrado por RUC para iniciar un pedido."""
    while True:
        ruc = pedir_ruc_cliente("Ingrese el RUC del cliente: ")

        if ruc is None:
            return None

        fue_encontrado, cliente, _ = consultar_cliente(ruc)

        if fue_encontrado and cliente is not None:
            return cliente

        print("Cliente no registrado o no encontrado.")


def registrar_cliente_desde_pedido() -> Cliente | None:
    """Registra un cliente durante el flujo de creación de pedido."""
    print("\nRegistro de cliente para pedido")
    print('Escriba "cancelar" para volver al menú Registrar nuevo pedido.')

    while True:
        ruc = pedir_ruc_cliente("Ingrese el RUC: ")

        if ruc is None:
            mostrar_operacion_cancelada()
            return None

        fue_encontrado, _, _ = consultar_cliente(ruc)

        if not fue_encontrado:
            break

        print("Ya existe un cliente registrado con ese RUC.")

    razon_social = pedir_dato_cliente("Ingrese la razón social: ")
    if razon_social is None:
        mostrar_operacion_cancelada()
        return None

    while True:
        telefono = pedir_dato_cliente("Ingrese el teléfono: ")

        if telefono is None:
            mostrar_operacion_cancelada()
            return None

        if telefono_solo_numeros(telefono):
            break

        print(mensaje_error_telefono(telefono))

    direccion = pedir_dato_cliente("Ingrese la dirección: ")
    if direccion is None:
        mostrar_operacion_cancelada()
        return None

    fue_registrado, cliente, mensaje = registrar_cliente(
        ruc,
        razon_social,
        telefono,
        direccion,
    )
    print(mensaje)

    if fue_registrado and cliente is not None:
        mostrar_cliente(cliente)
        return cliente

    return None


def guardar_pedido(cliente: Cliente, detalle_pedido):
    """Guarda cabecera y detalle del pedido después de la confirmación."""
    codigo_pedido = pedir_codigo_pedido()

    if codigo_pedido is None:
        mostrar_operacion_cancelada()
        return

    fue_registrada_cabecera, _, mensaje_cabecera = registrar_cabecera_pedido(
        codigo_pedido,
        cliente.ruc,
        cliente.razon_social,
    )

    if not fue_registrada_cabecera:
        print(mensaje_cabecera)
        return

    fue_registrado_detalle, _, mensaje_detalle = registrar_detalle_pedido(
        codigo_pedido,
        detalle_pedido,
    )

    if not fue_registrado_detalle:
        print(mensaje_detalle)
        return

    print("Pedido registrado correctamente.")


def pedir_producto_para_pedido():
    """Solicita productos para el pedido validando existencia y disponibilidad."""
    while True:
        id_producto = input("Ingrese el ID del producto: ").strip()

        if entrada_cancelada(id_producto):
            return "cancelar", None

        if id_producto.lower() == "pedido terminado":
            return "pedido terminado", None

        id_producto = id_producto.upper()

        if not id_producto.startswith("PER-") and not id_producto.startswith("ABA-"):
            print("El ID del producto debe iniciar con PER- o ABA-.")
            continue

        fue_encontrado, producto, _ = consultar_producto(id_producto)

        if not fue_encontrado:
            print("Producto no registrado.")
            continue

        if producto.stock <= 0:
            print("Producto agotado o no disponible.")
            continue

        return "producto", producto


def pedir_cantidad_producto_pedido(producto):
    """Solicita una cantidad compatible con el producto y su stock disponible."""
    while True:
        cantidad = pedir_dato_stock("Ingrese la cantidad solicitada: ")

        if cantidad is None:
            return None

        if not stock_valido(cantidad, producto.tipo):
            print(mensaje_error_stock(cantidad, producto.tipo))
            continue

        cantidad = float(cantidad)

        if cantidad <= 0:
            print("La cantidad solicitada debe ser mayor que cero.")
            continue

        if cantidad > producto.stock:
            print("Stock insuficiente para atender la cantidad solicitada.")
            continue

        return cantidad


def registrar_productos_del_pedido():
    """Construye la lista temporal de productos que formarán parte del pedido."""
    # detalle_pedido existe solo durante el registro; recién se guarda en CSV
    # cuando el usuario confirma la orden completa.
    detalle_pedido = []
    print('\nIngrese productos del pedido. Escriba "Pedido terminado" para finalizar.')
    print('Escriba "cancelar" para cancelar todo el registro del pedido.')

    # El ciclo permite agregar varios productos al mismo pedido sin regresar al
    # menú entre cada línea de detalle.
    while True:
        accion, producto = pedir_producto_para_pedido()

        if accion == "cancelar":
            mostrar_operacion_cancelada()
            return None

        if accion == "pedido terminado":
            if len(detalle_pedido) == 0:
                print("No se registraron productos en el pedido.")
                return []

            return detalle_pedido

        cantidad = pedir_cantidad_producto_pedido(producto)

        if cantidad is None:
            mostrar_operacion_cancelada()
            return None

        # Cada producto solicitado se modela como DetallePedido para calcular
        # subtotal y luego persistirlo en detalle_pedidos.csv.
        detalle = DetallePedido(
            "",
            producto.id_producto,
            producto.descripcion,
            cantidad,
            producto.precio_unitario,
        )
        detalle_pedido.append(detalle)
        print("Producto agregado al pedido.")


def mostrar_resumen_pedido(detalle_pedido):
    """Muestra los productos seleccionados y el total antes de confirmar."""
    total_general = 0

    print("\nResumen del pedido")
    for detalle in detalle_pedido:
        print(
            f"{detalle.descripcion} | "
            f"Cantidad: {detalle.cantidad} | "
            f"Precio unitario: S/ {detalle.precio_unitario:.2f} | "
            f"Subtotal: S/ {detalle.subtotal:.2f}"
        )
        total_general += detalle.subtotal

    print(f"Total general: S/ {total_general:.2f}")


def mostrar_pedido(pedido):
    print(f"\nCódigo del pedido: {pedido.codigo_pedido}")
    print(f"RUC del cliente: {pedido.ruc_cliente}")
    print(f"Razón social: {pedido.razon_social}")
    print(f"Estado actual: {pedido.estado}")


def registrar_pedido_para_cliente(cliente: Cliente):
    """Completa el registro de productos para un cliente ya definido."""
    detalle_pedido = registrar_productos_del_pedido()

    if detalle_pedido is None:
        return

    if len(detalle_pedido) == 0:
        return

    mostrar_resumen_pedido(detalle_pedido)

    if not pedir_confirmacion("¿Desea confirmar el pedido? (s/n): "):
        print("Registro de pedido cancelado.")
        return

    guardar_pedido(cliente, detalle_pedido)


def interfaz_pedido_cliente_existente():
    print("\nPedido para cliente existente")
    print('Escriba "cancelar" para volver al menú Registrar nuevo pedido.')

    cliente = pedir_cliente_existente_para_pedido()

    if cliente is None:
        mostrar_operacion_cancelada()
        return

    mostrar_cliente(cliente)
    registrar_pedido_para_cliente(cliente)


def interfaz_pedido_cliente_nuevo():
    cliente = registrar_cliente_desde_pedido()

    if cliente is None:
        return

    registrar_pedido_para_cliente(cliente)


def interfaz_registrar_nuevo_pedido():
    """Muestra el submenú para registrar pedidos de clientes nuevos o existentes."""
    # El submenú permanece activo hasta que el usuario elige volver al menú de
    # pedidos.
    while True:
        mostrar_menu_registrar_pedido()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_pedido_cliente_existente()
        elif opcion == "2":
            interfaz_pedido_cliente_nuevo()
        elif opcion == "3":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def interfaz_cancelar_pedido():
    """Permite marcar un pedido existente como cancelado."""
    print("\nCancelar un pedido")
    print('Escriba "cancelar" para volver al menú Manejar pedidos.')

    while True:
        codigo_pedido, pedido = pedir_codigo_pedido_existente()

        if codigo_pedido is None:
            mostrar_operacion_cancelada()
            return

        mostrar_pedido(pedido)

        while True:
            respuesta = input("¿Desea cancelar el pedido? (s/n): ").strip().lower()

            if entrada_cancelada(respuesta):
                mostrar_operacion_cancelada()
                return

            if respuesta == "s":
                fue_actualizado, pedido_actualizado, mensaje = actualizar_estado_pedido(
                    codigo_pedido,
                    "Pedido cancelado",
                )
                print(mensaje)

                if fue_actualizado:
                    mostrar_pedido(pedido_actualizado)

                return

            if respuesta == "n":
                print("Cancelación anulada")
                break

            print("Respuesta no válida. Ingrese s, n o cancelar.")


def interfaz_consultar_estado_pedido():
    print("\nConsultar estado de un pedido")
    print('Escriba "cancelar" para volver al menú Manejar estado de los pedidos.')

    while True:
        _, pedido = pedir_codigo_pedido_existente()

        if pedido is None:
            return

        mostrar_pedido(pedido)


def pedir_nuevo_estado_pedido():
    estados_por_opcion = {
        "1": "Pedido recibido",
        "2": "Pedido pendiente",
        "3": "Pedido atendido parcialmente",
        "4": "Pedido atendido",
    }

    while True:
        mostrar_menu_actualizar_estado_pedido()
        opcion = input("Seleccione una opción: ").strip()

        if entrada_cancelada(opcion) or opcion == "5":
            return None

        if opcion in estados_por_opcion:
            return estados_por_opcion[opcion]

        print("\nOpción no válida. Intente nuevamente.")


def interfaz_actualizar_estado_pedido():
    print("\nActualizar estado de un pedido")
    print('Escriba "cancelar" para volver al menú Manejar estado de los pedidos.')

    while True:
        codigo_pedido, pedido = pedir_codigo_pedido_existente()

        if codigo_pedido is None:
            return

        mostrar_pedido(pedido)

        if pedido.estado == "Pedido cancelado":
            print(
                "No se puede actualizar el estado de este pedido porque ha sido "
                "cancelado."
            )
            return

        if pedido.estado == "Pedido atendido":
            print("Este pedido ya fue atendido y no puede cambiar de estado.")
            return

        nuevo_estado = pedir_nuevo_estado_pedido()

        if nuevo_estado is None:
            return

        if nuevo_estado == "Pedido atendido":
            fue_actualizado, pedido_actualizado, mensaje = atender_pedido(
                codigo_pedido
            )
        else:
            fue_actualizado, pedido_actualizado, mensaje = actualizar_estado_pedido(
                codigo_pedido,
                nuevo_estado,
            )
        print(mensaje)

        if fue_actualizado:
            mostrar_pedido(pedido_actualizado)

        return


def manejar_estado_pedidos():
    """Gestiona el submenú de consulta y actualización de estados de pedidos."""
    while True:
        mostrar_menu_estado_pedidos()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_actualizar_estado_pedido()
        elif opcion == "2":
            interfaz_consultar_estado_pedido()
        elif opcion == "3":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def mostrar_cliente(cliente: Cliente):
    """Muestra los datos principales de un cliente en consola."""
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

    if fue_encontrado and cliente is not None:
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

    if fue_registrado and cliente is not None:
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

    if cliente is None:
        print("Cliente no encontrado.")
        return

    mostrar_cliente(cliente)
    confirmacion = input("¿Confirma la eliminación? (s/n): ").strip().lower()

    if entrada_cancelada(confirmacion) or confirmacion != "s":
        print("Eliminación cancelada.")
        return

    fue_eliminado, cliente_eliminado, mensaje = eliminar_cliente(ruc)
    print(mensaje)

    if fue_eliminado and cliente_eliminado is not None:
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

    descripcion = pedir_texto_obligatorio(
        "Ingrese la descripción: ",
        "La descripción",
    )
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

    id_producto, producto = pedir_producto_existente(
        "Ingrese el ID del producto a eliminar: "
    )

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

    fue_actualizado, producto_actualizado, mensaje = agregar_stock(
        id_producto,
        cantidad,
    )
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
    """Mantiene activo el módulo de pedidos y deriva a sus submenús."""
    # El while conserva el módulo abierto hasta que el usuario elige volver al
    # menú principal.
    while True:
        mostrar_menu_pedidos()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_registrar_nuevo_pedido()
        elif opcion == "2":
            interfaz_cancelar_pedido()
        elif opcion == "3":
            manejar_estado_pedidos()
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def manejar_stock():
    """Mantiene activo el módulo de stock y ejecuta sus operaciones."""
    # El menú se repite para permitir varias operaciones de inventario en una
    # misma sesión.
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
    """Mantiene activo el módulo de clientes y ejecuta sus operaciones."""
    # Este ciclo permite consultar, registrar o eliminar clientes hasta volver
    # al menú principal.
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


def interfaz_reporte_general_pedidos():
    """Muestra el total de pedidos y el conteo por estado."""
    reporte = obtener_reporte_general_pedidos()

    if reporte["total_pedidos"] == 0:
        print("\nNo hay pedidos registrados.")
        return

    print("\nReporte general de pedidos")
    print(f"Total de pedidos: {reporte['total_pedidos']}")
    print(f"Pedido registrado: {reporte['Pedido registrado']}")
    print(f"Pedido recibido: {reporte['Pedido recibido']}")
    print(f"Pedido pendiente: {reporte['Pedido pendiente']}")
    print(
        "Pedido atendido parcialmente: "
        f"{reporte['Pedido atendido parcialmente']}"
    )
    print(f"Pedido atendido: {reporte['Pedido atendido']}")
    print(f"Pedido cancelado: {reporte['Pedido cancelado']}")


def mostrar_pedidos_reporte(pedidos):
    """Muestra una lista de pedidos preparada por el servicio de reportes."""
    for pedido in pedidos:
        print(f"\nCódigo de pedido: {pedido['codigo_pedido']}")
        print(f"RUC: {pedido['ruc_cliente']}")
        print(f"Razón social: {pedido['razon_social']}")
        print(f"Estado: {pedido['estado']}")


def interfaz_reporte_pedidos_por_estado():
    """Muestra un submenú para filtrar pedidos por estado."""
    # Diccionario auxiliar para traducir la opción de menú al estado usado en
    # pedidos.csv.
    estados_por_opcion = {
        "1": "Pedido registrado",
        "2": "Pedido recibido",
        "3": "Pedido pendiente",
        "4": "Pedido atendido parcialmente",
        "5": "Pedido atendido",
        "6": "Pedido cancelado",
    }

    # El submenú se mantiene activo para revisar varios estados sin salir de
    # Reportes.
    while True:
        mostrar_menu_estados_reporte()
        opcion = input("Seleccione una opción: ")

        if opcion == "7":
            break

        if opcion not in estados_por_opcion:
            print("\nOpción no válida. Intente nuevamente.")
            continue

        estado = estados_por_opcion[opcion]
        pedidos = obtener_pedidos_por_estado(estado)

        if len(pedidos) == 0:
            print("\nNo se encontraron pedidos con el estado seleccionado.")
            continue

        print(f"\nPedidos con estado: {estado}")
        mostrar_pedidos_reporte(pedidos)


def interfaz_reporte_productos_bajo_stock():
    """Muestra productos con stock menor o igual al límite definido."""
    productos = obtener_productos_bajo_stock(limite=5)

    if len(productos) == 0:
        print("\nNo se encontraron productos con bajo stock.")
        return

    print("\nReporte de productos con bajo stock")
    for producto in productos:
        print(f"\nID: {producto['id_producto']}")
        print(f"Descripción: {producto['descripcion']}")
        print(f"Tipo: {producto['tipo']}")
        print(f"Stock: {producto['stock']}")
        print(f"Precio unitario: S/ {producto['precio_unitario']:.2f}")


def interfaz_reporte_producto_mas_solicitado():
    """Muestra el producto acumulado como más solicitado en los detalles."""
    producto = obtener_producto_mas_solicitado()

    if producto is None:
        print("\nNo hay productos solicitados registrados.")
        return

    print("\nReporte de producto más solicitado")
    print(f"ID del producto: {producto['id_producto']}")
    print(f"Descripción: {producto['descripcion']}")
    print(f"Cantidad total solicitada: {producto['cantidad_total']}")


def interfaz_reporte_clientes_con_pedidos_en_curso():
    """Muestra clientes que tienen pedidos activos."""
    clientes = obtener_clientes_con_pedidos_en_curso()

    if len(clientes) == 0:
        print("\nNo hay clientes con pedidos en curso.")
        return

    print("\nReporte de clientes con pedidos en curso")
    for cliente in clientes:
        print(f"\nRUC: {cliente['ruc_cliente']}")
        print(f"Razón social: {cliente['razon_social']}")
        print(
            "Cantidad de pedidos en curso: "
            f"{cliente['cantidad_pedidos_en_curso']}"
        )


def manejar_reportes():
    """Mantiene activo el módulo de reportes y ejecuta cada reporte disponible."""
    # El usuario puede consultar varios reportes antes de volver al menú
    # principal.
    while True:
        mostrar_menu_reportes()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            interfaz_reporte_general_pedidos()
        elif opcion == "2":
            interfaz_reporte_pedidos_por_estado()
        elif opcion == "3":
            interfaz_reporte_productos_bajo_stock()
        elif opcion == "4":
            interfaz_reporte_producto_mas_solicitado()
        elif opcion == "5":
            interfaz_reporte_clientes_con_pedidos_en_curso()
        elif opcion == "6":
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")


def iniciar_consola():
    """Punto de inicio de la interfaz de consola del sistema."""
    mostrar_bienvenida()

    # Menú principal de la aplicación: se mantiene activo hasta seleccionar
    # la opción Salir.
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
