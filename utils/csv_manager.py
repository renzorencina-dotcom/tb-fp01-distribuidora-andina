import csv
import os


def asegurar_directorio(ruta):
    directorio = os.path.dirname(ruta)

    if directorio:
        os.makedirs(directorio, exist_ok=True)


def leer_csv(ruta):
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []

    with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames is None:
            return []

        return list(lector)


def escribir_csv(ruta, datos, campos):
    asegurar_directorio(ruta)

    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)


def agregar_fila_csv(ruta, fila, campos):
    datos = leer_csv(ruta)
    datos.append(fila)
    escribir_csv(ruta, datos, campos)


def buscar_por_campo(ruta, campo, valor):
    datos = leer_csv(ruta)

    for fila in datos:
        if fila.get(campo) == valor:
            return fila

    return None


def eliminar_fila_csv(ruta, campo, valor, campos):
    datos = leer_csv(ruta)
    datos_actualizados = []
    fila_eliminada = None

    for fila in datos:
        if fila.get(campo) == valor:
            fila_eliminada = fila
        else:
            datos_actualizados.append(fila)

    if fila_eliminada is None:
        return None

    escribir_csv(ruta, datos_actualizados, campos)
    return fila_eliminada
