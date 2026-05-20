class Producto:
    """Representa un producto del inventario con stock y precio unitario."""

    def __init__(self, id_producto, descripcion, tipo, stock, precio_unitario):
        self.id_producto = id_producto
        self.descripcion = descripcion
        self.tipo = tipo
        self.stock = stock
        self.precio_unitario = precio_unitario

    def __str__(self):
        return (
            f"ID: {self.id_producto} | "
            f"Descripción: {self.descripcion} | "
            f"Tipo: {self.tipo} | "
            f"Stock: {self.stock} | "
            f"Precio unitario: S/ {self.precio_unitario:.2f}"
        )
