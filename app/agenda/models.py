from app import db
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    nome_sala = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, numero, nome_sala):
        self.numero = numero
        self.nome_sala = nome_sala

    def __repr__(self):
        return '<Sala %d>' % self.id

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    id_locatario = db.Column(db.Integer, db.ForeignKey('locatario.id'), nullable=False)
    horario = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # data = db.Column(db.String, nullable=False, default=datetime.utcnow)

    def __init__(self, id_sala, id_locatario, horario):
        self.id_sala = id_sala
        self.id_locatario = id_locatario
        self.horario = horario

    # category = db.relationship('Sala', backref=db.backref('posts', lazy=True))
    # sala = db.relationship('Sala', foreign_keys=sala_id)
    # locatario = db.relationship('Locatario', foreign_keys=loca_id)

    def __repr__(self):
        return '<Agendamento %d>' % self.id_sala

class Locatario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(120), nullable=False)

        def __init__(self, nome):
            self.nome = nome

        def __repr__(self):
            return '<Locatario %r>' % (self.nome)

class LocatarioSchema(ModelSchema):
    class Meta:
        model = Locatario

