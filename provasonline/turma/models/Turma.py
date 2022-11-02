from provasonline import db
class Turma(db.Model):
    __tablename__ = 'turma'
    id              = db.Column(db.Integer, primary_key = True)
    id_professor    = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete = 'CASCADE'), nullable = True)
    descricao       = db.Column(db.Text, nullable = True)
    nome            = db.Column(db.Text, nullable = True)

    alunos = db.relationship("AlunoTurma", backref='turma', lazy='dynamic')
    def __init__(self, descricao, nome, id_professor): 
        self.id_professor = id_professor
        self.descricao = descricao
        self.nome = nome

class AlunoTurma(db.Model):

    __tablename__ = 'aluno_na_turma'
    aluno_id      = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete = 'CASCADE'), nullable = True, primary_key = True)
    turma_id      = db.Column(db.Integer, db.ForeignKey('turma.id', ondelete = 'CASCADE'), nullable = True, primary_key = True)

    def __init__(self, aluno_id, turma_id):
        self.aluno_id = aluno_id
        self.turma_id   = turma_id