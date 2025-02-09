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
            f"SELECT * FROM clientes WHERE id = ?", (identificador,), False
        )

        return cursorObj.fetchall()[0]

    # Consultar varios clientes
    def consultarVarios(ids=None):
        if ids:
            # Retornar los ids dados si se especifica
            placeholders = ",".join("?" for _ in ids)  # (?, ?) segun la cantidad de ids
            query = f"SELECT * FROM clientes WHERE id IN ({placeholders})"
            cursorObj = correr(query, tuple(ids), False)
        else:
            query = "SELECT * FROM clientes"
            cursorObj = correr(query, persistencia=False)

        return cursorObj.fetchall()

    # Borrar un cliente
    def borrar(identificador):
        correr(f"DELETE FROM clientes WHERE id = ?", (identificador))

    return {
        "crear": crear,
        "actualizarDireccion": actualizarDireccion,
        "consultarUno": consultarUno,
        "borrar": borrar,
    }
