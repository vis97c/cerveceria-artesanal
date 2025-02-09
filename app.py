# CERVECERÍA ARTESANAL
# Este es el archivo principal de nuestra aplicación
# La lógica de los módulos se divide en los archivos de la ruta "/modules" pera luego ser importados aca

from flask import Flask, render_template, request, redirect
import atexit
from datetime import datetime

from utils.db import conectar
from modules.productos import productos

# INICIALIZAMOS FLASK
# Flask es un framework/librería que nos permite generar un servidor web con python
# Los usuarios interactuaran con la aplicación desde su navegador
app = Flask(__name__, static_url_path="/")


# Función principal de la aplicación
def main():
    # RUTAS
    # Separamos los módulos de nuestra aplicación en rutas que pueden ser accedidas desde el navegador
    # Ej: http://localhost:5000

    # Menu principal de la aplicación
    @app.route("/")
    def index():
        return render_template("index.html")

    # PRODUCTOS

    # Vista de gestión de productos
    @app.route("/productos")
    def productos_vista():
        return render_template("productos.html")

    # Vista para crear un nuevo producto
    @app.route("/productos/crear", methods=["GET", "POST"])
    def crear_producto():
        error = None
        success = None

        if request.method == "POST":
            correr, conexion, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                # Obtener todos los campos del formulario
                productId = int(request.form.get("id"))
                nombre = request.form.get("nombre")
                peso = int(request.form.get("peso"))
                volumen = int(request.form.get("volumen"))
                precioProduccion = int(request.form.get("precioProduccion"))
                precioVenta = int(request.form.get("precioVenta"))

                # Convertir fecha de YYYY-MM-DD a DD/MM/YYYY
                fecha = request.form.get("vencimiento")
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                vencimiento = fecha_obj.strftime("%d/%m/%Y")

                # Crear el producto con todos los valores
                moduloProductos["crear"](
                    (
                        productId,
                        nombre,
                        peso,
                        volumen,
                        vencimiento,
                        precioProduccion,
                        precioVenta,
                    )
                )
                success = f'Producto con el id "{productId}" fue creado exitosamente'

            except Exception as err:
                print(f"Error al crear producto: {err}")

                if "UNIQUE constraint failed" in str(err):
                    error = "Ya existe un producto con ese ID"
                else:
                    error = "Error al crear el producto"

            cerrar()  # Cerrar la conexión

        return render_template("productos/crear.html", error=error, success=success)

    # Vista para actualizar el nombre de un producto existente
    @app.route("/productos/actualizar", methods=["GET", "POST"])
    def actualizar_producto():
        error = None
        success = None

        if request.method == "POST":
            correr, conexion, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                productId = int(request.form.get("id"))
                nuevo_nombre = request.form.get("nombre")

                # Actualizar nombre del producto
                moduloProductos["actualizarNombre"](productId, nuevo_nombre)
                success = (
                    f'Producto con el id "{productId}" fue actualizado exitosamente'
                )

            except Exception as err:
                print(f"Error al actualizar producto: {err}")
                error = "Error al actualizar el producto"

            cerrar()  # Cerrar la conexión

        return render_template(
            "productos/actualizar.html", error=error, success=success
        )

    # Vista para consultar un producto existente
    @app.route("/productos/consultar", methods=["GET", "POST"])
    def consultar_producto():
        producto = None

        if request.method == "POST":
            correr, conexion, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                productId = int(request.form.get("id"))
                # Obtener producto con el id
                resultado = moduloProductos["consultarUno"](productId)

                if resultado:
                    producto = {
                        "id": resultado[0],
                        "nombre": resultado[1],
                        "peso": resultado[2],
                        "volumen": resultado[3],
                        "vencimiento": resultado[4],
                        "produccion": resultado[5],
                        "precio": resultado[6],
                    }
                else:
                    producto = False  # Indicar que el producto no existe

            except Exception as err:
                print(f"Error al consultar producto: {err}")
                producto = False  # Tambien indicamos que no existe si hay error

            cerrar()  # Cerrar la conexión

        return render_template("productos/consultar.html", producto=producto)

    # CLIENTES

    # Vista de gestión de clientes
    @app.route("/clientes")
    def clientes():
        return render_template("clientes.html")

    # Vista para crear un nuevo cliente
    @app.route("/clientes/crear")
    def crear_cliente():
        return render_template("clientes/crear.html")

    # Vista para actualizar la direccion de un cliente existente
    @app.route("/clientes/actualizar")
    def actualizar_cliente():
        return render_template("clientes/actualizar.html")

    # Vista para consultar un cliente existente
    @app.route("/clientes/consultar")
    def consultar_cliente():
        return render_template("clientes/consultar.html")

    # VENTAS

    # Vista de ventas
    @app.route("/ventas")
    def ventas():
        return render_template("ventas.html")

    # FACTURACIÓN

    # Vista de facturación
    @app.route("/facturacion")
    def facturacion():
        return render_template("facturacion.html")


main()
