from flask import Blueprint
from provasonline import db, login_required
from provasonline.constants import usuario_urole_roles
from provasonline.aluno.models.Aluno import Aluno
from provasonline.turma.models.Turma import Turma, AlunoTurma
from provasonline.prova.models.Prova import Prova, AlunoProva
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user

aluno = Blueprint('aluno', __name__, template_folder='templates')

@aluno.route("/listar_alunos", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template("listar_alunos.html", alunos = alunos)

@aluno.route("/ver_aluno/<_id>", methods=["GET","POST"])
@login_required()
def ver_aluno(_id):
    aluno = Aluno.query.get_or_404(_id)

    provas = (Aluno.query.join(AlunoProva, Aluno.id == AlunoProva.aluno_id)
                              .join(Prova, AlunoProva.prova_id == Prova.id)
                              .add_columns((Prova.id).label("prova_id"),
                                           (Prova.descricao).label("descricao"),
                                           (AlunoProva.nota).label("nota"))
                              .filter(Aluno.id == _id)).all()

    turmas = (Aluno.query.join(AlunoTurma, Aluno.id == AlunoTurma.aluno_id)
                              .join(Turma, AlunoTurma.turma_id == Turma.id)
                              .add_columns((Turma.id).label("turma_id"),
                                           (Turma.descricao).label("descricao"),
                                           (Turma.nome).label("turma_nome"))
                              .filter(Aluno.id == _id)).all()

    return render_template("ver_aluno.html", aluno = aluno, provas = provas, turmas = turmas)