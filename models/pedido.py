class Pedido:
    def __init__(self, id_pedido, cliente, producto, cantidad):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad

    def __str__(self):
        return (
            f"Pedido #{self.id_pedido} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Producto: {self.producto.nombre} | "
            f"Cantidad: {self.cantidad}"
        )