from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Acesse <a href='/api/v1/filmes'>aqui</a>"


@app.route('/api/v1/filmes', methods=['GET'])
def filmes():
    res = requests.get('http://www.adorocinema.com/filmes/numero-cinemas/')
    soup = BeautifulSoup(res.content)

    data = []
    lista_filmes = soup.find_all('li', {'class':'mdl'})
    for filme in lista_filmes:
        nome = filme.find('h2', {'class':'meta-title'}).text.strip()
        info = filme.find('div', {'class':'meta-body-item meta-body-info'}).text.strip()
        direcao = filme.find('div', {'class':'meta-body-item meta-body-direction light'}).text.strip()
        sinopse = filme.find('div', {'class':'synopsis'}).text.strip()
        cartaz = filme.find('figure', {'class': 'thumbnail'}).find('img')['data-src']

        data.append({'nome': nome,
                 'info': info,
                 'direcao':direcao,
                 'sinopse': sinopse,
                 'cartaz':cartaz
                 })


    return jsonify({'filmes': data})

if __name__ == "__main__":
    app.run()