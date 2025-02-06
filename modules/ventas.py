# Helpers para trabajar con los ventas
#
# El id de la venta se define asi: "factura_conteo"
# En la aplicacion se muestran las ventas asociadas a un factura como una sola
def ventas(correr):

   # Definir y crear tabla de ventas si no existe
   correr('''
      CREATE TABLE IF NOT EXISTS ventas (
         id text,
         factura interger,
         venta text NOT NULL,
         producto text NOT NULL,
         cantidad interger NOT NULL,
         PRIMARY KEY (factura)
      )
   ''')

   # Crear nueva venta
   def crear(valores):
      correr('INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?)', valores)

   # Consultar una unica venta
   def consultarUna(factura):
      cursorObj = correr(f'SELECT * FROM ventas WHERE factura = ?', (factura), False)
      
      return cursorObj.fetchall()[0]

   # Consultar varias ventas
   def consultarVarias(facturas = None):
      if facturas:
         # Retornar los facturas dados si se especifica
         placeholders = ",".join("?" for _ in facturas) # (?, ?) segun la cantidad de facturas
         query = f"SELECT * FROM ventas WHERE factura IN ({placeholders})"
         cursorObj = correr(query, tuple(facturas), False)
      else:
         query = "SELECT * FROM ventas"
         cursorObj = correr(query, persistencia=False)
      
      return cursorObj.fetchall()

   # Borrar un venta con un producto especifico
   def borrar(factura, producto):
      correr(f'DELETE FROM ventas WHERE factura = ? AND producto = ?', (factura, producto))

   return { crear, consultarUna, consultarVarias, borrar }
