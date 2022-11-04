import unittest
from provasonline.prova.controller import *
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