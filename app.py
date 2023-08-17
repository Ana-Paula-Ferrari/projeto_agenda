from flask import Flask
from flask_sqlalchemy import SQLAlchemy;
from flask_wtf.csrf import CSRFProtect;
from flask_bcrypt import Bcrypt;

#instaciar a aplicacao flask
app = Flask(__name__)

#referencia ao arquivo que possue as configurações
app.config.from_pyfile('config.py')

#instancia do ORM
db = SQLAlchemy(app)

#token para falha de segurança
csrf = CSRFProtect(app)

#criptografia de senhas
bcrypt = Bcrypt(app)

#importar todas as rotas
from views.views_contatos import *
from views.views_usuarios import *


#permite importacoes multiplas
if __name__ == '__main__':
    app.run(debug=True)