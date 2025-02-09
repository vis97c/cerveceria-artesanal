import sqlite3
from sqlite3 import Error

# Helpers para trabajar con la db
def conectar():
   try:
      # Conexión con el archivo tipo db con el que se va a trabajar 
      conexion = sqlite3.connect('cerveceria.db')

      # Finalizar conexión de la base de datos dada
      def cerrar():
         conexion.close()

      # Ejecurar SQL condicionalmente
      def correr(instruccion, valores = None, persistencia = True):
         # 1. Recorrer base de datos
         cursorObj = conexion.cursor()

         # 2. SQL a ejecutar, 3. Ejecutar la instrucción SQL
         # Si la tabla existe "IF NOT EXISTS" previene errores
         if valores:
            cursorObj.execute(instruccion, valores)
         else:
            cursorObj.execute(instruccion)

         # 4. Persistencia con el commit
         if persistencia:
            conexion.commit()

         return cursorObj

      # Establezco la conexión y creo la db fisica
      return ( correr, conexion, cerrar )
    
   except Error:
      print(Error)