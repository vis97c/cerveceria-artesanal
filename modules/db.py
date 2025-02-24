import sqlite3
from sqlite3 import Error


# Clase Conectar, para trabajar con la base de datos
class Conectar:
    
    def __init__(self):
        try:
            # Conexión con el archivo tipo db con el que se va a trabajar
            self.__conexion = sqlite3.connect("cerveceria.db")
        except Error:
            print(Error)

    # Método de conexión con la base de datos dada
    def cerrar(self):
        self.__conexion.close()

    # Método para ejecutar SQL condicionalmente
    def _correr(self,instruccion, valores=None, persistencia=True):
        # Pasos:
        # 1. Recorrer base de datos
        cursorObj = self.__conexion.cursor()

        # 2. SQL a ejecutar 
        # 3. Ejecutar la instrucción SQL
        # Si la tabla existe "IF NOT EXISTS" previene errores###
        if valores:
            cursorObj.execute(instruccion, valores)
        else:
            cursorObj.execute(instruccion)

        # 4. Persistencia con el commit
        if persistencia:
            self.__conexion.commit()

        return cursorObj
        

    
