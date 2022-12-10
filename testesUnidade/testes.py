import unittest
from provasonline.prova.controller import *
from provasonline.turma.controller import *
from provasonline.utilities.string_treat import *
from provasonline.usuario.models.Usuario import *

import datetime

class CadastrarProvas(unittest.TestCase):
    def testChecaDataEstaNoFuturo(self):
        dataPassado = datetime.datetime(2013, 1, 1)
        dataAVerificar = datetime.datetime(2018, 6, 1)
        comparacao = data_no_futuro(dataAVerificar, dataPassado)
        self.assertTrue(comparacao)

    def testChecaDataEstaNoPassado(self):
        dataPassado = datetime.datetime(2018, 1, 1)
        dataAVerificar = datetime.datetime(2013, 6, 1)
        comparacao = data_no_futuro(dataAVerificar, dataPassado)
        self.assertFalse(comparacao)

    def testSelecionaAlternativa3ComoCorreta(self):
        coreta = 3
        alternativa1 = Opcao('TextoA', False, 1)
        alternativa2 = Opcao('TextoB', False, 1)
        alternativa3 = Opcao('TextoC', False, 1)
        alternativa4 = Opcao('TextoD', False, 1)
        seleciona_alternativa_correta(alternativa1, alternativa2, alternativa3, alternativa4, coreta)
        self.assertFalse(alternativa1.correta)
        self.assertFalse(alternativa2.correta)
        self.assertTrue(alternativa3.correta)
        self.assertFalse(alternativa4.correta)

    def testAcertouPergunta(self):
        resposta1 = Resposta(1, 1, 1,1,1)
        self.assertTrue(corrige_questao(resposta1))

    def testErrouPergunta(self):
        resposta1 = Resposta(1, 1, 1, 0, 1)
        self.assertFalse(corrige_questao(resposta1))

    def testRemoveEspacosBrancosTexto(self):
        texto1 = " Matéria até o capitulo 2    "
        texto1 = remove_espacos_texto(texto1)
        self.assertEqual("Matéria até o capitulo 2", texto1)

    def testRemoveEspacosBrancosTextoEmStringsSoComEspacos(self):
        texto1 = "           "
        texto1 = remove_espacos_texto(texto1)
        self.assertEqual("", texto1)

    def testSortProvasPelasMelhoresNotas(self):
        prova1 = AlunoProva(1,1,8)
        prova2 = AlunoProva(1,2,7)
        prova3 = AlunoProva(1,3,9)
        prova4 = AlunoProva(1,4,3)
        provasOrdenadas = [prova3, prova1, prova2, prova4]
        provas = [prova1, prova2, prova3, prova4]
        provas = melhores_notas(provas)
        self.assertEqual(provas, provasOrdenadas)

    def testSortProvasPelasMelhoresERemoveProvasZeradas(self):
        prova1 = AlunoProva(1,1,0)
        prova2 = AlunoProva(1,2,7)
        prova3 = AlunoProva(1,3,9)
        prova4 = AlunoProva(1,4,3)
        provasOrdenadas = [prova3, prova2, prova4]
        provas = [prova1, prova2, prova3, prova4]
        provas = melhores_notas(provas)
        self.assertEqual(provas, provasOrdenadas)

    def testSomenteProvasQueZerei(self):
        prova1 = AlunoProva(1,1,0)
        prova2 = AlunoProva(1,2,7)
        prova3 = AlunoProva(1,3,0)
        prova4 = AlunoProva(1,4,3)
        provasZeradas = [prova1, prova3]
        provas = [prova1, prova2, prova3, prova4]
        provas = provas_que_zerei(provas)
        self.assertEqual(provas, provasZeradas)

    def testNenhumaProvaZerada(self):
        prova1 = AlunoProva(1,1,10)
        prova2 = AlunoProva(1,2,7)
        prova3 = AlunoProva(1,3,10)
        prova4 = AlunoProva(1,4,3)
        provasZeradas = []
        provas = [prova1, prova2, prova3, prova4]
        provas = provas_que_zerei(provas)
        self.assertEqual(provas, provasZeradas)

    def testRegraDe3NumeroParaPorcentagem(self):
        parcial = 5
        total = 10
        resultado = nota_para_porcentagem(total, parcial)
        self.assertEqual(resultado, 50.0)

    def testAdicionarPorcentagemAoNumero(self):
        numero = 50.0
        resultado = formatar_para_porcentagem(numero)
        self.assertEqual(resultado, '50.0%')

    def testAdicionarPercentualComPorcentagemAProva(self):
        provas = [Prova(1,1,10,1,1,0,0), Prova(1,1,10,1,1,0,0)]
        provas[0].valor = 10
        provas[0].nota = 5
        provas[1].valor = 10
        provas[1].nota = 8
        percentuais = adicionar_percentual(provas)
        comparar = ['50.0%', '80.0%']
        self.assertEqual(percentuais, comparar)

    def testProvaEntregueAtrasada(self):
        result = prova_entrega_atrasada('2022/11/05','2022/11/06')
        self.assertTrue(result)

    def testProvaEntregueSemAtraso(self):
        result = prova_entrega_atrasada('2022/11/05','2022/11/01')
        self.assertFalse(result)

    def testEntregueNoMesmoDia(self): # Edge case, deveria considerar como futuro.
        result = prova_entrega_atrasada('2022/11/05','2022/11/05')
        self.assertFalse(result)

    def testNotaParaPorcentagemThrowZeroDivisionException(self):
        self.assertRaises(ZeroDivisionError, nota_para_porcentagem, total=0, parcial=4)

    def testNotaParaPorcentagemThrowTypeErrorException(self):
        self.assertRaises(TypeError, nota_para_porcentagem, total="teste", parcial=4)

    def testProvaEntregueAtrasadaThrowTypeErrorException(self):
        self.assertRaises(TypeError, prova_entrega_atrasada, '2022/11/05', 20221106)

    def testFormatarParaPorcentagemThrowPorcentagemNegativaException(self):
        self.assertRaises(PorcentagemNegativa, formatar_para_porcentagem, -50)

    ## Implementação de atribuição de conceitos numa sprint futura do sistema
    def testPassouNaProva(self):
        parcial = 8
        total = 10
        result = nota_para_porcentagem(total, parcial)
        self.assertTrue(result >= 60.0)

    def testNaoPassouNaProva(self):
        parcial = 4
        total = 10
        result = nota_para_porcentagem(total, parcial)
        self.assertFalse(result >= 60.0)

    def testDireitoAoExameEspecial(self):
        parcial = 4
        total = 10
        result = nota_para_porcentagem(total, parcial)
        self.assertTrue(result >= 40.0)

    def testSemDireitoAoExameEspecial(self):
        parcial = 3
        total = 10
        result = nota_para_porcentagem(total, parcial)
        self.assertFalse(result >= 40.0)

    #####
    

