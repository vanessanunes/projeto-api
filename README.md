# projeto-api

Desenvolvido utilizando Python 3, framework Flask, e as bibliotecas Flask-RESTful, Flask-SQLAlchemy, BeautifulSoup, logging..

## Mão na massa

Clone esse repositório com:
 
 ```git clone https://github.com/vanessanunes/aprendendo-api.git```


Crie um ambiente virtual:

```python -m venv myvenv```


Para entrar no virtualenv:

Linux: ```. myvenv/bin/activate``` ou Windows: ```source myvenv/Script/activate```

Instale as bibliotecas necessárias com o comando abaixo:

```$ pip install -r requirements.txt```

Para rodar, use:
```python run.py```

_Para utilizar, você pode instalar o *Postman* em seu computador, ou usar os comandos `curl`, de qualquer forma os protocolos e parametros devem ser usandos da mesma forma._


## Comandos

```curl http://127.0.0.1:5000/```
Se a resposta for "TRUE" significa que a request foi feita com sucesso, caso contrário, não

######Locatario

Adicionar novo locatario:

```curl http://127.0.0.1:5000/locatario/novo/nome=<string:nome> -X POST```

Listar locatarios:

```curl http://127.0.0.1:5000/locatario/listar -X GET```

######Sala

Adicionar nova sala:

```curl "http://127.0.0.1:5000/sala/novo/nome=<string:nome>&numero=<int:numero>" -X POST```

Listar salas:

```curl http://127.0.0.1:5000/sala/listar -X GET```

Editar sala:

```curl "http://127.0.0.1:5000/sala/editar/id=<int:id>&nome=<string:nome>&numero=<int:numero>" -X PUT```

Excluir sala:

```curl "http://127.0.0.1:5000/sala/excluir/id=<int:id>" -X DELETE```

######Agendamento

Adicionar novo agendamento:

_a data deve ser enviada dessa forma: ```08-08-2018```, já a hora: ```09:30```_

Exemplo: ```curl "http://127.0.0.1:5000/agendamento/novo/sala=3&locatario=6&data=09-08-2018&hora_inicio=09:30&hora_fim=11:30" -X POST```

```curl "http://127.0.0.1:5000/agendamento/novo/sala=<int:sala>&locatario=<int:locatario>&data=<string:data>&hora_inicio=<string:hora_inicio>&hora_fim=<string:hora_fim>" -X POST```

Listar agendamento:

```curl http://127.0.0.1:5000/agendamento/listar -X GET```

Filtrar agendamento por sala:

```curl http://127.0.0.1:5000/agendamento/filtrar/sala=<int:sala> -X GET```

Filtrar agendamento por data:

__A data deve ser inserida dessa forma: ```09-09-2018```__

```curl http://127.0.0.1:5000/agendamento/filtrar/data=<string:data> -X GET```

Editar agendamento:

```curl "http://127.0.0.1:5000/agendamento/editar/id=<int:id>&sala=<int:sala>&locatario=<int:locatario>&data=<string:data>&hora_inicio=<string:hora_inicio>&hora_fim=<string:hora_fim>" -X PUT```

Excluir agendamento:
```curl http://127.0.0.1:5000/agendamento/excluir/id=<int:id> -X DELETE```


#Logs

O arquivo de log está em app/agenda/logs.txt

#Testes

Os arquivos de testes estão na pasta ```app/agenda/test/__init__.py```
