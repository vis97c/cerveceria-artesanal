from flask import Flask, render_template

from utils.db import conectar

# INIT APP
app = Flask(__name__)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')