class UtilidadesString(unittest.TestCase):
    def testStringContemSomenteNumeros(self):
        valor = string_contem_somente_numeros('123123123')
        self.assertTrue(valor)

    def testStringContemSomenteNumerosComEspacoNoMeio(self):
        valor = string_contem_somente_numeros('123 123 123 8798')
        self.assertTrue(valor)

    def testStringNaoContemSomenteNumeros(self):
        valor = string_contem_somente_numeros('1231letra23123')
        self.assertFalse(valor)

    def testStringNaoContemSomenteNumerosComEspacosNoMeio(self):
        valor = string_contem_somente_numeros('123 123 teste 123 tes12')
        self.assertFalse(valor)
    
    def testStringContemSomenteNumeroThrowTypeErrorException(self):
        self.assertRaises(AttributeError, string_contem_somente_numeros, 2222222) #Not a string parameter

    def testEmailValido(self):
        email = 'teste@gmail.com'
        self.assertTrue(checkEmailRegex(email))

    def testEmailNaoValidoSemArroba(self):
        email = 'testegmail.com'
        self.assertFalse(checkEmailRegex(email))

    def testEmailNaoValidoEspacoVazio(self):
        email = ' testegmail.com'
        self.assertFalse(checkEmailRegex(email))
    
    def testEmailNaoValidoIniciaComCaracterEspecial(self):
        email = '#testegmail.com'
        self.assertFalse(checkEmailRegex(email))

    def testCheckEmailRegexThrowTypeErrorException(self):
        self.assertRaises(TypeError, checkEmailRegex, 22)
    

    def testTranformaSimEmBool(self):
        string_yes1 = '1'
        string_yes2 = 'True'
        string_yes3 = 'yes'
        teste1 = transforma_um_e_zero_em_bool(string_yes1)
        teste2 = transforma_um_e_zero_em_bool(string_yes2)
        teste3 = transforma_um_e_zero_em_bool(string_yes3)
        self.assertTrue(teste1)
        self.assertTrue(teste2)
        self.assertTrue(teste3)

    def testTranformaNaoEmBool(self):
        string_no1 = '0'
        string_no2 = 'False'
        string_no3 = 'no'
        teste1 = transforma_um_e_zero_em_bool(string_no1)
        teste2 = transforma_um_e_zero_em_bool(string_no2)
        teste3 = transforma_um_e_zero_em_bool(string_no3)
        self.assertFalse(teste1)
        self.assertFalse(teste2)
        self.assertFalse(teste3)

    def testTransformaCaracterEspecialEmBool(self):
        especial_1 = '_'
        especial_2 = '#'
        teste1 = transforma_um_e_zero_em_bool(especial_1)
        teste2 = transforma_um_e_zero_em_bool(especial_2)
        self.assertTrue(teste1)
        self.assertTrue(teste2)

    def testTransformaUmEZeroEmBoolThrowTypeErrorException(self):
        self.assertRaises(NonStringArgument, transforma_um_e_zero_em_bool, 22) # Not a string parameter

