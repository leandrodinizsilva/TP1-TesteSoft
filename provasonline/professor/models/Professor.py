from provasonline import db
from flask_bcrypt import Bcrypt
from provasonline.usuario.models.Usuario import Usuario

######################################################################
#####                         PROFESSOR                          #####
######################################################################

class Professor(Usuario): 
	bcrypt = Bcrypt()

	__mapper_args__ = {
		'polymorphic_identity':"professor"
	}

	__tablename__ = 'professor'
	id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

	def __init__(self, nome, login, senha, urole):
		self.nome		= nome
		self.login		= login
		self.senha 		= self.setSenha(senha)
		self.urole		= urole