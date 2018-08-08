# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from app import app, db
from app.agenda.models import Locatario, Sala, Agendamento
from datetime import datetime
import logging
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

api = Api(app)

filename=os.path.join(basedir, 'logs.txt')
logging.basicConfig(filename=filename, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('INICIANDO...')

def verificar_agendas(horario_inicio, horario_fim, sala):
    if db.session.query(Agendamento).filter(Agendamento.horario_inicio.between(horario_inicio, horario_fim)).filter(
        Agendamento.id_sala == sala).first():
        return True

    return False

# LOCATARIO

class NovoLocatario(Resource):
    def post(self, nome):
        new = Locatario(nome)
        db.session.add(new)
        try:
            db.session.commit()
            logging.info('Novo locatario salvo com sucesso')
            return dict(resultado = 'TRUE')
        except:
            logging.info('Não foi possivel salvar locatario')
            return dict(resultado='FALSE')


class ListarLocatario(Resource):
    def get(self):
        lista = Locatario.query.order_by(Locatario.id).all()
        pessoas = {}
        for i in lista:
            pessoas['pessoa{}'.format(i.id)] = {'id':i.id, 'nome':i.nome}
        logging.info('Retornando lista de locatarios na tela')
        return dict(pessoas)

class ExcluirLocatario(Resource):
    def delete(self, id):
        delet = Locatario.query.get(id)
        db.session.delete(delet)
        try:
            logging.info('Locatario escluido com sucesso')
            db.session.commit()
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel excluir Locatario')
            return dict(resultado='FALSE')

# SALA

class NovaSala(Resource):
    def post(self, nome, numero):
        new = Sala(numero, nome)
        db.session.add(new)
        try:
            logging.info('Nova sala salva com sucesso')
            db.session.commit()
            return dict(resultado='TRUE', mensagem='Sala {} {} salva com sucesso'.format(numero, nome))
        except:
            logging.info('Não foi possivel salva sala')
            return dict(resultado='FALSE')

class ListarSala(Resource):
    def get(self):
        logging.info('Retornando lista de sala na tela')
        lista = Sala.query.order_by(Sala.id).all()
        salas = {}
        for i in lista:
            salas['sala{}'.format(i.id)] = {'sala': i.numero, 'nome': i.nome_sala}
        return dict(salas)

class EditarSala(Resource):
    def put(self, id, nome, numero):
        edit = Sala.query.filter_by(id=id).first()
        if not edit:
            return 'Não encontramos esse registro'

        edit.nome_sala = nome
        edit.numero = numero
        db.session.merge(edit)
        try:
            logging.info('Sala editada com sucesso')
            db.session.commit()
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel editar sala')
            return dict(resultado='FALSE')

class ExcluirSala(Resource):
    def delete(self, id):
        delet = Sala.query.get(id)
        db.session.delete(delet)
        try:
            logging.info('Sala escluida com sucesso')
            db.session.commit()
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel excluir Sala')
            return dict(resultado='FALSE')

# AGENDAMENTO

class NovoAgendamento(Resource):
    def post(self, sala, locatario, data, hora_inicio, hora_fim):
        data = datetime.strptime(data, '%d-%m-%Y')
        hora_inicio = datetime.strptime(hora_inicio, '%H:%M')
        hora_fim = datetime.strptime(hora_fim, '%H:%M')

        horario_inicio = data.replace(hour=hora_inicio.hour, minute=hora_inicio.minute)
        horario_fim = data.replace(hour=hora_fim.hour, minute=hora_fim.minute)

        verificar = verificar_agendas(horario_inicio, horario_fim, sala)

        if verificar is True:
            return dict(resultado='FALSE', mensagem='Já existe horario cadastrado para essa sala. Tente outro.')

        new = Agendamento(sala, locatario, horario_inicio, horario_fim)
        db.session.add(new)

        try:
            db.session.commit()
            logging.info('Novo agendamento feito com sucesso')
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel cadastrar agendamento')
            return dict(resultado='FALSE')

class ListarAgendamento(Resource):
    def get(self):
        lista = Agendamento.query.order_by(Agendamento.id).all()
        agendamentos = {}
        logging.info('Retornando lista de agendamento na tela')
        for i in lista:
            horario_inicio = i.horario_inicio.strftime('%d/%m/%Y %H:%M')
            horario_fim = i.horario_fim.strftime('%d/%m/%Y %H:%M')
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario_inicio':horario_inicio, 'horario_fim':horario_fim}
        return dict(agendamentos)

class EditarAgendamento(Resource):
    def put(self, id, sala, locatario, data, hora_inicio, hora_fim):
        edit = Agendamento.query.filter_by(id=id).first()
        edit.id_sala = sala
        edit.id_locatario = locatario
        data = datetime.strptime(data, '%d-%m-%Y')
        horario_inicio = datetime.strptime(hora_inicio, '%H:%M')
        horario_fim = datetime.strptime(hora_fim, '%H:%M')

        horario_inicio = data.replace(hour=horario_inicio.hour, minute=horario_inicio.minute)
        horario_fim = data.replace(hour=horario_fim.hour, minute=horario_fim.minute)

        verificar = verificar_agendas(horario_inicio, horario_fim, sala)

        if verificar is True:
            return dict(resultado='FALSE', mensagem='Já existe agenda para essa sala e horario. Tente outro horario ou dia.')

        edit.horario_inicio = horario_inicio
        edit.horario_fim = horario_fim

        db.session.merge(edit)
        try:
            db.session.commit()
            logging.info('Agendamento editado salva com sucesso')
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel editar agendamento')
            return dict(resultado='FALSE')

class ExcluirAgendamento(Resource):
    def delete(self, id):
        excluir = Agendamento.query.get(id)
        if not excluir:
            return dict(resultado='FALSE')
        db.session.delete(excluir)
        try:
            db.session.commit()
            logging.info('Agendamento excluido com sucesso')
            return dict(resultado='TRUE')
        except:
            logging.info('Não foi possivel excluir agendamento')
            return dict(resultado='FALSE')

class FiltrarAgendamentoSala(Resource):
    def get(self, sala):
        salas = Agendamento.query.filter_by(id_sala=sala).all()
        agendamentos = {}
        for i in salas:
            horario_inicio = i.horario_inicio.strftime('%d-%m-%Y %H:%M')
            horario_fim = i.horario_fim.strftime('%d-%m-%Y %H:%M')
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario_inicio': horario_inicio, 'horario_fim':horario_fim}
        logging.info('Filtrando agendamento por sala: {}'.format(sala))
        return dict(agendamentos)

class FiltrarAgendamentoData(Resource):
    def get(self, data):
        data_inicio = datetime.strptime(data, '%d-%m-%Y')
        data_fim = data_inicio.replace(hour=23, minute=59)

        datas = db.session.query(Agendamento).filter(Agendamento.horario_inicio.between(data_inicio, data_fim)).order_by(Agendamento.id).all()

        agendamentos = {}
        for i in datas:
            h_inicio = i.horario_inicio.strftime('%d/%m/%Y %H:%M')
            h_fim = i.horario_fim.strftime('%d/%m/%Y %H:%M')
            agendamentos['agendamento{}'.format(i.id)] = {'sala': i.id_sala, 'locatario': i.id_locatario,
                                                          'horario_inicio': h_inicio, 'horario_fim':h_fim}
        logging.info('Filtrando agendamento por data: {}'.format(data))
        return dict(agendamentos)

# ROTAS

api.add_resource(NovoLocatario, '/locatario/novo/nome=<string:nome>')
api.add_resource(ListarLocatario, '/locatario/listar')
api.add_resource(ExcluirLocatario, '/locatario/excluir/id=<int:id>')

api.add_resource(ListarSala, '/sala/listar')
api.add_resource(NovaSala, '/sala/novo/nome=<string:nome>&numero=<int:numero>')
api.add_resource(EditarSala, '/sala/editar/id=<int:id>&nome=<string:nome>&numero=<int:numero>')
api.add_resource(ExcluirSala, '/sala/excluir/id=<int:id>')

api.add_resource(ListarAgendamento, '/agendamento/listar')

api.add_resource(FiltrarAgendamentoSala, '/agendamento/filtrar/sala=<int:sala>')
api.add_resource(FiltrarAgendamentoData, '/agendamento/filtrar/data=<string:data>') # data apenas incluir o dia: 27-12-1993

api.add_resource(NovoAgendamento, '/agendamento/novo/sala=<int:sala>&locatario=<int:locatario>&data=<string:data>&hora_inicio=<string:hora_inicio>&hora_fim=<string:hora_fim>')
api.add_resource(EditarAgendamento, '/agendamento/editar/id=<int:id>&sala=<int:sala>&locatario=<int:locatario>&data=<string:data>&hora_inicio=<string:hora_inicio>&hora_fim=<string:hora_fim>')
api.add_resource(ExcluirAgendamento, '/agendamento/excluir/id=<int:id>')

