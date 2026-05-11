import csv
import os

from models.cliente import Cliente


RUTA_CLIENTES = "data/clientes.csv"


def asegurar_archivo_clientes():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(RUTA_CLIENTES):
        with open(RUTA_CLIENTES, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["id_cliente", "nombre"])


def cargar_clientes():
    # Lee el CSV de clientes y convierte cada fila valida en un objeto Cliente.
    clientes = []
    asegurar_archivo_clientes()

    with open(RUTA_CLIENTES, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        filas = list(lector)

        if filas and filas[0] == ["id_cliente", "nombre"]:
            filas = filas[1:]

        for fila in filas:
            # Ignora filas incompletas para evitar errores al crear el cliente.
            if len(fila) < 2:
                continue

            cliente = Cliente(fila[0], fila[1])
            clientes.append(cliente)

    return clientes


def guardar_cliente(cliente):
    # Agrega un cliente nuevo al final del archivo sin borrar los registros anteriores.
    asegurar_archivo_clientes()

    with open(RUTA_CLIENTES, mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([cliente.id_cliente, cliente.nombre])


def guardar_clientes(clientes):
    # Reescribe el archivo completo; se usa, por ejemplo, despues de borrar clientes.
    asegurar_archivo_clientes()

    with open(RUTA_CLIENTES, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        for cliente in clientes:
            escritor.writerow([cliente.id_cliente, cliente.nombre])
