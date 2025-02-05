from flask import Flask, render_template

from utils.db import conectar

# INIT APP
app = Flask(__name__)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')