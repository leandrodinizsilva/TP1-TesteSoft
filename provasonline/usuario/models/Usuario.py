
from provasonline import db, login_manager
from sqlalchemy.sql import case
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Usuario.query.filter_by(id = id).first() 

class Usuario(db.Model, UserMixin):
    bcrypt = Bcrypt()

    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255), nullable = False)
    urole = db.Column(db.String(50), server_default="user", nullable=False)

    __mapper_args__ = {
        "polymorphic_on":case(
            [
                (urole == "professor", "professor"),
                (urole == "aluno", "aluno"),
            ]
         )        
    }
    
    def __init__(self, login, senha, nome, urole):
        self.nome = nome
        self.login = login
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')
        self.urole = urole
    
    def setSenha(self, senha):
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')
        return self.senha
    
    def get_id(self):
        return self.id
