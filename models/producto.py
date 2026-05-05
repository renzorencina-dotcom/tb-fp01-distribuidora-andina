class Producto:
    def __init__(self, id_producto, nombre, stock, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock = stock
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} | Stock: {self.stock} | Precio: S/ {self.precio:.2f}"
