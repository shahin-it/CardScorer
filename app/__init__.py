from flask import Flask
from flask_bootstrap5 import Bootstrap

from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='', static_folder='../web/static', template_folder='../web/templates')
app.config.from_object(Config)

db = SQLAlchemy(app)
Bootstrap(app)
from app import routes, models

with app.app_context():
    db.create_all()
    # Migrate(app, db)
