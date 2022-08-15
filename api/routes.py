from flask import jsonify, request, abort, redirect, render_template
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import User

api_counter = 0
@app.route("/api/counter")
def ping():
    global api_counter
    api_counter += 1
    return jsonify(api_counter)

@app.route("/api/whoami")
@login_required
def whoami():
    return jsonify(current_user.email)

@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/api/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember', 'off') == 'on'

    if type(email) != str or type(password) != str:
        print([type(email), email, type(password), password])
        return abort(400)

    user = User.query.filter(User.email == email).first()
    if not user:
        return redirect('/login?err=user')
    if not check_password_hash(user.password, password):
        return redirect('/login?err=pass')
    login_user(user, remember=remember)

    return redirect('/home')

@app.route('/', defaults={'path': ''})
@app.route('/<ext:path>')
def index(path):
    user = current_user.__html__() if current_user.is_authenticated else "{}"
    return render_template('index.html', user=user)
