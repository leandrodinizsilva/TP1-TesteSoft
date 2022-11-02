import os
from functools import wraps
from flask import Flask, redirect, url_for, flash, current_app
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'AGKDGYdsfdfsI874RY9823gsdgdfgYR08Y20sdfwe93287RrewgN2NYORN3827'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://geovanna:BKc8QJen5wyxkh6p@34.222.122.201/provasonline'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db, compare_type = True)

#################################################################
################# VARIAVEIS/FUNCOES DO TEMPLATE #################
#################################################################

from provasonline.constants import usuario_urole_roles
@app.context_processor
def insere_usuario_urole_roles():
    return dict(usuario_urole_roles=usuario_urole_roles)

#################################################################
###################### CONFIGURA LOGIN ##########################
#################################################################

login_manager.init_app(app)
login_manager.login_view = "usuario.login"
login_manager.login_message = "Não foi possível acessar esta página ou executar esta ação. Por favor confira se o login foi feito ou se você tem a devida permissão."

def login_required(role=["ANY"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
               return current_app.login_manager.unauthorized()
            urole = current_user.urole
            if ((urole not in role) and (role != ["ANY"])):
                flash("Você não tem permissão para acessar essa página.")
                return redirect(url_for('usuario.index'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

#################################################################
########################## MODELS ###############################
#################################################################

from provasonline.usuario.models.Usuario import Usuario
from provasonline.aluno.models.Aluno import Aluno
from provasonline.professor.models.Professor import Professor
from provasonline.prova.models.Prova import Prova
from provasonline.turma.models.Turma import Turma

#################################################################
########################## BLUEPRINTS ###########################
#################################################################

from provasonline.usuario.controller import usuario
from provasonline.aluno.controller import aluno
from provasonline.professor.controller import professor
from provasonline.prova.controller import prova
from provasonline.turma.controller import turma

app.register_blueprint(usuario, url_prefix='/')
app.register_blueprint(aluno, url_prefix='/aluno')
app.register_blueprint(professor, url_prefix='/professor')
app.register_blueprint(prova, url_prefix='/prova')
app.register_blueprint(turma, url_prefix='/turma')

