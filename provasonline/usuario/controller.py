import os
from provasonline.usuario.models.Usuario import Usuario, load_user
from provasonline.professor.models.Professor import Professor
from provasonline.aluno.models.Aluno import Aluno
from provasonline.turma.models.Turma import Turma, AlunoTurma
from flask import render_template, request, redirect, url_for, flash
from provasonline import login_required
from flask_login import LoginManager, current_user, login_user, logout_user
from flask import Blueprint
from provasonline.usuario.models.Forms import LoginForm, UsuarioForm
from flask_bcrypt import Bcrypt
from provasonline import db, login_manager

usuario = Blueprint('usuario', __name__, template_folder='templates')

######################################################################
######                         INICIO                          #######
######################################################################

@usuario.route('/inicio')
@usuario.route('/', methods=['GET','POST'])
@login_required()
def index():
    if current_user.urole == "professor":
        turmas = Turma.query.filter_by(id_professor = current_user.id)
    else:
        id_turmas = []
        turmas_aluno = AlunoTurma.query.filter_by(aluno_id = current_user.id)
        for turma in turmas_aluno:
            id_turmas.append(turma.turma_id)
        turmas = Turma.query.filter(Turma.id.in_(id_turmas))
    return render_template('inicio.html', turmas = turmas)
            
   
######################################################################
########                        LOGIN                          #######
######################################################################

@usuario.route('/login', methods=['GET','POST'])
def login():
    #For GET requests, display the login form. 
    #For POSTS, login the current user by processing the form.
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        usuario = Usuario.query.filter_by(login=form.login.data).first()
        if usuario:
            autenticated_usuario = usuario.bcrypt.check_password_hash(usuario.senha, form.senha.data)
            if autenticated_usuario:
                usuario.authenticated = True
                login_user(usuario, remember=True)
                # flash("Usuario logado.")
                return redirect(url_for('usuario.index'))
            else:
                flash("Senha incorreta.")
        else: 
            flash("Login Inválido.")
    else:
        print(form.errors)
    return render_template('login.html', form=form)
    

######################################################################
########                        LOGOUT                         #######
######################################################################

@usuario.route('/logout', methods=['GET','POST'])
@login_required()
def logout():
    logout_user()
    return redirect(url_for('usuario.login'))

@usuario.route('/cadastrar_usuario', methods=['GET','POST'])
# @login_required()
def cadastrar_usuario():
    form = UsuarioForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            if(request.form["urole"] == 'professor'):
                entidade_usuario = Professor(nome = form.nome.data, login = form.login.data, senha = form.senha.data, urole = request.form["urole"])
                db.session.add(entidade_usuario)
            else:
                entidade_usuario = Aluno(nome = form.nome.data, login = form.login.data, senha = form.senha.data, urole = request.form["urole"])
                db.session.add(entidade_usuario)  

            db.session.commit()
            flash("Usuário cadastrado com sucesso!")
        else:
            return redirect(url_for('usuario.cadastrar_usuario'))

        return redirect(url_for('usuario.login'))

    return render_template('cadastrar_usuario.html', form=form)