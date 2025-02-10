# CERVECERÍA ARTESANAL
# Este es el archivo principal de nuestra aplicación
# La lógica de los módulos se divide en los archivos de la ruta "/modules" pera luego ser importados aca

from flask import Flask, render_template, request, redirect
from datetime import datetime
import pdfkit

# Pdfkit requiere wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf="./wkhtmltopdf/bin/wkhtmltopdf.exe")

# Para minimizar el codigo en este archivo separamos la logica por modulos
from modules.db import conectar
from modules.productos import productos
from modules.clientes import clientes
from modules.ventas import ventas
from modules.correo import enviarCorreo

# INICIALIZAMOS FLASK
# Flask es un framework/librería que nos permite generar un servidor web con python
# Los usuarios interactuaran con la aplicación desde su navegador
# SQlite3 se abre y cierra por cada request para evitar errores debido al multithreading de flask
app = Flask(__name__, static_url_path="/")


# Función principal de la aplicación donde definimos las rutas y vistas.
def main():
    # RUTAS PRINCIPALES
    # Separamos los módulos de nuestra aplicación en rutas que pueden ser accedidas desde el navegador
    # Ej: http://localhost:5000

    # Ruta del menu de la página de inicio.
    @app.route("/")
    def index():
        return render_template("index.html")

    # GESTIÓN DE PRODUCTOS

    # Vista de gestión de productos
    @app.route("/productos")
    def productos_vista():
        return render_template("productos/index.html")

    # Vista para crear un nuevo producto
    @app.route("/productos/crear", methods=["GET", "POST"])
    def crear_producto():
        error = None
        success = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                # Obtener datos del formulario enviados por el usuario.
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

                # Crear el producto con todos los valores en la base de datos.
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

            cerrar()  # Cerrar la conexión con la base de datos

        return render_template("productos/crear.html", error=error, success=success)

    # Vista para actualizar el nombre de un producto existente
    @app.route("/productos/actualizar", methods=["GET", "POST"])
    def actualizar_producto():
        error = None
        success = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                # Obtener datos del formulario
                productId = int(request.form.get("id"))
                nuevoNombre = request.form.get("nombre")

                # Actualizar nombre del producto
                moduloProductos["actualizarNombre"](productId, nuevoNombre)
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
            correr, cerrar = conectar()
            moduloProductos = productos(correr)

            try:
                # Obtener datos del formulario
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

    # GESTIÓN DE CLIENTES

    # Vista de gestión de clientes
    @app.route("/clientes")
    def clientes_vista():
        return render_template("clientes/index.html")

    # Vista para crear un nuevo cliente
    @app.route("/clientes/crear", methods=["GET", "POST"])
    def crear_cliente():
        error = None
        success = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloClientes = clientes(correr)

            try:
                # Obtener datos del formulario
                clienteId = request.form.get("id")
                nombre = request.form.get("nombre")
                apellido = request.form.get("apellido")
                direccion = request.form.get("direccion")
                telefono = request.form.get("telefono")
                email = request.form.get("email")

                # Crear el cliente con todos los valores
                moduloClientes["crear"](
                    (clienteId, nombre, apellido, direccion, telefono, email)
                )
                success = f'Cliente con el id "{clienteId}" fue creado exitosamente'

            except Exception as err:
                print(f"Error al crear cliente: {err}")

                if "UNIQUE constraint failed" in str(err):
                    error = "Ya existe un cliente con ese ID"
                else:
                    error = "Error al crear el cliente"

            cerrar()  # Cerrar la conexión

        return render_template("clientes/crear.html", error=error, success=success)

    # Vista para actualizar la direccion de un cliente existente
    @app.route("/clientes/actualizar", methods=["GET", "POST"])
    def actualizar_cliente():
        error = None
        success = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloClientes = clientes(correr)

            try:
                # Obtener datos del formulario
                clienteId = request.form.get("id")
                nuevaDireccion = request.form.get("direccion")

                # Actualizar direccion del cliente
                moduloClientes["actualizarDireccion"](clienteId, nuevaDireccion)
                success = f'Dirección del cliente con id "{clienteId}" actualizada exitosamente'

            except Exception as err:
                print(f"Error al actualizar dirección: {err}")
                if str(err) == "NO_EXISTE":
                    error = "No existe un cliente con ese ID"
                else:
                    error = "Error al actualizar la dirección"

            cerrar()  # Cerrar la conexión

        return render_template("clientes/actualizar.html", error=error, success=success)

    # Vista para consultar un cliente existente
    @app.route("/clientes/consultar", methods=["GET", "POST"])
    def consultar_cliente():
        cliente = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloClientes = clientes(correr)

            try:
                clienteId = request.form.get("id")
                # Obtener cliente con el id
                resultado = moduloClientes["consultarUno"](clienteId)

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
                cliente = False  # Tambien indicamos que no existe si hay error

            cerrar()  # Cerrar la conexión

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
            correr, cerrar = conectar()
            moduloVentas = ventas(correr)

            try:
                # Obtener datos del formulario
                clienteId = request.form.get("clienteId")
                productoId = request.form.get("productoId")
                cantidad = int(request.form.get("cantidad"))
                factura = request.form.get("factura")

                # Generar ID de venta
                ventaId = f"{factura}_{productoId}"

                # Crear la venta
                moduloVentas["crear"](
                    (ventaId, factura, clienteId, productoId, cantidad)
                )
                success = f"Venta con id {ventaId} creada exitosamente"

            except Exception as err:
                print(f"Error al crear venta: {err}")
                if "UNIQUE constraint failed" in str(err):
                    error = "Ya existe una venta con ese ID"
                else:
                    error = "Error al crear la venta"

            cerrar()  # Cerrar la conexión

        return render_template("ventas/crear.html", error=error, success=success)

    # Vista para borrar una venta existente
    @app.route("/ventas/borrar", methods=["GET", "POST"])
    def borrar_venta():
        error = None
        success = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloVentas = ventas(correr)

            try:
                # Obtener datos del formulario
                factura = request.form.get("factura")
                producto = request.form.get("producto")

                # Borrar la venta
                moduloVentas["borrar"](factura, producto)
                success = f"Venta de producto {producto} en factura {factura} eliminada exitosamente"

            except Exception as err:
                print(f"Error al borrar venta: {err}")
                error = "Error al borrar la venta"

            cerrar()  # Cerrar la conexión

        return render_template("ventas/borrar.html", error=error, success=success)

    # FACTURACIÓN

    # Vista de facturación
    @app.route("/facturacion", methods=["GET", "POST"])
    def facturacion_vista():
        factura = None

        if request.method == "POST":
            correr, cerrar = conectar()
            moduloVentas = ventas(correr)

            # Obtener datos del formulario
            facturaId = request.form.get("id")

            if facturaId:
                # Obtener factura con el id
                resultado = moduloVentas["consultarVarias"](facturaId)

                cerrar()  # Cerrar la conexión

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
        correr, cerrar = conectar()
        moduloVentas = ventas(correr)
        moduloClientes = clientes(correr)
        moduloProductos = productos(correr)

        try:
            # Obtener factura con el id
            resultado = moduloVentas["consultarVarias"](facturaId)

            if request.args.get("pdfkit"):
                pdf = True

            if resultado and len(resultado) > 0:
                clienteId = resultado[0][2]
                cliente = moduloClientes["consultarUno"](clienteId)
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
                    producto = moduloProductos["consultarUno"](productoId)
                    precio = producto[6]

                    # Listar productos
                    factura["productos"].append(
                        {
                            "idProducto": productoId,
                            "cantidad": cantidad,
                            # Informacion adicional del producto
                            "nombre": producto[1],
                            "peso": producto[2],
                            "volumen": producto[3],
                            "vencimiento": producto[4],
                            "produccion": producto[5],
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
            factura = False  # Tambien indicamos que no existe si hay error

        cerrar()  # Cerrar la conexión

        return render_template(
            "facturacion/factura.html",
            factura=factura,
            correo=correo,
            pdf=pdf,
            fecha=datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S"),
        )


main()
