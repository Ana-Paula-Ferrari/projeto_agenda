from app import app, db
from flask import render_template, redirect, session, url_for, request, flash
from models.tabelas import Usuario
from helpers import FormularioUsuario, FormularioCadastro
from flask_bcrypt import check_password_hash, generate_password_hash



@app.route('/novo_usuario')
def novo_usuario():
    form = FormularioCadastro()
    proxima = request.args.get('proxima')
    return render_template('usuario.html', proxima=proxima, form=form)
    

@app.route('/cadastrar_usuario', methods=['POST',])
def cadastrar_usuario():
    
    form = FormularioCadastro(request.form)

    nome = form.nome.data
    senha = generate_password_hash(form.senha.data).decode("utf-8")
   
    #buscar se já tem no banco um usuario com o nome fornecido
    usuario = Usuario.query.filter_by(nome=nome).first()

    if usuario:
        flash('Usuário já cadastrado! ')
        return redirect(url_for('login'))
    
    #gravar no banco
    novo_usuario = Usuario(nome=nome, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login')
def login():
    form = FormularioUsuario()
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():

    form = FormularioUsuario()
    usuario = Usuario.query.filter_by(nome=form.nome.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    
    if usuario and senha:
        session['usuario_logado'] = usuario.nome
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

