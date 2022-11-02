from provasonline import db, login_required
from provasonline.prova.models.Prova import Opcao, Pergunta, Prova, Resposta, AlunoProva
from provasonline.turma.models.Turma import Turma, AlunoTurma
from provasonline.aluno.models.Aluno import Aluno
from provasonline.professor.models.Professor import Professor
from provasonline.constants import usuario_urole_roles
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user
from datetime import datetime, date

prova = Blueprint('prova', __name__, template_folder='templates')

@prova.route("/cadastrar_prova", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def cadastrar_prova():
    valor_total = 0

    if request.method == 'POST':

        descricao = request.form['prova']
        data      = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        turma     = request.form['turma']

        prova     = Prova(data, descricao, 0, current_user.id, turma)
        db.session.add(prova)
        db.session.commit()

        numero_de_perguntas = request.form['numero_de_perguntas']

        contador = 0

        while (contador < int(numero_de_perguntas)):    
            pergunta = request.form['pergunta'+str(contador)] 
            valor    = request.form['valor'+str(contador)] 

            valor_total = valor_total + int(valor)
            
            questao = Pergunta(pergunta, prova.id, valor)
            db.session.add(questao)    
            db.session.commit()

            opcao1   = request.form['opcao'+str(contador)+'1']
            opcao2   = request.form['opcao'+str(contador)+'2']
            opcao3   = request.form['opcao'+str(contador)+'3']
            opcao4   = request.form['opcao'+str(contador)+'4']   

            correta  = int(request.form['correta'+str(contador)])
            
            alternativa1 = Opcao(opcao1, False, questao.id)
            alternativa2 = Opcao(opcao2, False, questao.id)
            alternativa3 = Opcao(opcao3, False, questao.id)
            alternativa4 = Opcao(opcao4, False, questao.id)

            if (correta == 1):
                alternativa1.correta = True
            elif (correta == 2):
                alternativa2.correta = True
            elif (correta == 3):
                alternativa3.correta = True
            else:        
                alternativa4.correta = True

            db.session.add(alternativa1)
            db.session.add(alternativa2)
            db.session.add(alternativa3)
            db.session.add(alternativa4)                   

            contador = contador + 1    

        prova.valor = valor_total
        
        db.session.commit() 
        flash("Prova cadastrada com sucesso")
        return redirect(url_for('prova.listar_provas'))    

    turmas = Turma.query.filter(Turma.id_professor == current_user.id)
    return render_template("cadastrar_prova.html", turmas = turmas)

@prova.route("/ver_prova_correta/<_id>", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['PROFESSOR']])
def ver_prova_correta(_id):
    prova = Prova.query.get_or_404(_id)
    return render_template("ver_prova_correta.html", prova = prova)

@prova.route("/listar_provas", methods=["GET","POST"])
@login_required()
def listar_provas():
    provas = Prova.query.all()
    
    if current_user.urole == 'aluno':
        provas = (AlunoTurma.query.join(Turma, Turma.id == AlunoTurma.turma_id)
                                .join(Prova, Prova.turma == Turma.id)
                                .outerjoin(AlunoProva, Prova.id == AlunoProva.prova_id)
                                .add_columns((Prova.id).label("prova_id"),
                                            (Prova.descricao).label("descricao"),
                                            (Prova.data).label("data"),
                                            (Prova.valor).label("valor"),
                                            (AlunoProva.nota).label("nota"),
                                            (Turma.nome).label("turma"),
                                            (Turma.descricao).label("turma_descricao"))
                                .filter(AlunoTurma.aluno_id == current_user.id)).all() 
    else:
        provas = (Professor.query.join(Turma, Turma.id_professor == Professor.id)
                                .join(Prova, Prova.turma == Turma.id)
                                .add_columns((Prova.id).label("prova_id"),
                                            (Prova.descricao).label("descricao"),
                                            (Prova.data).label("data"),
                                            (Prova.valor).label("valor"),
                                            (Turma.nome).label("turma"),
                                            (Turma.descricao).label("turma_descricao"))
                                .filter(Professor.id == current_user.id)).all() 

    
    return render_template("listar_provas.html", provas = provas)

@prova.route("/responder_prova/<_id>", methods=["GET","POST"])
@login_required(role=[usuario_urole_roles['ALUNO']])
def responder_prova(_id):
    prova = Prova.query.get_or_404(_id)  
    turma = Turma.query.get_or_404(prova.turma)    

    if AlunoProva.query.filter(AlunoProva.prova_id == _id, AlunoProva.aluno_id == current_user.id).first():
        return redirect(url_for('prova.ver_correcao', id_prova = _id, id_aluno = current_user.id)) 

    if request.method == 'POST':
        nota = 0        
        for p in prova.perguntas: 
            opcao = request.form['op'+str(p.id)]
            
            aux = Opcao.query.get_or_404(opcao)

            if (aux.correta == 1):                
                resposta = Resposta(_id, p.id, opcao, 1, current_user.id) 
                nota = nota + p.valor
            else:
                resposta = Resposta(_id, p.id, opcao, 0, current_user.id)

            db.session.add(resposta)   
        
        aluno_prova = AlunoProva(current_user.id, _id, nota)
        db.session.add(aluno_prova)   

        db.session.commit()    

        flash("Prova respondida com sucesso!")
        return redirect(url_for('prova.prova_respondida', _id = _id))  

    return render_template("responder_prova.html", prova = prova, turma = turma)

@prova.route("/prova_respondida/<_id>", methods=["GET","POST"])
@login_required()
def prova_respondida(_id):
    # TODO: PEGAR RESPOSTA DA PROVA DO ALUNO E MOSTRAR NOTA E CORREÇÃO
    prova = Prova.query.get_or_404(_id)
    respostas = Resposta.query.filter(Resposta.prova == _id).all() # filtrar pelo aluno tb
    return render_template("prova_respondida.html", prova = prova, respostas = respostas)

@prova.route("/ver_correcao/<id_prova>/<id_aluno>", methods=["GET","POST"])
@login_required()
def ver_correcao(id_prova, id_aluno):
    prova = Prova.query.get_or_404(id_prova)
    turma = Turma.query.get_or_404(prova.turma) 
    respostas = Resposta.query.filter(Resposta.prova == id_prova, Resposta.aluno == id_aluno).all()
    nota = 0
    for resposta in respostas:
        if resposta.acertou:
            nota = nota + resposta.pergunta_obj.valor
    return render_template("ver_correcao.html", prova = prova, respostas = respostas, nota = nota, turma = turma)