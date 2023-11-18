from flask import (
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    jsonify,
    send_from_directory,
)
from .models import User
from app import app
import jwt, datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os
from lxml import etree
import cgi


# generate jwt
def generate_jwt(email, role):
    payload = {
        "user_email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
        "flag": "TAC_2023{3a4b5c6d7e8f9a0b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5}",
        "role": role,
    }
    return jwt.encode(
        payload,
        "e04d2d8d0c0ceb9d6de3901cf3b41c8eb4d61461f8eff7bee081b4ff4274f97b",
        algorithm="HS256",
    )


# middleware default
def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        SessionToken = request.cookies.get("SessionToken")
        try:
            token_decoded = jwt.decode(
                SessionToken,
                "e04d2d8d0c0ceb9d6de3901cf3b41c8eb4d61461f8eff7bee081b4ff4274f97b",
                algorithms=["HS256"],
            )
            if token_decoded["role"] != "employee" and token_decoded["role"] != "admin":
                return jsonify({"message": "Token inválido!"}), 403

        except:
            return jsonify({"message": "Token inválido!"}), 403
        return f(*args, **kwargs)

    return wrap


# middlweware admin
def check_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        SessionToken = request.cookies.get("SessionToken")
        try:
            token_decoded = jwt.decode(
                SessionToken, options={"verify_signature": False}
            )
            if token_decoded["role"] != "admin":
                return jsonify({"message": "Acesso apenas para administradores!"}), 403
        except:
            return jsonify({"message": "Token inválido!"}), 403
        return f(*args, **kwargs)

    return wrap


# Index page
@app.route("/")
def index():
    return render_template("index.html")


# Login process
@app.route("/login", methods=["GET", "POST"])
def login_method():
    if request.method == "GET":
        error = request.args.get("error")
        return render_template("login.html", error=error)

    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(email=username, password=password).first()

        if user is None:
            error = "Credencias inválidas!"
        else:
            if username == "contato@wicked.com":
                token = generate_jwt(username, "employee")
                response = make_response(redirect("trickpage"))
                response.set_cookie("SessionToken", token)
                return response

        return redirect(url_for("login_method", error=error))

# Trick page
@app.route("/trickpage", methods=["GET"])
@check_token
def trickpage():
    return render_template("trickpage.html")


# Dashboard
@app.route("/dashboard", methods=["GET"])
# @check_admin
def dashboard():
    return render_template("dashboard.html")


# upload XML file route
@app.route("/upload", methods=["POST"])
# check_admin
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'xmlfile' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado!"}), 400

    xmlfile = request.files['xmlfile']
    if xmlfile.filename == '':
        return jsonify({"message": "Nenhum arquivo enviado!"}), 400

    try:
        # Configuração vulnerável: permite a resolução de entidades externas
        parser = etree.XMLParser(load_dtd=True, no_network=False, resolve_entities=True)
        doc = etree.parse(xmlfile.stream, parser)
        parsed_xml = etree.tostring(doc, pretty_print=True).decode()
    except etree.XMLSyntaxError as e:
        return jsonify({"message": "Erro ao processar XML: " + str(e)}), 400

    return jsonify({"message": "XML processado com sucesso!", "xml": parsed_xml}), 200

# download XML file route
@app.route("/download-template", methods=["GET"])
# @check_admin
def download():
    return send_from_directory("static/template_xml", "template.xml", as_attachment=True)
