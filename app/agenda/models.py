from app import db
from datetime import datetime

class Sala(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    nome_sala = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, numero, nome_sala):
        self.numero = numero
        self.nome_sala = nome_sala

    def __repr__(self):
        return '<Sala %d>' % self.id

class Agendamento(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    id_locatario = db.Column(db.Integer, db.ForeignKey('locatario.id'), nullable=False)
    horario_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    horario_fim = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, id_sala, id_locatario, horario_inicio, horario_fim):
        self.id_sala = id_sala
        self.id_locatario = id_locatario
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim


    def __repr__(self):
        return '<Agendamento %d>' % self.id

class Locatario(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return '<Locatario %r>' % (self.nome)


