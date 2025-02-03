import os
from flask import Flask, request, render_template, jsonify, redirect, session

# INIT APP
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ROUTES
@app.route('/')
def index():
    if session.get('logged_in'): return redirect('/admin')

    return render_template('index.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'): return redirect('/')

    return render_template('admin.html')

sampleEmail = "example@example.com"
samplePassword = "insecure_password"

# REST API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid payload. Email and password are required."}), 400

    email = data['email']
    password = data['password']

    # TODO: Do a proper validation
    if email == sampleEmail and password == samplePassword:
        session['logged_in'] = True
        return jsonify({"data": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"data": None, "error": "Invalid email or password."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()

    return jsonify({"data": True, "message": "Logged out successfully!"}), 200