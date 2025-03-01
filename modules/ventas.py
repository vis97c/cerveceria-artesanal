from modules.db import Conectar


# Clase Ventas, para trabajar con los ventas
# El ID de la venta se define asi: "factura_producto"
# En la aplicacion se muestran las ventas asociadas a un factura como una sola
class Ventas(Conectar):

    # Método que define y crea la tabla de ventas si no existe
    def __init__(self):
        # Inicializar la clase Conectar (clase padre)
        super().__init__()

        self._correr(
            """
        CREATE TABLE IF NOT EXISTS ventas (
            id text,
            factura integer NOT NULL,
            cliente integer NOT NULL,
            producto integer NOT NULL,
            cantidad integer NOT NULL,
            PRIMARY KEY (id)
        )
    """
        )

    # Método que crea una nueva venta
    def crear(self, valores):
        self._correr("INSERT INTO ventas VALUES (?, ?, ?, ?, ?)", valores)

    # Método que consulta una única venta
    def consultarUna(self, factura):
        cursorObj = self._correr(
            "SELECT * FROM ventas WHERE factura = ?", (factura,), False
        )

        return cursorObj.fetchall()[0]

    # Método que consulta varias ventas en facturación
    def consultarVarias(self, factura=None):
        if factura:
            # Retornar los ventas por factura
            cursorObj = self._correr(
                "SELECT * FROM ventas WHERE factura = ?", (factura,), False
            )
        else:
            cursorObj = self._correr("SELECT * FROM ventas", persistencia=False)

        return cursorObj.fetchall()

    # Método que borra una venta con un producto específico, usado en facturación
    def borrar(self, factura, producto):
        self._correr(
            "DELETE FROM ventas WHERE factura = ? AND producto = ?", (factura, producto)
        )
