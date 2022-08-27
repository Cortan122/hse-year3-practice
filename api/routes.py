from collections import OrderedDict, defaultdict
from datetime import datetime
from flask import jsonify, request, abort, redirect, render_template
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import or_, func, literal_column
from webargs import fields
from webargs.flaskparser import use_args
from app import app, db
from models import Task, User, Company, Project, TaskLog, Client, Tag, task_tags

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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

def stats(user=False, tags=False, project=False, client=False):
    # month = func.month(TaskLog.start_time) on postgres
    month = func.strftime('%m', TaskLog.start_time)

    cols = [month]
    if user:
        cols += [User.id, User.first_name, User.last_name]
    if tags:
        cols += [Tag.name]
    if project:
        cols += [Project.name, Project.id]
    if client:
        cols += [Client.name, Client.id]

    res = db.session.query(*cols, func.sum(TaskLog._duration)) \
        .join(User).join(Task, TaskLog.task_id == Task.id).join(Project).join(Client).join(Company)
    if tags:
        res = res.outerjoin(task_tags).outerjoin(Tag)

    if isinstance(user, User):
        res = res.filter(User.id == user.id)

    if not current_user.is_admin:
        res = res.filter(Company.id == current_user.company_id)

    res = res.group_by(*cols).all()
    names = ['month', *[c.table.name + '_' + c.name for c in cols[1:]], 'total']

    return [{names[i]: v for i, v in enumerate(row)} for row in res]

def datasets(stats, namefunc=None, title=None):
    if namefunc == None:
        namefunc = lambda row: f"{row['user_first_name']} {row['user_last_name'] or ''}"
    if type(namefunc) == str:
        old_namefunc = namefunc
        namefunc = lambda row: row[old_namefunc]

    users = defaultdict(lambda: [0]*12)

    for row in stats:
        username = namefunc(row)
        month = int(row['month']) - 1
        users[username][month] += row['total'] / 3600_000

    return {
        "type": "line",
        "labels": MONTHS,
        "title": title,
        "datasets": [{"label": k, "data": u} for k, u in users.items()],
    }

def pie_dataset(stats, namefunc=None, title=None):
    if namefunc == None:
        namefunc = lambda row: f"{row['user_first_name']} {row['user_last_name'] or ''}"
    if type(namefunc) == str:
        old_namefunc = namefunc
        namefunc = lambda row: row[old_namefunc]

    labels = OrderedDict()
    total = 0

    for row in stats:
        val = row['total'] / 3600_000
        total += val
        labels.setdefault(namefunc(row), [0])[0] += val

    return {
        "type": "pie",
        "labels": list(labels.keys()),
        "title": title,
        "datasets": [{"label": 'Dataset 1', "data": [
            e[0]/total*100 for e in labels.values()
        ]}],
    }

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

@app.route("/api/stats_tree")
@login_required
def stats_tree():
    if current_user.is_admin:
        users = User.query.all()
    else:
        users = User.query.filter_by(company_id=current_user.company_id).all()

    return jsonify([
        {"label": "Общая статистика", "id": "/stats"},
        {"label": "Статистика отдельных пользователей", "id": "/users", "children": [
            {"label": u.name(), "id": f"/stats/users/{u.id}"} for u in users
        ]},
    ])

@app.route("/api/stats")
@login_required
def statistics():
    return jsonify([
        datasets(stats(user=True), title='Активность пользователей'),
        datasets(stats(tags=True), namefunc='tag_name', title='Активность тегов'),
        datasets(stats(project=True), namefunc='project_name', title='Активность проектов'),
        datasets(stats(client=True), namefunc='client_name', title='Активность клиентов'),
    ])

@app.route("/api/stats/users/<int:id>")
@login_required
def user_stats(id):
    user = get_model(User, id)

    return jsonify({
        "name": user.name(),
        "list": [
            pie_dataset(stats(user=user, tags=True), namefunc='tag_name', title='Распределение тегов'),
            datasets(stats(user=user, tags=True), namefunc='tag_name'),
            pie_dataset(stats(user=user, project=True), namefunc='project_name', title='Распределение проектов'),
            datasets(stats(user=user, project=True), namefunc='project_name'),
            pie_dataset(stats(user=user, client=True), namefunc='client_name', title='Распределение клиентов'),
            datasets(stats(user=user, client=True), namefunc='client_name'),
        ]
    })

@app.route("/api/companies")
@login_required
def companies():
    sub_query1 = db.session.query(Client.company_id, func.count(Client.id).label('clients_count')).group_by(Client.company_id).subquery()
    sub_query2 = db.session.query(User.company_id, func.count(User.id).label('users_count')).group_by(User.company_id).subquery()
    sub_query3 = db.session.query(Client.company_id, func.count(Project.id).label('projects_count')) \
        .join(Project).group_by(Client.company_id).subquery()

    return sortable_table(
        Company,
        filter=[Company.name],
        columns={
            **Company.__table__.columns,
            "clients_count": literal_column('clients_count'),
            "users_count": literal_column('users_count'),
            "projects_count": literal_column('projects_count'),
        },
        query=Company.query
            .outerjoin(sub_query1, sub_query1.c.company_id == Company.id)
            .outerjoin(sub_query2, sub_query2.c.company_id == Company.id)
            .outerjoin(sub_query3, sub_query3.c.company_id == Company.id),
    )

