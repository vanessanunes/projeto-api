import unittest
# from app import app
import app.agenda.models # 
from app.agenda.views import NovoLocatario



# def TestCaseNovoLocatario(nome):

    # def post(self, nome):
    #     new = Locatario(nome)
    #     db.session.add(new)
    #     try:
    #         db.session.commit()
    #         logging.info('Novo locatario salvo com sucesso')
    #         return dict(resultado = 'TRUE')
    #     except:
    #         logging.info('Não foi possivel salvar locatario')
    #         return dict(resultado='FALSE')

# return dict(resultado = 'TRUE')

class TestCaseNovoLocatario(unittest.TestCase):
    def test(self):
        self.assertEqual(NovoLocatario.post('Mariana'), dict(resultado = 'TRUE'))

if __name__ == '__main__':
    unittest.main()