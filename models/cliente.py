class Cliente:
    """Representa a un cliente identificado por su RUC dentro del sistema."""

    def __init__(self, ruc, razon_social, telefono, direccion):
        self.ruc = ruc
        self.razon_social = razon_social
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return (
            f"RUC: {self.ruc} | "
            f"Razón social: {self.razon_social} | "
            f"Teléfono: {self.telefono} | "
            f"Dirección: {self.direccion}"
        )
