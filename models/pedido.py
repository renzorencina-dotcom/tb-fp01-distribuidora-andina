class Pedido:
    def __init__(
        self,
        codigo_pedido,
        ruc_cliente,
        razon_social,
        estado="Pedido registrado",
    ):
        self.codigo_pedido = codigo_pedido
        self.ruc_cliente = ruc_cliente
        self.razon_social = razon_social
        self.estado = estado

    def __str__(self):
        return (
            f"Pedido #{self.codigo_pedido} | "
            f"RUC: {self.ruc_cliente} | "
            f"Cliente: {self.razon_social} | "
            f"Estado: {self.estado}"
        )


class DetallePedido:
    def __init__(
        self,
        codigo_pedido,
        id_producto,
        descripcion,
        cantidad,
        precio_unitario,
    ):
        self.codigo_pedido = codigo_pedido
        self.id_producto = id_producto
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario

    def __str__(self):
        return (
            f"Pedido #{self.codigo_pedido} | "
            f"Producto: {self.descripcion} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio unitario: S/ {self.precio_unitario:.2f} | "
            f"Subtotal: S/ {self.subtotal:.2f}"
        )
