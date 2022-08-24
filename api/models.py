from datetime import datetime
import json
from sqlalchemy.sql import func, expression
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
from app import db

task_tags = db.Table('task_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class TimestampMixin:
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)

class Company(TimestampMixin, db.Model):
    name = db.Column(db.String(255), nullable=False)
    employees = db.relationship('User', backref='company', lazy=True)
    clients = db.relationship('Client', backref='company', lazy=True)

    def to_tree_node(self):
        return {
            "label": self.name,
            "id": f"/{self.__class__.__name__.lower()}/{self.id}",
            "children": [e.to_tree_node() for e in self.clients],
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "users_count": len(self.employees),
            "clients_count": len(self.clients),
            "projects_count": sum(len(e.projects) for e in self.clients),
        }

class Client(TimestampMixin, db.Model):
    name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    projects = db.relationship('Project', backref='client', lazy=True)

    def to_tree_node(self):
        return {
            "label": self.name,
            "id": f"/{self.__class__.__name__.lower()}/{self.id}",
            "children": [e.to_tree_node() for e in self.projects],
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company.name,
            "created_at": self.created_at,
            "projects_count": len(self.projects),
        }

class Project(TimestampMixin, db.Model):
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

    def to_tree_node(self):
        return {
            "label": self.name,
            "id": f"/{self.__class__.__name__.lower()}/{self.id}",
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tasks": sorted([e.to_dict() for e in self.tasks], key=lambda x: x['completed']),
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "client": self.client.name,
            "company": self.client.company.name,
            "created_at": self.created_at,
            "tasks_count": len(self.tasks),
        }

class Task(TimestampMixin, db.Model):
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    workload = db.Column(db.Float, nullable=True) # in milliseconds
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    tags = db.relationship('Tag', secondary=task_tags, lazy='subquery', backref=db.backref('task', lazy=True))
    history = db.relationship('TaskLog', backref='task', lazy=True)
    occupied_by = db.relationship('User', backref='current_task', lazy=True, uselist=False)
    completed = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    def tags_list(self):
        return [e.to_dict() for e in self.tags]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "workload": self.workload or 3600_000,
            "tags": self.tags_list(),
            "history": [e.to_dict() for e in self.history],
            "occupied_by": self.occupied_by.to_dict() if self.occupied_by else None,
            "completed": self.completed,
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id,
            "project": self.project.name,
            "created_at": self.created_at,
            "tasks_count": len(self.history),
            "completed": self.completed,
            "tags": self.tags_list(),
        }

    def add_tag(self, tag: str):
        res = Tag.query.filter(Tag.name == tag).first()
        if res in self.tags:
            return
        self.tags.append(res if res else Tag(name=tag))

    def remove_tag(self, tag: str):
        res = Tag.query.filter(Tag.name == tag).first()
        if res in self.tags:
            self.tags.remove(res)

class Tag(TimestampMixin, db.Model):
    name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "tags_count": len(self.task),
        }

class TaskLog(TimestampMixin, db.Model):
    description = db.Column(db.Text, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=True)

    def finished(self):
        return self.end_time != None

    def duration(self):
        end = datetime.now()
        if self.finished():
            end = self.end_time

        return int((end - self.start_time).total_seconds() * 1000)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "user": self.user.to_dict(),
            "finished": self.finished(),
            "duration": self.duration(),
            "start_date": self.start_time,
        }

class User(TimestampMixin, UserMixin, db.Model):
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    _password = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True, unique=True)
    history = db.relationship('TaskLog', backref='user', lazy=True)

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self._password

    @password.setter
    def password(self, new_pass):
        """Salt/Hash and save the user's new password."""
        new_password_hash = generate_password_hash(new_pass)
        self._password = new_password_hash

    def current_log(self):
        # todo: race condition?
        return self.history[-1] if self.current_task else None

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "has_current_task": self.current_task != None,
            "timer": self.current_log().duration() if self.current_task else None,
        }

    def to_shallow_dict(self):
        return {
            "id": self.id,
            "name": f"{self.first_name} {self.last_name or ''}",
            "email": self.email,
            "is_admin": self.is_admin,
            "has_current_task": self.current_task != None,
            "company": self.company.name if self.company else None,
            "created_at": self.created_at,
            "tasks_count": len(self.history),
        }

    def __html__(self):
        return json.dumps(self.to_dict())

    def can_access(self, obj):
        if self.is_admin:
            return True
        if isinstance(obj, Task):
            obj = obj.project
        if isinstance(obj, Project):
            obj = obj.client
        if isinstance(obj, Client):
            obj = obj.company
        if isinstance(obj, Company):
            return self.company_id == obj.id
        return False
