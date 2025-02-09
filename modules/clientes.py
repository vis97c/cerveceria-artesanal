# Helpers para trabajar con los clientes
def clientes(correr):

   # Definir y crear tabla de clientes si no existe
   correr('''
      CREATE TABLE IF NOT EXISTS clientes (
         id text,
         nombre text NOT NULL,
         apellido text NOT NULL,
         direccion text NOT NULL,
         telefono text NOT NULL,
         email text NOT NULL,
         PRIMARY KEY (id)
      )
   ''')

   # Crear nuevo cliente
   def crear(valores):
      correr('INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?)', valores)


   # Actualizar nombre de un cliente existente
   def actualizarNombre(identificador, nuevoNombre):
      correr(f'UPDATE clientes SET nombre = "{nuevoNombre}" WHERE id = ?', (identificador))

   # Consultar un unico cliente
   def consultarUno(identificador):
      cursorObj = correr(f'SELECT * FROM clientes WHERE id = ?', (identificador), False)
      
      return cursorObj.fetchall()[0]

   # Borrar un cliente
   def borrar(identificador):
      correr(f'DELETE FROM clientes WHERE id = ?', (identificador))

   return { crear, actualizarNombre, consultarUno, borrar }
