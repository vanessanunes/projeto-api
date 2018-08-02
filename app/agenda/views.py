from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.agenda.models import Locatario

# aqui deve ter as rotas

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('nome')

PESSOAS = {}

class HelloWorld(Resource):
    # tá ok
    def get(self):
        return {'hello': 'world'}

class NovoLocatario(Resource):
    # def get(self):
    #     res = {}
    #     locatarios = Locatario.query.filter_by(id=id)
    #     for locatario in locatarios:
    #         res[locatario.id] = {
    #             'nome': locatario.nome,
    #         }
    #
    #     return id

    def put(self, nome):
        # PESSOAS['nome'] = nome
        new = Locatario(nome=nome)
        db.session.add(new)
        db.session.commit()


class Listar(Resource):
    def get(self):
        # lista = Locatario.query.order_by(Locatario.id).all()
        return PESSOAS

api.add_resource(HelloWorld, '/')
api.add_resource(NovoLocatario, '/locatario/<string:nome>')
api.add_resource(Listar, '/listar')