@app.route("/api/companies", methods=['POST'])
@login_required
@use_args({
    "name": fields.String(required=True),
}, location="form")
def add_company(args):
    if not current_user.is_admin:
        return abort(403)

    db.session.add(Company(**args))
    db.session.commit()
    return redirect('/companies')

@app.route("/api/clients")
@login_required
def clients():
    sub_query = db.session.query(Project.client_id, func.count(Project.id).label('projects_count')).group_by(Project.client_id).subquery()

    return sortable_table(
        Client,
        filter=[Client.name, Company.name],
        columns={
            **Client.__table__.columns,
            "company": Company.name,
            "projects_count": literal_column('projects_count'),
        },
        query=Client.query.outerjoin(sub_query, sub_query.c.client_id == Client.id).join(Company),
    )

@app.route("/api/clients", methods=['POST'])
@login_required
@use_args({
    "name": fields.String(required=True),
    "company_id": fields.Integer(required=True),
}, location="form")
def add_client(args):
    if not current_user.is_admin:
        return abort(403)

    db.session.add(Client(**args))
    db.session.commit()
    return redirect('/clients')

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

@app.route("/api/projects", methods=['POST'])
@login_required
@use_args({
    "name": fields.String(required=True),
    "description": fields.String(),
    "client_id": fields.Integer(required=True),
}, location="form")
def add_project(args):
    if not current_user.is_admin:
        return abort(403)

    db.session.add(Project(**args))
    db.session.commit()
    return redirect('/projects')

@app.route("/api/tasks")
@login_required
def tasks():
    sub_query1 = db.session.query(TaskLog.task_id, func.count(TaskLog.id).label('tasks_count')).group_by(TaskLog.task_id).subquery()
    sub_query2 = db.session.query(task_tags.c.task_id, func.count(task_tags.c.tag_id).label('tags_count')) \
        .group_by(task_tags.c.task_id).subquery()

    return sortable_table(
        Task,
        filter=[Task.name, Task.description, Client.name],
        columns={
            **Task.__table__.columns,
            "project": Project.name,
            "tasks_count": literal_column('tasks_count'),
            "tags_count": literal_column('tags_count'),
        },
        query=Task.query
            .outerjoin(sub_query1, sub_query1.c.task_id == Task.id)
            .outerjoin(sub_query2, sub_query2.c.task_id == Task.id).join(Project),
    )

@app.route("/api/tasks", methods=['POST'])
@login_required
@use_args({
    "name": fields.String(required=True),
    "description": fields.String(),
    "workload": fields.Float(),
    "tags": fields.DelimitedList(fields.String()),
    "project_id": fields.Integer(required=True),
}, location="form")
def add_task(args):
    if not current_user.is_admin:
        return abort(403)

    tags = []
    if 'tags' in args:
        tags = args['tags']
        del args['tags']

    task = Task(**args)
    for tag in tags:
        task.add_tag(tag)

    db.session.add(task)
    db.session.commit()
    return redirect('/tasks')

@app.route("/api/tags")
@login_required
def tags():
    sub_query = db.session.query(task_tags.c.tag_id, func.count(task_tags.c.task_id).label('tags_count')) \
        .group_by(task_tags.c.tag_id).subquery()

    return sortable_table(
        Tag,
        filter=[Tag.name],
        columns={
            **Tag.__table__.columns,
            "tags_count": literal_column('tags_count'),
        },
        query=Tag.query.outerjoin(sub_query, sub_query.c.tag_id == Tag.id),
    )

@app.route("/api/tags/<int:id>", methods=['DELETE'])
@login_required
def delete_tag(id):
    if not current_user.is_admin:
        return abort(403)

    res = Tag.query.get(id)
    Tag.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(res.to_dict())

@app.route("/api/tags", methods=['POST'])
@login_required
@use_args({
    "old_name": fields.String(required=True),
    "name": fields.String(required=True),
}, location="form")
def rename_tag(args):
    if not current_user.is_admin:
        return abort(403)

    if Tag.query.filter_by(name=args['name']).count():
        return redirect('/tags?err=name')

    res = Tag.query.filter_by(name=args['old_name']).first()
    res.name = args['name']
    db.session.commit()
    return redirect('/tags')

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
    "first_name": fields.String(required=True),
    "last_name": fields.String(),
    "email": fields.Email(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(),
    "company_id": fields.Integer(),
}, location="form")
def add_user(args):
    if not current_user.is_admin:
        return abort(403)

    if User.query.filter(User.email == args['email']).count():
        return redirect('/users?err=email')

    db.session.add(User(**args))
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

    log = current_user.current_log()
    log.end_time = datetime.now()
    log._duration = log.duration()
    current_user.current_task = None
    db.session.commit()
    return jsonify(log.to_dict())

@app.route('/api/finalize/<int:id>', methods=["POST"])
@login_required
@use_args({
    "github_url": fields.String(),
    "description": fields.String(),
    "is_completed": fields.Boolean(),
}, location="form")
def finalize_task(args, id):
    log = TaskLog.query.get(id)
    if log.user_id != current_user.id:
        return abort(403)

    if args.get('description'):
        log.description = args['description']
    if args.get('github_url'):
        log.github_url = args['github_url']
    if args.get('is_completed'):
        log.task.completed = True
        log.task.workload = sum(e.duration() for e in log.task.history)

    db.session.commit()
    return redirect(f'/project/{log.task.project.id}')

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

@app.route('/stats/users/<int:id>')
@login_required
def user_stats_index(id):
    if not User.query.get(id):
        return abort(404)
    return index('')
