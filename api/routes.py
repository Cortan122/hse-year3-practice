from datetime import datetime
from flask import jsonify, request, abort, redirect, render_template
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import Task, User, Company, Project, TaskLog

def get_model(model, id):
    obj = model.query.get(id)
    if not obj:
        abort(404)
    if not current_user.can_access(obj):
        abort(403)
    return obj

api_counter = 0
@app.route("/api/counter")
def ping():
    global api_counter
    api_counter += 1
    return jsonify(api_counter)

@app.route("/api/whoami")
@login_required
def whoami():
    return jsonify(current_user.to_dict())

@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/api/project_tree")
@login_required
def project_tree():
    if current_user.is_admin:
        return jsonify([e.to_tree_node() for e in Company.query.all()])
    else:
        return jsonify([current_user.company.to_tree_node()])

@app.route('/api/project/<int:id>')
@login_required
def project(id):
    return jsonify(get_model(Project, id).to_dict())

@app.route('/api/task/<int:id>/start', methods=["POST"])
@login_required
def start_task(id):
    if current_user.current_task:
        return abort(400)

    task = get_model(Task, id)
    if task.occupied_by:
        return abort(400)

    task.occupied_by = current_user
    db.session.add(TaskLog(task=task, user=current_user, start_time=datetime.now()))
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/stop', methods=["POST"])
@login_required
def stop_task():
    task = current_user.current_task
    if not task:
        return abort(400)

    # todo: set current_log description (and url)
    log = current_user.current_log()
    log.end_time = datetime.now()
    current_user.current_task = None
    db.session.commit()
    return jsonify(task.to_dict())

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

@app.route('/project/<int:id>')
@login_required
def project_index(id):
    if not Project.query.get(id):
        return abort(404)
    return index('')
