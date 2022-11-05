import unittest
from provasonline.prova.controller import *
from provasonline.turma.controller import *
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
        provas = [Prova(1,1,10,1,1), Prova(1,1,10,1,1)]
        provas[0].valor = 10
        provas[0].nota = 5
        provas[1].valor = 10
        provas[1].nota = 8
        percentuais = adicionar_percentual(provas)
        comparar = ['50.0%', '80.0%']
        self.assertEqual(percentuais, comparar)

class CadastrarTurmas(unittest.TestCase):
    def testStringContemSomenteNumeros(self):
        valor = string_contem_somente_numeros('123123123')
        self.assertTrue(valor)
    
    def testStringNaoContemSomenteNumeros(self):
        valor = string_contem_somente_numeros('1231letra23123')
        self.assertFalse(valor)