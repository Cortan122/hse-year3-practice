from flask import Flask
from werkzeug.routing import BaseConverter
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../dist',
    template_folder='../dist',
)
app.config.from_prefixed_env()
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

class NoExtentionConverter(BaseConverter):
    regex = r'(?:[a-zA-Z0-9]+)'

app.url_map.converters['ext'] = NoExtentionConverter

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

import routes

if __name__ == '__main__':
    app.run()
