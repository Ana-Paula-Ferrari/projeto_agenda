from app import app, db
from flask import render_template, redirect, session, url_for, request, flash, send_from_directory
from models.tabelas import Contatos
from helpers import recupera_imagem, deletar_imagem,  FormularioContato
import time


#pagina principal
@app.route('/')
def index():

    #buscar todos os contatos para exibir
    lista = Contatos.query.order_by(Contatos.id)
    return render_template('lista.html', titulo='Agenda', agenda=lista)

#VERIFICAR ROTA
#adicionar um contato
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    
    form = FormularioContato()
    return render_template('novo.html', titulo='Novo Contato', form=form)


#criando um novo contato
@app.route('/criar', methods=['POST',])
def criar():

    #Instanciar formulario
    form = FormularioContato(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    
    nome = form.nome.data
    apelido = form.apelido.data
    telefone = form.telefone.data
    email = form.email.data
    
    #buscar se já tem no banco um contato com o nome fornecido
    contato = Contatos.query.filter_by(nome=nome).first()

    if contato:
        flash('Contato já existente! ')
        return redirect(url_for('index'))
    
    #gravar no banco
    novo_contato = Contatos(nome=nome, apelido=apelido, telefone=telefone, email=email)
    db.session.add(novo_contato)
    db.session.commit()

    #pegar a imagem recebida 
    arquivo = request.files['arquivo']
    #arquivo.save(f'uploads/{arquivo.filename}') #salvar na pasta uploads com o nome do arquivo
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/img{novo_contato.id}-{timestamp}.jpg') #salvar na pasta uploads com o id do contato
    return redirect(url_for('index'))



#editar um contato
@app.route('/editar/<int:id>') #recebe id de lista.html
def  editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    
    contato = Contatos.query.filter_by(id=id).first() #busca o contato com o id informado

    form = FormularioContato()
    form.nome.data = contato.nome
    form.apelido.data = contato.apelido
    form.telefone.data = contato.telefone
    form.email.data = contato.email

    img_contato = recupera_imagem(id)

    return render_template('editar.html', titulo='Editar Contato', id=id, img_contato=img_contato, form=form) #passa o contato p/ editar.html


#atualizar um contato
@app.route('/atualizar', methods=['POST',])
def atualizar():

    form = FormularioContato(request.form)

    if form.validate_on_submit():
        #para o contato correspondente ao id, atualizar os campos setados com os dados recebidos do request
        contato = Contatos.query.filter_by(id=request.form['id']).first()
        contato.nome = form.nome.data
        contato.apelido = form.apelido.data
        contato.telefone = form.telefone.data
        contato.email = form.email.data
   
    #gravar no banco
    db.session.add(contato)
    db.session.commit()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deletar_imagem(contato.id)
    arquivo.save(f'{upload_path}/img{contato.id}-{timestamp}.jpg') #salvar na pasta uploads com o id do contato

    return redirect(url_for('index'))


#deletar um contato
@app.route('/deletar/<int:id>')
def deletar(id):
     if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
     
     Contatos.query.filter_by(id=id).delete()
     db.session.commit()
     flash('Contato deletado com sucesso! ')
     return redirect(url_for('index'))


#imagem do contato
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)