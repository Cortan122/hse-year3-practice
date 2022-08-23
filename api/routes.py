from datetime import datetime
from flask import jsonify, request, abort, redirect, render_template
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_, func, literal_column
from webargs import fields
from webargs.flaskparser import use_args
from app import app, db
from models import Task, User, Company, Project, TaskLog, Client, Tag

def get_model(model, id):
    obj = model.query.get(id)
    if not obj:
        abort(404)
    if not current_user.can_access(obj):
        abort(403)
    return obj

def sortable_table(model, columns=None, filter=None, query=None):
    if columns == None:
        columns = model.__table__.columns
    if filter == None:
        filter = [model.name, model.description]
    if query == None:
        query = model.query

    if not current_user.is_admin:
        return abort(403)

    search = request.args.get('search')
    sort = request.args.get('sort')

    if search:
        query = query.filter(or_(col.ilike(f"%{search}%") for col in filter))
    if sort and sort.isidentifier():
        if sort[0].isupper():
            query = query.order_by(columns[sort.lower()].desc())
        else:
            query = query.order_by(columns[sort])

    return jsonify({
        "filter": {"search": search, "sort": sort},
        "list": [e.to_shallow_dict() for e in query.all()],
    })

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

@app.route("/api/options")
@login_required
def options():
    if not current_user.is_admin:
        return abort(403)

    def id_and_name(e):
        return {"id": e.id, "name": e.name}
    def id_and_full_name(e):
        return {"id": e.id, "name": f"{e.first_name} {e.last_name or ''}"}

    return jsonify({
        "Task": [id_and_name(e) for e in Task.query.all()],
        "User": [id_and_full_name(e) for e in User.query.all()],
        "Company": [id_and_name(e) for e in Company.query.all()],
        "Project": [id_and_name(e) for e in Project.query.all()],
        "Client": [id_and_name(e) for e in Client.query.all()],
        "Tag": [id_and_name(e) for e in Tag.query.all()],
    })

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

@app.route("/api/projects")
@login_required
def projects():
    sub_query = db.session.query(Task.project_id, func.count(Task.id).label('tasks_count')).group_by(Task.project_id).subquery()

    return sortable_table(
        Project,
        filter=[Project.name, Project.description, Client.name, Company.name],
        columns={
            **Project.__table__.columns,
            "client": Client.name,
            "company": Company.name,
            "tasks_count": literal_column('tasks_count'),
        },
        query=Project.query.outerjoin(sub_query, sub_query.c.project_id == Project.id).join(Client).join(Company),
    )

@app.route("/api/users")
@login_required
def users():
    sub_query = db.session.query(TaskLog.user_id, func.count(TaskLog.id).label('tasks_count')).group_by(TaskLog.user_id).subquery()

    return sortable_table(
        User,
        filter=[User.first_name, User.last_name, Company.name, User.email],
        columns={
            **User.__table__.columns,
            "company": Company.name,
            "tasks_count": literal_column('tasks_count'),
        },
        query=User.query.outerjoin(sub_query, sub_query.c.user_id == User.id).outerjoin(Company),
    )

@app.route("/api/users", methods=['POST'])
@login_required
@use_args({
    "first_name": fields.Str(required=True),
    "last_name": fields.Str(),
    "email": fields.Email(required=True),
    "password": fields.Str(required=True),
    "is_admin": fields.Bool(),
    "company_id": fields.Number(),
}, location="form")
def add_user(args):
    if not current_user.is_admin:
        return abort(403)

    if User.query.filter(User.email == args['email']).count():
        return redirect('/users?err=email')

    res = User(**args)
    db.session.add(res)
    db.session.commit()
    return redirect('/users')

@app.route('/api/project/<int:id>')
@login_required
def project(id):
    return jsonify(get_model(Project, id).to_dict())

@app.route('/api/task/<int:id>')
@login_required
def task(id):
    return jsonify(get_model(Task, id).to_dict())

@app.route('/api/task/<int:id>/tags/<tag>', methods=["POST"])
@login_required
def add_tag(id, tag):
    task = get_model(Task, id)
    task.add_tag(tag)
    db.session.commit()
    return jsonify(task.tags_list())

@app.route('/api/task/<int:id>/tags/<tag>', methods=["DELETE"])
@login_required
def remove_tag(id, tag):
    task = get_model(Task, id)
    task.remove_tag(tag)
    db.session.commit()
    return jsonify(task.tags_list())

@app.route('/api/task/<int:id>/tags/<tag>/to/<newtag>', methods=["PATCH"])
@login_required
def change_tag(id, tag, newtag):
    task = get_model(Task, id)
    task.remove_tag(tag)
    task.add_tag(newtag)
    db.session.commit()
    return jsonify(task.tags_list())

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
