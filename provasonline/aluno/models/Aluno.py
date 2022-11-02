from provasonline import db
from flask_bcrypt import Bcrypt
from provasonline.usuario.models.Usuario import Usuario
from provasonline.turma.models.Turma import AlunoTurma
from provasonline.prova.models.Prova import AlunoProva

######################################################################
#######                         ALUNO                          #######
######################################################################

class Aluno(Usuario): 
	bcrypt = Bcrypt()

	__mapper_args__ = {
		'polymorphic_identity':"aluno"
	}

	__tablename__ = 'aluno'
	id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
	# turmas = db.relationship("Turma", secondary=AlunoTurma, back_populates="alunos")
	# provas = db.relationship("Prova", secondary=AlunoProva, back_populates="alunos")

	def __init__(self, nome, login, senha, urole):
		self.nome		= nome
		self.login		= login
		self.senha 		= self.setSenha(senha)
		self.urole		= urole


	