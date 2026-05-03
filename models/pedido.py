class Pedido:
    def __init__(self, id_pedido, cliente, producto, cantidad):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad