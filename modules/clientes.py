# Helpers para trabajar con los clientes
def clientes(correr):

    # Definir y crear tabla de clientes si no existe.
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

    # Función que crea un nuevo cliente. Solicitando los 6 argumentos, (número de identificación (ID), nombre, apellido, dirección, teléfono, correo electrónico)
    def crear(valores):
        correr("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)", valores)

    # Función que actualiza dirección de un cliente existente. Solicitando 2 argumentos (ID cliente y nueva dirección) 
    def actualizarDireccion(identificador, nuevoDireccion):
        correr(
            "UPDATE clientes SET direccion = ? WHERE id = ?",
            (nuevoDireccion, identificador),
        )

    # Función que consulta la información de un cliente. A partir del ID del cliente, muestra la información vigente. Para esto se requiere un objeto cursor que recorre la base de datos 
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
