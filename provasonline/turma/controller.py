import re
from provasonline import db, login_required
from flask_login import LoginManager, current_user
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from provasonline.turma.models.Turma import Turma , AlunoTurma
from provasonline.aluno.models.Aluno import Aluno
from provasonline.prova.models.Prova import Prova
from provasonline.usuario.models.Usuario import Usuario
from provasonline.constants import usuario_urole_roles
import json

turma = Blueprint('turma', __name__, template_folder='templates')

@turma.route("/editar_turma", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def editar_turma():
    id_turma = request.args.get('id')
    turmas = Turma.query.filter(Turma.id == id_turma).all()
    turmas = turmas[0]
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        db.session.query(Turma).filter(Turma.id == id_turma).update({Turma.nome: nome, Turma.descricao : descricao})
        db.session.commit()
        flash("Turma alterada com sucesso")
        return redirect(url_for('turma.listar_turmas'))
    return render_template("editar_turma.html", turma=turmas)

@turma.route("/adicionar_professor", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def adicionar_professor():
    id = request.args.get('id')

    professores = db.session.query(Usuario, Turma).outerjoin(Turma, (Usuario.id == Turma.id_professor) & (Turma.id == id)).filter(Usuario.urole == 'professor' ).all()
    # Mudar "Usuario" para professor
    if request.method == 'POST':
        lista_id = request.form.getlist('professor')
        id_turma = request.form['id_turma']
        db.session.query(Turma).filter(Turma.id == id_turma).update({Turma.id_professor: lista_id[0]})
        db.session.commit()
 
        return redirect(url_for('turma.adicionar_professor', id=id))

    return render_template("adicionar_professor.html", professores=professores)

@turma.route("/listar_turmas", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def listar_turmas():
    turmas = Turma.query.filter(Turma.id_professor == current_user.id)    
    return render_template("listar_turmas.html", turmas=turmas)

@turma.route("/ver_turma", methods=["GET","POST"])
@login_required()
def ver_turma():
    id_turma = request.args.get('id')
    professores = db.session.query(Usuario, Turma).outerjoin(Turma, (Usuario.id == Turma.id_professor) & (Turma.id == id_turma)).filter(Turma.id_professor == Usuario.id).all()
    turmas = Turma.query.filter(Turma.id == id_turma).all()
    provas = Prova.query.filter(Prova.turma == id_turma)
    return render_template("ver_turma.html", turmas=turmas, professores=professores, provas = provas)

@turma.route("/cadastrar_turma", methods=["GET", "POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def cadastrar_turma():
    if request.method == 'POST':

        # descricao = request.form['prova']
        nome = request.form['nome']
        descricao = request.form['descricao']
        turma     = Turma(descricao, nome, current_user.id)
        db.session.add(turma)
        db.session.commit()
        flash("Turma cadastrada com sucesso")
        return redirect(url_for('turma.listar_turmas'))
    return render_template("cadastrar_turma.html")

@turma.route("/adicionar_alunos", methods=["GET", "POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def adicionar_alunos():
    id = request.args.get('id')
    alunos = db.session.query(Aluno, AlunoTurma).outerjoin(AlunoTurma, (Aluno.id == AlunoTurma.aluno_id) & (AlunoTurma.turma_id == id)).all()

    if request.method == 'POST':
        lista_id = request.form.getlist('alunos')
        id_turma = request.form['id_turma']
        AlunoTurma.query.filter(AlunoTurma.turma_id == id_turma).delete()
        db.session.commit()
        for id_user in lista_id:
            alunoturma = AlunoTurma(id_user, id_turma)
            db.session.add(alunoturma)
            db.session.commit()
        id = id_turma
        return redirect(url_for('turma.ver_turma', id=id))
    return render_template("adicionar_alunos.html", id = id, alunos = alunos)