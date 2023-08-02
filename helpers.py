import os
from app import app;
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField


#validar as informações do formulario
class FormularioContato(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=3)])
    apelido = StringField('Apelido', [validators.DataRequired(), validators.Length(min=3)])
    telefone = StringField('Telefone',[validators.DataRequired(), validators.Length(min=3)] )
    email = StringField('E-mail', [validators.DataRequired(), validators.Length(min=7)] )
    salvar = SubmitField('Salvar')

#Funçoes auxiliar
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'img{id}' in nome_arquivo:
            return nome_arquivo

    return 'img_padrao.jpg'


def deletar_imagem(id):
    arquivo = recupera_imagem(id) #recupera o nome da imagem que vai ser deletada
    if arquivo != 'img_padrao.jpg':
        #remove img e busca na pasta o arquivo sem ficar dependente de Sistema Op.
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))