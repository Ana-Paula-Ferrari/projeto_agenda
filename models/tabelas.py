from app import app, db;


class Contatos(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome= db.Column(db.String)
    apelido= db.Column(db.String)
    telefone= db.Column(db.String)
    email = db.Column(db.String)


    def __init__(self, nome, apelido, telefone, email):
        self.nome=nome
        self.apelido=apelido
        self.telefone=telefone
        self.email=email

    def __repr__(self):
        return '<nome %r>' % self.nome



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

def __repr__(self):
       return '<nome %r>' % self.nome

