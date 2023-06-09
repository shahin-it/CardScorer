from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_migrate import Migrate

from app.config import Config, app_config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='', static_folder='../web/static', template_folder='../web/templates')
app.config.from_object(Config)

db = SQLAlchemy(app)
from app import routes, models

migrate = Migrate(app, db)
Bootstrap5(app)

with app.app_context():
    db.create_all()
    # Migrate(app, db)


@app.context_processor
def custom_context():
    return dict(_cfg=app_config)


@app.template_filter()
def str_date(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime('%b %d, %Y')


@app.template_filter()
def str_time(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime('%I:%M:%S %p')


@app.template_filter()
def str_date_time(date, fmt=None):
    native = date.replace(tzinfo=None)
    return native.strftime('%b %d, %I:%M:%S %p')
