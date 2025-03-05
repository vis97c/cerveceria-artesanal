from modules.db import Conectar


# Clase Clientes, para trabajar con los clientes
class Clientes(Conectar):

    # Método que define y crea la tabla de clientes si no existe.
    def __init__(self):
        # Inicializar la clase Conectar (clase padre).
        super().__init__()

        self._correr(
            """
        CREATE TABLE IF NOT EXISTS clientes (
            id integer,
            nombre text NOT NULL,
            apellido text NOT NULL,
            direccion text NOT NULL,
            telefono text NOT NULL,
            email text NOT NULL,
            PRIMARY KEY (id)
        )
    """
        )

    # Método que crea un nuevo cliente.
    def crear(self, valores):
        self._correr("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)", valores)

    # Método que actualiza dirección de un cliente existente.
    def actualizarDireccion(self, identificador, nuevoDireccion):
        self._correr(
            "UPDATE clientes SET direccion = ? WHERE id = ?",
            (nuevoDireccion, identificador),
        )

    # Método que consulta un cliente por su ID.
    def consultarUno(self, identificador):
        cursorObj = self._correr(
            "SELECT * FROM clientes WHERE id = ?", (identificador,), False
        )

        return cursorObj.fetchall()[0]

    # Método que consulta todos los clientes.
    def consultarVarios(self, ordenarPor=None):
        query = "SELECT * FROM clientes"

        if ordenarPor:
            query += f" ORDER BY {ordenarPor[0]} {ordenarPor[1]}"

        cursorObj = self._correr(query, persistencia=False)

        return cursorObj.fetchall()
