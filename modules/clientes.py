# Helpers para trabajar con los clientes
def clientes(correr):

    # Definir y crear tabla de clientes si no existe
    correr(
        """
      CREATE TABLE IF NOT EXISTS clientes (
         id text,
         nombre text NOT NULL,
         apellido text NOT NULL,
         direccion text NOT NULL,
         telefono text NOT NULL,
         email text NOT NULL,
         PRIMARY KEY (id)
      )
   """
    )

    # Crear nuevo cliente
    def crear(valores):
        correr("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)", valores)

    # Actualizar direccion de un cliente existente
    def actualizarDireccion(identificador, nuevoDireccion):
        correr(
            "UPDATE clientes SET direccion = ? WHERE id = ?",
            (nuevoDireccion, identificador),
        )

    # Consultar un unico cliente
    def consultarUno(identificador):
        cursorObj = correr(
            "SELECT * FROM clientes WHERE id = ?", (identificador,), False
        )

        return cursorObj.fetchall()[0]

    return {
        "crear": crear,
        "actualizarDireccion": actualizarDireccion,
        "consultarUno": consultarUno,
    }
