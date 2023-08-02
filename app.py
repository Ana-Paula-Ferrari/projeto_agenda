from flask import Flask
from flask_sqlalchemy import SQLAlchemy;

#instaciar a aplicacao flask
app = Flask(__name__)

#referencia ao arquivo que possue as configurações
app.config.from_pyfile('config.py')

#instancia do ORM
db = SQLAlchemy(app)

#importar todas as rotas
from views.rotas import *


#permite importacoes multiplas
if __name__ == '__main__':
    app.run(debug=True)