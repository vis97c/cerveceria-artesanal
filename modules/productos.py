# Helpers para trabajar con los productos
def productos(correr):

   # Definir y crear tabla de productos si no existe
   correr('''
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
   ''')

   # Crear nuevo producto
   def crear(valores):
      correr('INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?, ?)', valores)


   # Actualizar nombre de un producto existente
   def actualizarNombre(identificador, nuevoNombre):
      correr(f'UPDATE productos SET nombre = "{nuevoNombre}" WHERE id = ?', (identificador))

   # Consultar un unico producto
   def consultarUno(identificador):
      cursorObj = correr(f'SELECT * FROM productos WHERE id = ?', (identificador), False)

      return cursorObj.fetchall()[0]

   # Consultar varios productos
   def consultarVarios(ids = None):
      if ids:
         # Retornar los ids dados si se especifica
         placeholders = ",".join("?" for _ in ids) # (?, ?) segun la cantidad de ids
         query = f"SELECT * FROM productos WHERE id IN ({placeholders})"
         cursorObj = correr(query, tuple(ids), False)
      else:
         query = "SELECT * FROM productos"
         cursorObj = correr(query, persistencia=False)

      return cursorObj.fetchall()

   # Borrar un producto
   def borrar(identificador):
      correr(f'DELETE FROM productos WHERE id = ?', (identificador))

   return { crear, actualizarNombre, consultarUno, consultarVarios, borrar }
