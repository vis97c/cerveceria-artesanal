# CERVECERÍA ARTESANAL
# Este es el archivo principal de nuestra aplicación
# La lógica de los módulos se divide en los archivos de la ruta "/modules" pera luego ser importados acá
# La aplicación se puede iniciar al ejecutar el archivo app.py, ya sea desde la consola o desde el IDLE.

import os
import socket
import pdfkit
from flask import Flask, render_template, request, redirect
from flaskwebgui import FlaskUI, close_application
from datetime import datetime

# Para minimizar el código en este archivo separamos la lógica por módulos
from modules.productos import Productos
from modules.clientes import Clientes
from modules.ventas import Ventas
from modules.correo import enviarCorreo

currentDir = os.path.dirname(os.path.abspath(__file__))
templateFolder = os.path.join(currentDir, "templates")
staticFolder = os.path.join(currentDir, "static")

# Pdfkit usado para generar pdfs requiere wkhtmltopdf
wkhtmltopdfPath = os.path.join(currentDir, "wkhtmltopdf", "bin", "wkhtmltopdf.exe")
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdfPath)

# INICIALIZAMOS FLASK
# Flask es un framework/librería que nos permite generar un servidor web con python
# Al adicionar pyinstaller y flaskwebgui se genera un ejecutable que puede ser usado por usuarios sin cononocimientos de python
# Los usuarios interactuaran con la aplicación desde la ventana de la aplicacion
# SQlite3 se abre y cierra por cada request para evitar errores debido al multithreading de flask
app = Flask(
    __name__,
    static_url_path="/",
    template_folder=templateFolder,
    static_folder=staticFolder,
)
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Función principal de la aplicación donde definimos las rutas y vistas
# Las vistas se encuentran en templates y son archivos html que se renderizan cuando se accede a una ruta
# Flask permite usar un pseudo lenguaje de templates llamado Jinja2 y que permite inyectar datos de python
# Estos datos se pasan a la funcion render_template junto a las variables que vayamos a usar
def main():
    # RUTAS PRINCIPALES
    # Separamos los módulos de nuestra aplicación en rutas que pueden ser accedidas desde la aplicacion
    # Ej: http://localhost:5000

    # Ruta del menú de la página de inicio.
    # La función abajo del @app.route("/") usará la dirección que está dentro de los paréntesis y el render_template buscará y devolverá el archivo html
    @app.route("/")
    def index():
        return render_template("index.html")

    # GESTIÓN DE PRODUCTOS

    # Vista de gestión de productos
    # Permite listar todos los productos en la base de datos
    @app.route("/productos")
    def productos_vista():
        productos = []
        moduloProductos = Productos()

        # Definir orden de tabulacion
        orden = request.args.get("order", "ASC")
        columna = request.args.get("column", "id")

        # Funcion para mostrar el orden segun la columna
        def mostrarOrden(nuevaColumna):
            if nuevaColumna == columna:
                return "DESC" if orden == "ASC" else "ASC"
            else:
                return "ASC"

        try:

            # Obtener todos los productos de la base de datos
            resultado = moduloProductos.consultarVarios((columna, orden))

            if resultado and len(resultado) > 0:
                for producto in resultado:
                    productos.append(
                        {
                            # Información del producto
                            "id": producto[0],
                            "nombre": producto[1],
                            "volumen": producto[2],
                            "vencimiento": producto[3],
                            "precioProduccion": producto[4],
                            "precioVenta": producto[5],
                        }
                    )

        except Exception as err:
            print(f"Error al consultar productos: {err}")
            productos = []

        moduloProductos.cerrar()  # Cerrar la conexión con la base de datos

        return render_template(
            "productos/index.html",
            debug=app.debug,
            productos=productos,
            mostrarOrden=mostrarOrden,
        )

    # Vista para crear un nuevo producto, con los métodos para visualizar la página ("GET") y para recibir datos ("POST")
    @app.route("/productos/crear", methods=["GET", "POST"])
    def crear_producto():
        error = None
        success = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Productos para gestionar los productos en la base de datos
            moduloProductos = Productos()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                productId = int(request.form.get("id"))
                nombre = request.form.get("nombre")
                volumen = int(request.form.get("volumen"))
                precioProduccion = int(request.form.get("precioProduccion"))
                precioVenta = int(request.form.get("precioVenta"))

                # Convertir fecha de YYYY-MM-DD a DD/MM/YYYY
                fecha = request.form.get("vencimiento")
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                vencimiento = fecha_obj.strftime("%d/%m/%Y")

                # Se llama al método "crear" del objeto moduloProductos y crear el producto con todos los valores en la base de datos.
                moduloProductos.crear(
                    (
                        productId,
                        nombre,
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

            moduloProductos.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("productos/crear.html", error=error, success=success)

    # Vista para actualizar el nombre de un producto existente
    @app.route("/productos/actualizar", methods=["GET", "POST"])
    def actualizar_producto():
        error = None
        success = None

        if request.method == "POST":
            moduloProductos = Productos()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                productId = int(request.form.get("id"))
                nuevoNombre = request.form.get("nombre")

                # Se llama al método "actualizarNombre" del objeto moduloProductos y actualizar el nombre del producto
                moduloProductos.actualizarNombre(productId, nuevoNombre)
                success = (
                    f'Producto con el id "{productId}" fue actualizado exitosamente'
                )

            except Exception as err:
                print(f"Error al actualizar producto: {err}")
                error = "Error al actualizar el producto"

            moduloProductos.cerrar()  # Cerrar la conexión con la base de datos

        return render_template(
            "productos/actualizar.html", error=error, success=success
        )

    # Vista para consultar un producto existente
    @app.route("/productos/consultar", methods=["GET", "POST"])
    def consultar_producto():
        producto = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Productos para gestionar los productos en la base de datos
            moduloProductos = Productos()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                productId = int(request.form.get("id"))
                # Se llama al método "consultarUno" del objeto moduloProductos y se obtiene el producto con el id
                resultado = moduloProductos.consultarUno(productId)

                if resultado:
                    producto = {
                        "id": resultado[0],
                        "nombre": resultado[1],
                        "volumen": resultado[2],
                        "vencimiento": resultado[3],
                        "produccion": resultado[4],
                        "precio": resultado[5],
                    }
                else:
                    producto = False  # Indicar que el producto no existe

            except Exception as err:
                print(f"Error al consultar producto: {err}")
                producto = False  # También indicamos que no existe si hay error

            moduloProductos.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("productos/consultar.html", producto=producto)

    # GESTIÓN DE CLIENTES

    # Vista de gestión de clientes
    # Permite listar todos los clientes en la base de datos
    @app.route("/clientes")
    def clientes_vista():
        clientes = []
        moduloClientes = Clientes()

        # Definir orden de tabulacion
        orden = request.args.get("order", "ASC")
        columna = request.args.get("column", "id")

        # Funcion para mostrar el orden segun la columna
        def mostrarOrden(nuevaColumna):
            if nuevaColumna == columna:
                return "DESC" if orden == "ASC" else "ASC"
            else:
                return "ASC"

        try:

            # Obtener todos los clientes de la base de datos
            resultado = moduloClientes.consultarVarios((columna, orden))

            if resultado and len(resultado) > 0:
                for cliente in resultado:
                    clientes.append(
                        {
                            # Información del cliente
                            "id": cliente[0],
                            "nombre": cliente[1],
                            "apellido": cliente[2],
                            "direccion": cliente[3],
                            "telefono": cliente[4],
                            "email": cliente[5],
                        }
                    )

        except Exception as err:
            print(f"Error al consultar clientes: {err}")
            clientes = []

        moduloClientes.cerrar()  # Cerrar la conexión con la base de datos

        return render_template(
            "clientes/index.html",
            debug=app.debug,
            clientes=clientes,
            mostrarOrden=mostrarOrden,
        )

    # Vista para crear un nuevo cliente
    @app.route("/clientes/crear", methods=["GET", "POST"])
    def crear_cliente():
        error = None
        success = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Clientes para gestionar los clientes en la base de datos
            moduloClientes = Clientes()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                clienteId = int(request.form.get("id"))
                nombre = request.form.get("nombre")
                apellido = request.form.get("apellido")
                direccion = request.form.get("direccion")
                telefono = request.form.get("telefono")
                email = request.form.get("email")

                # Se llama al método "crear" del objeto moduloClientes y se crea el cliente con todos los valores
                moduloClientes.crear(
                    (clienteId, nombre, apellido, direccion, telefono, email)
                )
                success = f'Cliente con el id "{clienteId}" fue creado exitosamente'

            except Exception as err:
                print(f"Error al crear cliente: {err}")

                if "UNIQUE constraint failed" in str(err):
                    error = "Ya existe un cliente con ese ID"
                else:
                    error = "Error al crear el cliente"

            moduloClientes.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("clientes/crear.html", error=error, success=success)

    # Vista para actualizar la dirección de un cliente existente
    @app.route("/clientes/actualizar", methods=["GET", "POST"])
    def actualizar_cliente():
        error = None
        success = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Clientes para gestionar los clientes en la base de datos
            moduloClientes = Clientes()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                clienteId = int(request.form.get("id"))
                nuevaDireccion = request.form.get("direccion")

                # Se llama al método "actualizarDireccion" del objeto moduloClientes y se actualiza la dirección del cliente
                moduloClientes.actualizarDireccion(clienteId, nuevaDireccion)
                success = f'Dirección del cliente con id "{clienteId}" actualizada exitosamente'

            except Exception as err:
                print(f"Error al actualizar dirección: {err}")
                if str(err) == "NO_EXISTE":
                    error = "No existe un cliente con ese ID"
                else:
                    error = "Error al actualizar la dirección"

            moduloClientes.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("clientes/actualizar.html", error=error, success=success)

    # Vista para consultar un cliente existente
    @app.route("/clientes/consultar", methods=["GET", "POST"])
    def consultar_cliente():
        cliente = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Clientes para gestionar los clientes en la base de datos
            moduloClientes = Clientes()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                clienteId = int(request.form.get("id"))
                # Se llama al método "consultarUno" del objeto moduloClientes y se obtiene el cliente con el id.
                resultado = moduloClientes.consultarUno(clienteId)

                if resultado:
                    cliente = {
                        "id": resultado[0],
                        "nombre": resultado[1],
                        "apellido": resultado[2],
                        "direccion": resultado[3],
                        "telefono": resultado[4],
                        "email": resultado[5],
                    }
                else:
                    cliente = False  # Indicar que el cliente no existe

            except Exception as err:
                print(f"Error al consultar cliente: {err}")
                cliente = False  # También indicamos que no existe si hay error

            moduloClientes.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("clientes/consultar.html", cliente=cliente)

    # GESTIÓN DE VENTAS

    # Vista de ventas
    @app.route("/ventas")
    def ventas_vista():
        return render_template("ventas/index.html")

    # Vista para crear una nueva venta
    @app.route("/ventas/crear", methods=["GET", "POST"])
    def crear_venta():
        error = None
        success = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Ventas para gestionar las ventas en la base de datos
            moduloVentas = Ventas()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                clienteId = int(request.form.get("clienteId"))
                productoId = int(request.form.get("productoId"))
                cantidad = int(request.form.get("cantidad"))
                factura = int(request.form.get("factura"))

                # Generar ID de venta
                ventaId = f"{factura}_{productoId}"

                #  Se llama al método "crear" del objeto moduloVentas y se crea la venta
                moduloVentas.crear((ventaId, factura, clienteId, productoId, cantidad))
                success = f"Venta con id {ventaId} creada exitosamente"

            except Exception as err:
                print(f"Error al crear venta: {err}")
                if "UNIQUE constraint failed" in str(err):
                    error = "Ya existe una venta con ese ID"
                else:
                    error = "Error al crear la venta"

            moduloVentas.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("ventas/crear.html", error=error, success=success)

    # Vista para borrar una venta existente
    @app.route("/ventas/borrar", methods=["GET", "POST"])
    def borrar_venta():
        error = None
        success = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Ventas para gestionar las ventas en la base de datos
            moduloVentas = Ventas()

            try:
                # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
                factura = int(request.form.get("factura"))
                producto = int(request.form.get("producto"))

                # Se llama al método "borrar" del objeto moduloVentas y se borra la venta
                moduloVentas.borrar(factura, producto)
                success = f"Venta de producto {producto} en factura {factura} eliminada exitosamente"

            except Exception as err:
                print(f"Error al borrar venta: {err}")
                error = "Error al borrar la venta"

            moduloVentas.cerrar()  # Cerrar la conexión con la base de datos

        return render_template("ventas/borrar.html", error=error, success=success)

    # FACTURACIÓN

    # Vista de facturación
    @app.route("/facturacion", methods=["GET", "POST"])
    def facturacion_vista():
        factura = None

        if request.method == "POST":
            # Se instancia un objeto de la clase Ventas para obtener datos de las ventas en la base de datos
            moduloVentas = Ventas()

            # Obtenemos datos del formulario enviados por el usuario en el html con request.from.get("")
            facturaId = int(request.form.get("id"))

            if facturaId:
                # Obtener factura con el id
                resultado = moduloVentas.consultarVarias(facturaId)

                moduloVentas.cerrar()  # Cerrar la conexión

                # Redireccionamos a la vista de factura
                if resultado and len(resultado) > 0:
                    return redirect(f"/facturacion/{facturaId}")
                else:
                    factura = False

        return render_template("facturacion/index.html", factura=factura)

    # Vista de factura
    @app.route("/facturacion/<facturaId>", methods=["GET", "POST"])
    def ver_factura(facturaId):
        correo = None
        factura = None
        pdf = False
        # Se instancian los objeto de las clases Ventas, Clientes y Productos para obtener informacion de la base de datos
        moduloVentas = Ventas()
        moduloClientes = Clientes()
        moduloProductos = Productos()

        try:
            # Obtener factura con el id
            resultado = moduloVentas.consultarVarias(facturaId)

            if request.args.get("pdfkit"):
                pdf = True

            if resultado and len(resultado) > 0:
                clienteId = resultado[0][2]
                cliente = moduloClientes.consultarUno(clienteId)
                email = cliente[5]
                # Definimos la estructura de la factura
                factura = {
                    "id": facturaId,
                    "productos": [],
                    "cliente": {
                        "id": clienteId,
                        "nombre": cliente[1],
                        "apellido": cliente[2],
                        "direccion": cliente[3],
                        "telefono": cliente[4],
                        "email": email,
                    },
                    "total": 0,
                }

                for venta in resultado:
                    productoId = venta[3]
                    cantidad = venta[4]
                    producto = moduloProductos.consultarUno(productoId)
                    precio = producto[5]

                    # Listar productos
                    factura["productos"].append(
                        {
                            "idProducto": productoId,
                            "cantidad": cantidad,
                            # Información adicional del producto
                            "nombre": producto[1],
                            "volumen": producto[2],
                            "vencimiento": producto[3],
                            "produccion": producto[4],
                            "precio": precio,
                        }
                    )

                    # Sumar al total
                    factura["total"] += cantidad * precio

                if request.method == "POST":
                    try:
                        # Genera el PDF en memoria
                        attachment = pdfkit.from_url(
                            f"{request.scheme}://{request.host}{request.path}?pdfkit=1",
                            configuration=config,
                        )

                        # Envía el correo
                        enviarCorreo(
                            email,
                            f"Factura #{facturaId}. Cervecería artesanal",
                            "Aquí esta tu factura de compra",
                            attachment,
                            f"factura_{facturaId}",
                        )
                        correo = True

                    except Exception as err:
                        print(f"Error al enviar correo: {err}")
                        correo = False
            else:
                factura = False  # Indicar que la factura no existe

        except Exception as err:
            print(f"Error al consultar factura: {err}")
            factura = False  # También indicamos que no existe si hay error

        # Cerrar la conexión con la base de datos
        moduloProductos.cerrar()
        moduloVentas.cerrar()
        moduloClientes.cerrar()

        return render_template(
            "facturacion/factura.html",
            factura=factura,
            correo=correo,
            pdf=pdf,
            fecha=datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S"),
        )

    # Vista para poder cerrar la aplicación manualmente
    @app.route("/cerrar", methods=["GET"])
    def cerrar_ventana():
        close_application()

        return "Aplicacion cerrada", 200


def cleanup():
    """Forzar la eliminación de la carpeta temporal antes de salir"""
    if hasattr(sys, "_MEIPASS"):
        temp_dir = sys._MEIPASS
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Carpeta temporal eliminada: {temp_dir}")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {temp_dir}: {e}")


main()

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]

    sock.close()

    # Instanciamos la clase FlaskUI
    # FlaskUI permite generar una ventana de la aplicacion en un navegador embebido (integrado)
    # Abrir la aplicación (Ventana de la aplicación)
    FlaskUI(
        app=app,
        port=port,
        server="flask",
        width=1150,
        height=700,
    ).run()
