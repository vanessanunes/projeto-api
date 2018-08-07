from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os.path
# import logging
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# filename=os.path.join(basedir, 'logs.txt')
# logger = logging.basicConfig(filename=filename, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


db = SQLAlchemy(app)
from app.agenda.views import app

db.create_all()
