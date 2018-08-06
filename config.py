import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

file_path = os.path.abspath(os.getcwd())
# SQLALCHEMY_DATABASE_URI = 'sqlite:///'+file_path+"\database.db"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'um-nome-seguro'

LOGFILE = file_path+'\\ate.log'
TESTING = True
THREADED = True
