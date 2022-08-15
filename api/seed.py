#!/usr/bin/env python

from app import db
from models import User

db.create_all()
admin = User(first_name='admin', email='admin@example.com', password="hello", is_admin=True)
guest = User(first_name='user', email='user@example.com', password="hi")
db.session.add(admin)
db.session.add(guest)
db.session.commit()
