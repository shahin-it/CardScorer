import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parents[1]


class Config(object):
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app_config = {
    'app_name': 'Card Scorer',
    'datetime': datetime.today(),
};