from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from app import app, db
from app.agenda.models import Locatario

# aqui deve ter as rotas

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('nome')

# PESSOAS = {} # este foi OK

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
        # PESSOAS[nome] = nome
        new = Locatario(nome)
        print("Nome: {}, locatario: {}".format(nome, new))
        # db.session.add(new)
        # db.session.commit()


class Listar(Resource):
    def get(self):
        # qnt_registro = db.session.query(Locatario.id).count()
        lista = Locatario.query.order_by(Locatario.nome).all()
        pessoas = {}
        for i in lista:
            pessoas['pessoa{}'.format(i.id)] = {'id':i.id, 'nome':i.nome}
        return pessoas

api.add_resource(HelloWorld, '/')
api.add_resource(NovoLocatario, '/locatario/<string:nome>')
api.add_resource(Listar, '/listar')
