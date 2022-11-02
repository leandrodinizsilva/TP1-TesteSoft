from provasonline import db


class AlunoProva(db.Model):
    __tablename__ = 'aluno_prova'
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id', ondelete = 'CASCADE'), nullable = False, primary_key = True)
    prova_id = db.Column(db.Integer, db.ForeignKey('prova.id', ondelete = 'CASCADE'), nullable = False, primary_key = True)
    nota     = db.Column(db.Integer, nullable = False)

    def __init__(self, aluno_id, prova_id, nota):
        self.aluno_id = aluno_id
        self.prova_id = prova_id
        self.nota     = nota

class Prova(db.Model):

    __tablename__ = 'prova'
    id          = db.Column(db.Integer, primary_key = True)
    descricao   = db.Column(db.Text, nullable = True)
    data        = db.Column(db.Date, nullable = False)
    valor       = db.Column(db.Integer, nullable = True)
    professor   = db.Column(db.Integer, db.ForeignKey('professor.id', ondelete = 'CASCADE'), nullable = True)
    turma       = db.Column(db.Integer, db.ForeignKey('turma.id', ondelete = 'CASCADE'), nullable = True)
    
    perguntas   = db.relationship("Pergunta", backref='perguntas', lazy='dynamic')
    
    def __init__(self, data, descricao, valor, professor, turma):
        self.data      = data
        self.descricao = descricao
        self.valor     = valor
        self.professor = professor
        self.turma     = turma

class Pergunta(db.Model):

    __tablename__ = 'pergunta'
    id          = db.Column(db.Integer, primary_key = True)
    descricao   = db.Column(db.Text, nullable = False)
    prova       = db.Column(db.Integer, db.ForeignKey('prova.id', ondelete = 'CASCADE'), nullable = False)
    valor       = db.Column(db.Integer, nullable = True)

    opcoes = db.relationship("Opcao", backref='opcoes', lazy='dynamic')
    
    def __init__(self, descricao, prova, valor):
        self.descricao = descricao
        self.prova     = prova
        self.valor     = valor

class Opcao(db.Model):

    __tablename__ = 'opcao'
    id          = db.Column(db.Integer, primary_key = True)
    descricao   = db.Column(db.Text, nullable = False)
    correta     = db.Column(db.Boolean, nullable = True)
    pergunta    = db.Column(db.Integer, db.ForeignKey('pergunta.id', ondelete = 'CASCADE'), nullable = False)
    
    def __init__(self, descricao, correta, pergunta):
        self.descricao = descricao
        self.correta   = correta
        self.pergunta  = pergunta

class Resposta(db.Model):

    __tablename__ = 'resposta'
    id         = db.Column(db.Integer, primary_key = True)
    prova      = db.Column(db.Integer, db.ForeignKey('prova.id', ondelete = 'CASCADE'), nullable = False)
    pergunta   = db.Column(db.Integer, db.ForeignKey('pergunta.id', ondelete = 'CASCADE'), nullable = False)
    opcao      = db.Column(db.Integer, db.ForeignKey('opcao.id', ondelete = 'CASCADE'), nullable = False)
    acertou    = db.Column(db.Boolean, nullable = True)
    aluno      = db.Column(db.Integer, db.ForeignKey('aluno.id', ondelete = 'CASCADE'), nullable = True)

    pergunta_obj = db.relationship('Pergunta', foreign_keys=pergunta)
    prova_obj    = db.relationship('Prova', foreign_keys=prova)
    opcao_obj    = db.relationship('Opcao', foreign_keys=opcao)
    
    def __init__(self, prova, pergunta, opcao, acertou, aluno):
        self.prova    = prova
        self.pergunta = pergunta
        self.opcao    = opcao
        self.acertou  = acertou
        self.aluno    = aluno
