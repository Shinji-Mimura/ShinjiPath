from flask import render_template, request, redirect, url_for
from app import app
from middleware import middleware

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('trickpage'))
    return render_template('login.html', error=error)

# Dashboard page (Admin)
@app.route('/dashboard')
@middleware
def dashboard():
    return render_template('dashboard.html')