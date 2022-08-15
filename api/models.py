import json
from sqlalchemy.sql import func, expression
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    _password = db.Column(db.String(255), nullable=False)

    @hybrid_property
    def password(self):
        """Return the hashed user password."""
        return self._password

    @password.setter
    def password(self, new_pass):
        """Salt/Hash and save the user's new password."""
        new_password_hash = generate_password_hash(new_pass)
        self._password = new_password_hash

    def __html__(self):
        return json.dumps({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
