# Helpers para trabajar con los ventas
#
# El id de la venta se define asi: "factura_producto"
# En la aplicacion se muestran las ventas asociadas a un factura como una sola
def ventas(correr):

    # Definir y crear tabla de ventas si no existe
    correr(
        """
      CREATE TABLE IF NOT EXISTS ventas (
         id text,
         factura interger,
         cliente text NOT NULL,
         producto text NOT NULL,
         cantidad interger NOT NULL,
         PRIMARY KEY (id)
      )
   """
    )

    # Crear nueva venta
    def crear(valores):
        correr("INSERT INTO ventas VALUES (?, ?, ?, ?, ?)", valores)

    # Consultar una unica venta
    def consultarUna(factura):
        cursorObj = correr("SELECT * FROM ventas WHERE factura = ?", (factura,), False)

        return cursorObj.fetchall()[0]

    # Consultar varias ventas
    # Metodo usado en facturacion
    def consultarVarias(factura=None):
        if factura:
            # Retornar los ventas por factura
            cursorObj = correr(
                "SELECT * FROM ventas WHERE factura = ?", (factura,), False
            )
        else:
            cursorObj = correr("SELECT * FROM ventas", persistencia=False)

        return cursorObj.fetchall()

    # Borrar un venta con un producto especifico
    # Metodo usado en facturacion
    def borrar(factura, producto):
        correr(
            "DELETE FROM ventas WHERE factura = ? AND producto = ?", (factura, producto)
        )

    return {
        "crear": crear,
        "consultarUna": consultarUna,
        "consultarVarias": consultarVarias,
        "borrar": borrar,
    }
