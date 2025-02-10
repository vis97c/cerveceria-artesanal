# Helpers para trabajar con los productos
def productos(correr):

    # Definir y crear tabla de productos si no existe
    correr(
        """
      CREATE TABLE IF NOT EXISTS productos (
         id interger,
         nombre text NOT NULL,
         peso interger NOT NULL,
         volumen interger NOT NULL,
         vencimiento date NOT NULL,
         precioProduccion interger NOT NULL,
         precioVenta interger NOT NULL,
         PRIMARY KEY (id)
      )
   """
    )

    # Crear nuevo producto
    def crear(valores):
        correr("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?, ?)", valores)

    # Actualizar nombre de un producto existente
    def actualizarNombre(identificador, nuevoNombre):
        correr(
            "UPDATE productos SET nombre = ? WHERE id = ?", (nuevoNombre, identificador)
        )

    # Consultar un unico producto
    def consultarUno(identificador):
        cursorObj = correr(
            "SELECT * FROM productos WHERE id = ?", (identificador,), False
        )

        return cursorObj.fetchall()[0]

    return {
        "crear": crear,
        "actualizarNombre": actualizarNombre,
        "consultarUno": consultarUno,
    }
