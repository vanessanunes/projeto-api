import os.path, sys
import unittest
import requests

dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..'))
sys.path.append(dirname)

from app import app, db

TEST_DB = 'test.db'
BASEDIR = os.path.abspath(os.path.join(os.path.dirname( __file__ )))

class TestesBasico(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(BASEDIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    ## LOCATARIO

    def test_novo_locatario(self):
        response = requests.post('http://localhost:5000/locatario/novo/nome=Vanessa')
        self.assertEqual(response.json(), {"resultado": "TRUE"})

    def test_listar_locatario(self):
        response = requests.get('http://localhost:5000/locatario/listar')
        self.assertEqual(response.status_code, 200)

    def test_excluir_locatario(self):
        response = requests.delete('http://localhost:5000/locatario/excluir/id=1')
        self.assertEqual(response.json(), {"resultado": "TRUE"})

    ## SALA

    def test_nova_sala(self):
        response = requests.post('http://localhost:5000/sala/novo/nome=Rosa&numero=30')
        self.assertEqual(response.status_code, 200)

    def test_listar_sala(self):
        response = requests.get('http://localhost:5000/sala/listar')
        self.assertEqual(response.status_code, 200)
    #
    def test_editar_sala(self):
        response = requests.put('http://localhost:5000/sala/editar/id=1&nome=Amarelo&numero=30')
        self.assertEqual(response.status_code, 200)

    def test_excluir_sala(self):
        response = requests.delete('http://localhost:5000/sala/excluir/id=1')
        self.assertEqual(response.json(), {"resultado": "TRUE"})

    ## AGENDAMENTO

    def test_novo_agendamento(self):
        response = requests.post('http://localhost:5000/agendamento/novo/sala=1&locatario=1&data=09-08-2018&hora_inicio=09:30&hora_fim=11:30')
        self.assertEqual(response.status_code, 200)

    def test_listar_agendamento(self):
        response = requests.get('http://localhost:5000/agendamento/listar')
        self.assertEqual(response.status_code, 200)

    def test_editar_agendamento(self):
        response = requests.put('http://localhost:5000/agendamento/editar/id=1&sala=2&locatario=1&data=10-08-2018&hora_inicio=10:30&hora_fim=12:00')
        self.assertEqual(response.status_code, 200)

    def test_filtrar_data_agendamento(self):
        response = requests.get('http://localhost:5000/agendamento/filtrar/data=10-08-2018')
        self.assertEqual(response.status_code, 200)

    def test_filtrar_sala_agendamento(self):
        response = requests.get('http://localhost:5000/agendamento/filtrar/sala=2')
        self.assertEqual(response.status_code, 200)

    def test_excluir_agendamento(self):
        response = requests.delete('http://localhost:5000/agendamento/excluir/id=1')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()