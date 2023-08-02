import os

FLASK_ENV="development"
SECRET_KEY = 'alura'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:208931@localhost/agenda'

#caminho relativo para a pasta de uploads/ Dirname devolve o caminho do elemento dentro dele 
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'