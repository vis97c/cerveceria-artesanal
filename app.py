# CERVECERÍA ARTESANAL
# Este es el archivo principal de nuestra aplicación
# La lógica de los módulos se divide en los archivos de la ruta "/modules" pera luego ser importados aca 

from flask import Flask, render_template
import atexit

from utils.db import conectar

# INICIALIZAMOS FLASK
# Flask es un framework/librería que nos permite generar un servidor web con python
# Los usuarios interactuaran con la aplicación desde su navegador
app = Flask(__name__, static_url_path="/")

# Función principal de la aplicación
def main():
    # Inicializamos la conexión con la db
    correr, conexion, cerrar = conectar()

    # Cerrar la conexión con la db al salir
    atexit.register(cerrar)

    # RUTAS
    # Separamos los módulos de nuestra aplicación en rutas que pueden ser accedidas desde el navegador
    # Ej: http://localhost:5000

    # Menu principal de la aplicación
    @app.route('/')
    def index():
        return render_template('index.html')

    # PRODUCTOS

    # Vista de gestión de productos
    @app.route('/productos')
    def productos():
        return render_template('productos.html')

    @app.route('/productos/crear')
    def crear_producto():
        return render_template('productos/crear.html')

    @app.route('/productos/actualizar')
    def actualizar_producto():
        return render_template('productos/actualizar.html')

    @app.route('/productos/consultar')
    def consultar_producto():
        return render_template('productos/consultar.html')

    # CLIENTES

    # Vista de gestión de clientes
    @app.route('/clientes')
    def clientes():
        return render_template('clientes.html')

    @app.route('/clientes/crear')
    def crear_cliente():
        return render_template('clientes/crear.html')

    @app.route('/clientes/actualizar')
    def actualizar_cliente():
        return render_template('clientes/actualizar.html')

    @app.route('/clientes/consultar')
    def consultar_cliente():
        return render_template('clientes/consultar.html')

    # VENTAS

    # Vista de ventas
    @app.route('/ventas')
    def ventas():
        return render_template('ventas.html')

    # FACTURACIÓN

    # Vista de facturación
    @app.route('/facturacion')
    def facturacion():
        return render_template('facturacion.html')

main()