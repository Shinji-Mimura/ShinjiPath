from flask import render_template, request, redirect, url_for
from .models import User
from app import app
from .middleware import middleware

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Login process
@app.route('/login', methods=['GET', 'POST'])
def login_method():
    if request.method == 'GET':
        error = request.args.get('error')
        return render_template('login.html', error=error)

    error = None
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            error = 'Invalid credentials. Please try again.'
        else:
            return redirect(url_for('trickpage'))
        
        return redirect(url_for('login_method', error=error))
