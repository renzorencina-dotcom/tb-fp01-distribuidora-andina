"""Utilidades de formato compartidas entre servicios."""


def formatear_numero(valor):
    """Devuelve un número como texto sin decimales innecesarios para el CSV.

    Un valor entero (por ejemplo 90.0) se guarda como "90" y uno con parte
    decimal (por ejemplo 3.5) conserva sus decimales. Se usa al escribir
    cantidades, precios y stock para evitar ceros sobrantes en los archivos CSV.
    """
    valor = float(valor)

    if valor.is_integer():
        return str(int(valor))

    return str(valor)
