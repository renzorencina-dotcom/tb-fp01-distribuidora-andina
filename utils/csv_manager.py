"""Utilidades compartidas para manejar archivos CSV del sistema.

Este módulo centraliza la lectura, escritura, búsqueda y eliminación de
registros CSV para evitar repetir la misma lógica en clientes, productos,
pedidos y reportes.
"""

import csv
import os


def asegurar_directorio(ruta):
    """Crea el directorio destino si la ruta del CSV lo requiere."""
    directorio = os.path.dirname(ruta)

    if directorio:
        os.makedirs(directorio, exist_ok=True)


def leer_csv(ruta):
    """Lee un CSV y devuelve sus filas como una lista de diccionarios."""
    # Si el archivo aún no fue creado o está vacío, se devuelve una lista
    # vacía para que los servicios puedan trabajar sin errores iniciales.
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return []

    with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        if lector.fieldnames is None:
            return []

        return list(lector)


def escribir_csv(ruta, datos, campos):
    """Escribe una lista de diccionarios en un CSV con encabezados definidos."""
    asegurar_directorio(ruta)

    # Se sobrescribe el archivo completo porque las operaciones de actualizar
    # o eliminar trabajan con una lista ya modificada en memoria.
    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)


def agregar_fila_csv(ruta, fila, campos):
    """Agrega una fila nueva conservando los registros existentes."""
    datos = leer_csv(ruta)
    datos.append(fila)
    escribir_csv(ruta, datos, campos)


def buscar_por_campo(ruta, campo, valor):
    """Busca la primera fila cuyo campo coincida con el valor recibido."""
    datos = leer_csv(ruta)

    # Cada fila del CSV se representa como diccionario; el recorrido permite
    # encontrar coincidencias sin que cada servicio repita esta búsqueda.
    for fila in datos:
        if fila.get(campo) == valor:
            return fila

    return None


def eliminar_fila_csv(ruta, campo, valor, campos):
    """Elimina una fila por coincidencia de campo y devuelve la fila eliminada."""
    datos = leer_csv(ruta)
    datos_actualizados = []
    fila_eliminada = None

    # Se recorre todo el archivo para separar la fila encontrada de las filas
    # que deben permanecer antes de reescribir el CSV actualizado.
    for fila in datos:
        if fila.get(campo) == valor:
            fila_eliminada = fila
        else:
            datos_actualizados.append(fila)

    if fila_eliminada is None:
        return None

    escribir_csv(ruta, datos_actualizados, campos)
    return fila_eliminada
