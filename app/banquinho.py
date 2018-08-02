# from app import db
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_TRACK_MODIFICATIONS = True
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' #editar aqui

db = SQLAlchemy(app)

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    nome_sala = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Sala %r>' % self.nome_sala

class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    id_locatario = db.Column(db.Integer, db.ForeignKey('locatario.id'), nullable=False)
    horario = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # category = db.relationship('Sala', backref=db.backref('posts', lazy=True))

    # sala = db.relationship('Sala', foreign_keys=sala_id)
    # locatario = db.relationship('Locatario', foreign_keys=loca_id)

    def __repr__(self):
        return '<Agendamento %r>' % self.nome_sala

class Locatario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Locatario %r>' % self.nome



### não fiz completo pq falta o banco, fazer postgres :(
