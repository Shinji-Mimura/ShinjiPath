from flask import render_template, request, redirect, url_for, make_response, jsonify
from .models import User
from app import app
import jwt, datetime
from functools import wraps

# generate jwt
def generate_jwt(email, role):
    payload = {
        'user_email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
        'role': role
    }
    return jwt.encode(payload, "e04d2d8d0c0ceb9d6de3901cf3b41c8eb4d61461f8eff7bee081b4ff4274f97b", algorithm='HS256')

# middleware default
def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        SessionToken = request.cookies.get('SessionToken')
        try:
            token_decoded = jwt.decode(SessionToken, "e04d2d8d0c0ceb9d6de3901cf3b41c8eb4d61461f8eff7bee081b4ff4274f97b", algorithms=['HS256'])
            if token_decoded['role'] != "employee" and token_decoded['role'] != "admin":
                return jsonify({'message': 'Token inválido!'}), 403
            
        except:
            return jsonify({'message': 'Token inválido!'}), 403
        return f(*args, **kwargs)

    return wrap

# middlweware admin
def check_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        SessionToken = request.cookies.get('SessionToken')
        try:
            token_decoded = jwt.decode(SessionToken, options={"verify_signature": False})
            if token_decoded['role'] != "admin":
                return jsonify({'message': 'Acesso apenas para administradores!'}), 403
        except:
            return jsonify({'message': 'Token inválido!'}), 403
        return f(*args, **kwargs)
    return wrap

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
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(email=username, password=password).first()

        if user is None:
            error = 'Credencias inválidas!'
        else:
            if username == "contato@wicked.com":
                token = generate_jwt(username, "employee")
                response = make_response(redirect("trickpage"))
                response.set_cookie('SessionToken', token)
                return response
        
        return redirect(url_for('login_method', error=error))

# Trick page
@app.route('/trickpage', methods=['GET'])
@check_token
def trickpage():
    return render_template('trickpage.html')

# Dashboard
@app.route('/dashboard', methods=['GET'])
@check_admin
def dashboard():
    return render_template('dashboard.html')