from modules.db import Conectar

# Helpers para trabajar con los ventas
#
# El id de la venta se define asi: "factura_producto"
# En la aplicacion se muestran las ventas asociadas a un factura como una sola
class Ventas(Conectar):

    def __init__(self):
        # Definir y crear tabla de ventas si no existe
        self._correr(
            """
        CREATE TABLE IF NOT EXISTS ventas (
            id text,
            factura interger,
            cliente text NOT NULL,
            producto text NOT NULL,
            cantidad interger NOT NULL,
            PRIMARY KEY (factura)
        )
    """
        )

    # Crear nueva venta
    def crear(self,valores):
        self._correr("INSERT INTO ventas VALUES (?, ?, ?, ?, ?)", valores)

    # Consultar una unica venta
    def consultarUna(self, factura):
        cursorObj = self._correr("SELECT * FROM ventas WHERE factura = ?", (factura,), False)

        return cursorObj.fetchall()[0]

    # Consultar varias ventas
    # Metodo usado en facturacion
    def consultarVarias(self, factura=None):
        if factura:
            # Retornar los ventas por factura
            cursorObj = self._correr(
                "SELECT * FROM ventas WHERE factura = ?", (factura,), False
            )
        else:
            cursorObj = self._correr("SELECT * FROM ventas", persistencia=False)

        return cursorObj.fetchall()

    # Borrar un venta con un producto especifico
    # Metodo usado en facturacion
    def borrar(self, factura, producto):
        self._correr(
            "DELETE FROM ventas WHERE factura = ? AND producto = ?", (factura, producto)
        )

