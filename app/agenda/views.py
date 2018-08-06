from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from app import app, db
from app.agenda.models import Locatario, Sala, Agendamento

# aqui deve ter as rotas

api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('nome')

# PESSOAS = {} # este foi OK

class HelloWorld(Resource):
    # tá ok
    def get(self):
        return {'hello': 'world'}

class NovoLocatario(Resource):
    def put(self, nome):
        # PESSOAS[nome] = nome
        new = Locatario(nome)
        db.session.add(new)
        db.session.commit()
        return 'OK'

class ListarPessoas(Resource):
    def get(self):
        lista = Locatario.query.order_by(Locatario.id).all()
        pessoas = {}
        for i in lista:
            pessoas['pessoa{}'.format(i.id)] = {'id':i.id, 'nome':i.nome}
        return pessoas

# SALA

class NovaSala(Resource):
    def post(self, numero, nome):
        new = Sala(numero, nome)
        db.session.add(new)
        db.session.commit()
        return 'OK'

class ListarSala(Resource):
    def get(self):
        # https: // marshmallow.readthedocs.io / en / 3.0 /
        lista = Sala.query.order_by(Sala.id).all()
        salas = {}
        for i in lista:
            salas['sala{}'.format(i.id)] = {'sala': i.numero, 'nome': i.nome_sala}
        return salas

# não rolou ainda não
class EditarSala(Resource):
    def put(self, id, nome, numero):
        edit = Sala.query.filter_by(id=id).first()
        edit.nome_sala = nome
        edit.numero = numero
        db.session.merge(edit)
        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

class ExcluirSala(Resource):
    def delete(self, id):
        delet = Sala.query.get(id)
        db.session.delete(delet)
        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

# Agendamentos

class NovoAgendamento(Resource):
    def post(self, sala, locatario, horario, data):
        # import pdb; pdb.set_trace()
        new = Agendamento(sala, locatario, horario, data)
        db.session.add(new)
        try:
            return 'OK'
            db.session.commit()
        except: return 'NON'

class ListarAgendamento(Resource):
    def get(self):
        # import pdb ; pdb.set_trace()
        lista = Agendamento.query.order_by(Agendamento.id_agendamento).all()
        # lista = Agendamento.query.filter_by(horario=horario).all()
        agendamentos = {}
        for i in lista:
            agendamentos['agendamento{}'.format(i.id_agendamento)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario':i.horario, 'data':i.data}
        return agendamentos

# class EditarAgendamento(Resource):

class ExcluirAgendamento(Resource):
    def delete(self, id):
        delet = Agendamento.query.get(id)
        db.session.delete(delet)
        try:
            return 'OK'
            db.session.commit()
        except:
            return 'NON'



api.add_resource(HelloWorld, '/')
api.add_resource(NovoLocatario, '/locatario/novo/<string:nome>')
api.add_resource(ListarPessoas, '/locatario/listar')

api.add_resource(ListarSala, '/sala/listar')
api.add_resource(NovaSala, '/sala/novo/nome=<string:nome>&numero=<int:numero>')
api.add_resource(EditarSala, '/sala/editar/id=<int:id>&nome=<string:nome>&numero=<int:numero>')
api.add_resource(ExcluirSala, '/sala/excluir/<int:id>')

api.add_resource(ListarAgendamento, '/agendamento/listar')

# api.add_resource(ListarAgendamento, '/agendamento/listar/sala=<int:id_sala>')
# api.add_resource(ListarAgendamento, '/agendamento/listar/sala=<int:id_sala>&horario=<int:horario>&data=data')

api.add_resource(NovoAgendamento, '/agendamento/novo/sala=<int:sala>&locatario=<int:locatario>&horario=<string:horario>&data=<string:data>')
# api.add_resource(EditarAgendamento, '/agendamento/editar/id=<int:id>&sala=<int:sala>&locatario=<int:locatario>&horario=<date:horario>')
api.add_resource(ExcluirAgendamento, '/agendamento/excluir/<int:id>')



# api.add_resource(NovoLocatario, '/locatario/<string:nome>')