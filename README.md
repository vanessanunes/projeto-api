# aprendendo-api


## Criar virtualenv:

```python3 -m venv myvenv```


## Para entrar no virtualenv:

```. myvenv/bin/activate```


## Execute o requirements

```$ venv/bin/pip3 install -r requirements.txt```




#####ler sobre


Tutorial: https://codigosimples.net/2017/05/15/criando-uma-api-de-filmes-em-cartaz-usando-python-e-heroku/


https://marshmallow.readthedocs.io/en/3.0/

--

Ver data e horario - provavelmente precise separar
horas - incluir data de termino e verificar se já está ocupado
ver algum metodo pra transformar tipo o horario de fim e de inicio em "hash" e comprar entre esses dois valores pra acusar se já está sendo ou não usado esse horario
Algo como:  _unix_time_millis(data), _unix_time_millis(prox_data)
* Consegui um filter between que pode ajudar nisso :)