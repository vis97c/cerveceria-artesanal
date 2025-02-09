# CERVECERÍA ARTESANAL
# Este es el archivo principal de nuestra aplicación
# La lógica de los módulos se divide en los archivos de la ruta "/modules" pera luego ser importados aca 

from flask import Flask, render_template, request
import atexit

from utils.db import conectar
from modules.productos import productos
from modules.clientes import clientes

# INICIALIZAMOS FLASK
# Flask es un framework/librería que nos permite generar un servidor web con python
# Los usuarios interactuaran con la aplicación desde su navegador
app = Flask(__name__, static_url_path="/")

# Inicializamos la conexión con la db
correr, conexion, cerrar = conectar()

# Inicializar módulos
productos_module = productos(correr)
clientes_modules = clientes(correr)

# Función principal de la aplicación
def main():
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

    @app.route('/productos/consultar', methods=['GET', 'POST'])
    def consultar_producto():
        producto = None
        if request.method == 'POST':
            try:
                id = int(request.form.get('id'))
                # Usar el método consultarUno del módulo productos
                resultado = productos_module.consultarUno(id)
                if resultado:
                    # Convertir a diccionario para la plantilla
                    producto = {
                        'id': resultado[0],
                        'nombre': resultado[1],
                        'precio': resultado[6]  # precioVenta
                    }
                else:
                    producto = False  # Indicar que el producto no existe
            except Exception as e:
                print(f"Error al consultar producto: {e}")
                producto = False  # También indicamos que no existe si hay error
        return render_template('productos/consultar.html', producto=producto)

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