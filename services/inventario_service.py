def sumar_stock(stock_actual, cantidad):
    return stock_actual + cantidad


def descontar_stock(stock_actual, cantidad):
    nuevo_stock = stock_actual - cantidad

    if nuevo_stock < 0:
        return None

    return nuevo_stock
