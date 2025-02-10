# Helpers para trabajar con los productos
def productos(correr):

    # Definir y crear tabla de productos si no existe.
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

    # Función que crea un nuevo producto. Recibe los valores de cada producto y los asigna a la tabla productos.
    def crear(valores):
        correr("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?, ?)", valores)

    # Función que actualiza el nombre de un producto existente. Solicita el ID del producto y el nuevo nombre. Luego actualiza el nombre.
    def actualizarNombre(identificador, nuevoNombre):
        correr(
            "UPDATE productos SET nombre = ? WHERE id = ?", (nuevoNombre, identificador)
        )

    # Función que consulta la información vigente de un producto. Solicita al usuario diligenciar el ID del prodcuto,
    # luego muestra toda la infomación de este, con la creación del objeto cursor que recorre la base de datos.
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
