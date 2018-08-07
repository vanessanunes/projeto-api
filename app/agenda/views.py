from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from app import app, db
from app.agenda.models import Locatario, Sala, Agendamento, LocatarioSchema
from datetime import date, datetime
from marshmallow import Schema, fields, pprint

api = Api(app)

def verificar_agendas(agenda, horario, sala):
    # import pdb; pdb.set_trace()
    if not agenda:
        # liberado
        return False

    if agenda.id_sala == sala and agenda.horario == horario:
        # já tem cadastro
        return True

class HelloWorld(Resource):
    # tá ok
    def get(self):
        return dict(hello='world')

# class LocatarioSchema(Schema):
#     nome = fields.Str()
#     id = fields.Number()


class NovoLocatario(Resource):
    def post(self, nome):
        new = Locatario(nome)
        db.session.add(new)
        try:
            db.session.commit()
            print('OK')
            return 'OK'
        except:
            print('NON')
            return 'NON'


class ListarPessoas(Resource):
    def get(self):
        # locatario = Locatario.query.order_by(Locatario.id).all()
        lista = Locatario.query.order_by(Locatario.id).all()
        # schema = LocatarioSchema()
        # result = schema.dump(lista)
        # pprint(result)
        pessoas = {}
        for i in lista:
            pessoas['pessoa{}'.format(i.id)] = {'id':i.id, 'nome':i.nome}
        return pessoas

# SALA

class NovaSala(Resource):
    def post(self, nome, numero):
        new = Sala(numero, nome)
        db.session.add(new)
        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

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

# AGENDAMENTO

class NovoAgendamento(Resource):
    def post(self, sala, locatario, horario, data):
        data = datetime.strptime(data, '%d-%m-%Y')
        horario = datetime.strptime(horario, '%H:%M')
        horario = data.replace(hour=horario.hour, minute=horario.minute)
        agenda = Agendamento.query.filter_by(id_sala=sala).first()
        verificar = verificar_agendas(agenda, horario, sala)

        if verificar is True:
            return 'Já existe horario cadastrado para essa sala. Tente outro.'

        new = Agendamento(sala, locatario, horario)
        db.session.add(new)

        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

class ListarAgendamento(Resource):
    def get(self):
        lista = Agendamento.query.order_by(Agendamento.id).all()
        agendamentos = {}
        for i in lista:
            horario = i.horario.strftime('%d/%m/%Y %H:%M')
            # # # # # # # # # # # # # # # # # # #
            #   VER COMO SERIALIZAR CERTOOOOOO  #
            # # # # # # # # # # # # # # # # # # #
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario':horario}

        return agendamentos

class EditarAgendamento(Resource):
    def put(self, id, sala, locatario, data, hora):
        edit = Agendamento.query.filter_by(id=id).first()
        edit.id_sala = sala
        edit.id_locatario = locatario
        data = datetime.strptime(data, '%d-%m-%Y')
        horario = datetime.strptime(hora, '%H:%M')
        horario = data.replace(hour=horario.hour, minute=horario.minute)

        agenda = Agendamento.query.filter_by(horario=horario).first()
        verificar = verificar_agendas(agenda, horario, sala)
        if verificar is True:
            return 'Já existe agenda para essa sala e horario. Tente outro horario ou dia.'

        edit.horario = horario

        db.session.merge(edit)
        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

class ExcluirAgendamento(Resource):
    def delete(self, id):
        excluir = Agendamento.query.get(id)
        # excluir direito, primeiro verificar se existe, se não mostrar msg
        # que não existe, se sim, excluir
        db.session.delete(excluir)
        try:
            db.session.commit()
            return 'OK'
        except:
            return 'NON'

class FiltrarAgendamentoSala(Resource):
    def post(self, sala):
        salas = Agendamento.query.filter_by(id_sala=sala).all()
        # import pdb ; pdb.set_trace()
        agendamentos = {}
        for i in salas:
            horario = i.horario.strftime('%d/%m/%Y %H:%M')
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario': horario}
        return agendamentos

class FiltrarAgendamentoData(Resource):
    def post(self, data):
        data_inicio = datetime.strptime(data, '%d-%m-%Y')
        # 23:59 as 00:00
        data_fim = data_inicio.replace(hour=23, minute=59)
        datas = Agendamento.query.order_by(horario=data).all()
        datas = Agendamento.query.filter(Agendamento.horario.between(data_inicio, data_fim)).all()
        agendamentos = {}
        for i in datas:
            horario = i.horario.strftime('%d/%m/%Y %H:%M')
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario': horario}
        return agendamentos


api.add_resource(HelloWorld, '/')
api.add_resource(NovoLocatario, '/locatario/novo/nome=<string:nome>')
api.add_resource(ListarPessoas, '/locatario/listar')

api.add_resource(ListarSala, '/sala/listar')
api.add_resource(NovaSala, '/sala/novo/nome=<string:nome>&numero=<int:numero>')
api.add_resource(EditarSala, '/sala/editar/id=<int:id>&nome=<string:nome>&numero=<int:numero>')
api.add_resource(ExcluirSala, '/sala/excluir/id=<int:id>')

api.add_resource(ListarAgendamento, '/agendamento/listar')

api.add_resource(FiltrarAgendamentoSala, '/agendamento/filtrar/sala=<int:sala>')
api.add_resource(FiltrarAgendamentoData, '/agendamento/filtrar/data=<string:data>')

# api.add_resource(ListarAgendamento, '/agendamento/listar/sala=<int:id_sala>&horario=<int:horario>&data=data')

api.add_resource(NovoAgendamento, '/agendamento/novo/sala=<int:sala>&locatario=<int:locatario>&hora=<string:horario>&data=<string:data>')
api.add_resource(EditarAgendamento, '/agendamento/editar/id=<int:id>&sala=<int:sala>&locatario=<int:locatario>&data=<string:data>&hora=<string:hora>')
api.add_resource(ExcluirAgendamento, '/agendamento/excluir/id=<int:id>')



# api.add_resource(NovoLocatario, '/locatario/<string:nome>')