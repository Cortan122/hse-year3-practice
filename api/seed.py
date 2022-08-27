#!/usr/bin/env python

from datetime import datetime, timedelta
from app import db
from models import User, Company, Client, Project, Task, Tag, TaskLog

db.create_all()
company = Company(name="Высшая школа экономики")
db.session.add(company)
client = Client(name="Брейман Александр Давидович", company=company)
db.session.add(client)
project = Project(name="Трекер проектов", description="маленькое веб приложение для трекинга работы над проектами", client=client)
db.session.add(project)

admin = User(first_name='admin', email='admin@example.com', password="hello", is_admin=True)
user = User(first_name='Костя', last_name='Борисов', email='knborisov@edu.hse.ru', password="hi", company=company)

task = Task(name="Сделать интерфейс с деревом", description="примерно как в vscode-е", workload=3600_000, project=project, completed=True)
task.add_tag('frontend')
task.add_tag('vuejs')

tl = TaskLog(task=task, user=user, start_time=datetime.now() - timedelta(minutes=30, weeks=4), end_time=datetime.now() - timedelta(weeks=4))
tl._duration = tl.duration()
task.history.append(tl)

tl = TaskLog(task=task, user=admin, start_time=datetime.now() - timedelta(minutes=30), end_time=datetime.now())
tl._duration = tl.duration()
task.history.append(tl)
db.session.add(task)

task = Task(name="Прикрутить таймер", description="чтобы обновлялся каждую секунду и давил на нервы", workload=500_000, project=project)
task.add_tag('frontend')
task.add_tag('js')
db.session.add(task)

task = Task(name="Сделать главную страницу", description="с описанием того, про что сайт", workload=1000_000, project=project)
task.add_tag('frontend')
task.add_tag('design')
db.session.add(task)

client = Client(name="Самоненко Илья Юрьевич", company=company)
db.session.add(client)
project = Project(name="Parser Visualizer", description="win32 приложение для визуализации метода рекурсивного спуска", client=client)
db.session.add(project)

client = Client(name="Шадрин Михаил Дмитриевич", company=company)
db.session.add(client)
project = Project(name="Screenshot Editor", description="кроссплатформенное десктоп приложение для редактирования скриншотов", client=client)
db.session.add(project)

client = Client(name="Каширина Ольга Александровна", company=company)
db.session.add(client)
project = Project(name="Discount Delivery", description="мобильный агрегатор доставки из магазинов", client=client)
db.session.add(project)

company2 = Company(name="University of Groningen")
db.session.add(company2)
client = Client(name="Andrea Capiluppi", company=company2)
db.session.add(client)
project = Project(name="University-Industry Collaboration", description="a collaborative platform for industries and students", client=client)
db.session.add(project)

task = Task(name="Fix email notifications", description="you have to do a lot of things. you see, there's a problem. due to a configuration error, everyone subscribed to update notification will receive emails all 5 days before the deadline, rather then just once", project=project)
task.add_tag('backend')
task.add_tag('php')
db.session.add(task)

db.session.add(admin)
db.session.add(user)
db.session.add(User(first_name='Kostya', last_name='Borisov', email='k.borisov@student.rug.nl', password="hi", company=company2))
db.session.commit()
