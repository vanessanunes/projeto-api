from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DEBUG = True
SECRET_KEY = 'um-nome-seguro'

db = SQLAlchemy(app)

from app.agenda.views import app

db.create_all()