from modules.db import Conectar

# Clase para trabajar con los productos
class Productos(Conectar):

    # Método que define y crea la tabla de productos si no existe.
    def __init__(self):
        # Inicializar la clase Conectar (clase padre)
        super().__init__()
        
        self._correr(
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

    # Método que crea un nuevo producto. Recibe los valores de cada producto y los asigna a la tabla productos.
    def crear(self,valores):
        self._correr("INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?, ?)", valores)

    # Método que actualiza el nombre de un producto existente. Solicita el ID del producto y el nuevo nombre. Luego actualiza el nombre.
    def actualizarNombre(self,identificador, nuevoNombre):
        self._correr(
            "UPDATE productos SET nombre = ? WHERE id = ?", (nuevoNombre, identificador)
        )

    # Método que consulta la información vigente de un producto. Solicita al usuario diligenciar el ID del prodcuto, 
    # luego muestra toda la infomación de este, con la creación del objeto cursor que recorre la base de datos.
    def consultarUno(self,identificador):
        cursorObj = self._correr(
            "SELECT * FROM productos WHERE id = ?", (identificador,), False
        )

        return cursorObj.fetchall()[0]

    
