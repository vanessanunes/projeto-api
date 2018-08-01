#PARTE1
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

#PARTE2
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


#PARTE3
@app.route('/api/v1/filmes', methods=['GET'])
def filmes():
  #MEU CÓDIGO AQUI
  return"Tudo pronto!"

#PARTE4
# if __name__ == '__main__':
#   port = int(os.environ.get('PORT', 5000))
#   app.run(host='127.0.0.1', port=port)