class FuncoesDeUsuario(unittest.TestCase):
    def testContrutorEncriptaSenha(self):
        senhaUsada = '123123'
        usuario = Usuario('teste1', senhaUsada, 'teste', '1')
        resultado = usuario.bcrypt.check_password_hash(usuario.senha, senhaUsada)
        self.assertTrue(resultado)

    def testSetSenhaMudaSenhaEEncripta(self):
        senhaUsada = '123123'
        usuario = Usuario('teste1', senhaUsada, 'teste', '1')
        novaSenha = '321321'
        usuario.setSenha(novaSenha)
        resultado = usuario.bcrypt.check_password_hash(usuario.senha, novaSenha)
        self.assertTrue(resultado)

    def testChangeUsername(self):
        usuario = Usuario(nome="Nome1", login="login1", senha="123", urole="aluno")
        usuario.mudarNome("Nome2")
        self.assertEqual("Nome2", usuario.nome)

    def testChangeUsernameComStringVazia(self):
        usuario = Usuario(nome="Nome1", login="login1", senha="123", urole="aluno")
        usuario.mudarNome("")
        self.assertEqual("Nome1", usuario.nome)


## Testes de "Turma"
class TestesTurma(unittest.TestCase):
    def testNumeroDeTurmasDeUmAluno(self):
        provas_do_aluno = [Prova(1,1,10,1,1,0,0), Prova(1,1,10,0,1,0,0), Prova(1,1,10,2,2,0,0), Prova(1,1,10,0,0,0,0)]
        result = quantidadeDeTurmasDoAluno(provas_do_aluno)
        self.assertEqual(result, 3)

    def testAlunoEstaMatriculadoEmMaisDeUmaTurma(self):
        provas_do_aluno = [Prova(1,1,10,1,1,0,0), Prova(1,1,10,0,1,0,0), Prova(1,1,10,2,2,0,0), Prova(1,1,10,0,0,0,0)]
        result = quantidadeDeTurmasDoAluno(provas_do_aluno)
        self.assertTrue(result > 1)

    def testQuantidadeDeProfessoresCadastrados(self):
        turmas = [Turma(descricao="Desc 1", nome="Turma 1", id_professor=0), Turma(descricao="Desc 2", nome="Turma 2", id_professor=1), Turma(descricao="Desc 3", nome="Turma 3", id_professor=0)]
        result = quantidadeDeProfessoresCadastrados(turmas)
        self.assertEqual(result, 2)

    def testTodasTurmasPossuemDescricao(self):
        turmas = [Turma(descricao="Desc 1", nome="Turma 1", id_professor=0), Turma(descricao="Desc 2", nome="Turma 2", id_professor=1), Turma(descricao="Desc 3", nome="Turma 3", id_professor=0)]
        result = turmasPossuemDescricao(turmas)
        self.assertTrue(result)

    def testNemTodasAsTurmasPossuemDescricao(self):
        turmas = [Turma(nome="Turma 1", id_professor=0), Turma(nome="Turma 2", id_professor=1), Turma(nome="Turma 3", id_professor=0)]
        result = turmasPossuemDescricao(turmas)
        self.assertFalse(result)

    def testExisteTurmaComMaisDeUmAluno(self):
        alunos_turma = [AlunoTurma(0, 0), AlunoTurma(0, 1), AlunoTurma(0, 2),
                        AlunoTurma(1, 0), AlunoTurma(0, 3), AlunoTurma(0, 4),
                        AlunoTurma(2, 0), AlunoTurma(2, 4), AlunoTurma(0, 5),]

        result = existeTurmaComMaisDeUmAluno(alunos_turma)
        self.assertTrue(result)

    def testNaoExisteTurmaComMaisDeUmAluno(self):
        alunos_turma = [AlunoTurma(0, 0), AlunoTurma(0, 1), AlunoTurma(0, 2),
                        AlunoTurma(1, 3), AlunoTurma(0, 5), AlunoTurma(0, 6),
                        AlunoTurma(2, 7), AlunoTurma(2, 8), AlunoTurma(0, 9),]

        result = existeTurmaComMaisDeUmAluno(alunos_turma)
        self.assertFalse(result)
        
    #def teste1(self):
    #    parcial = 5
    #    resultado = nota_para_porcentagem("teste", parcial)
    #    self.assertEqual(resultado, 50.0)