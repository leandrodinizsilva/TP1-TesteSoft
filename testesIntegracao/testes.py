import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from sqlalchemy import text
from provasonline import db



class TesteIntegracao(unittest.TestCase):
    def setUp(self):
        self.truncateDB()
        self.driver = webdriver.Firefox(executable_path='geckodriver.exe')
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")

    @classmethod
    def setUpClass(self):
        self.truncateDB(self)

    def truncateDB(self):
        sql = text('SET FOREIGN_KEY_CHECKS = 0')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `aluno`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `aluno_na_turma`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `aluno_prova`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `opcao`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `pergunta`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `professor`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `prova`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `resposta`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `turma`')
        result = db.engine.execute(sql)
        sql = text('TRUNCATE `usuario`')
        result = db.engine.execute(sql)

        sql = text('SET FOREIGN_KEY_CHECKS = 1')
        result = db.engine.execute(sql)


    def cadastrarUsuarioAluno(self):
        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-cadastrar').click()
        time.sleep(1)

        self.driver.find_element(By.ID, 'nome').send_keys("Aluno1")
        self.driver.find_element(By.ID, 'login').send_keys("Aluno1")
        self.driver.find_element(By.ID, 'senha').send_keys("123123")
        self.driver.find_element(By.ID, 'submit').click()
        time.sleep(1)
        e = self.driver.find_element(By.CLASS_NAME, 'message')
        msgSuccess = e.get_attribute('innerHTML')
        time.sleep(1)

        return msgSuccess

    def testCadastrarUsuarioAluno(self):
        msgSuccess = self.cadastrarUsuarioAluno()
        self.driver.close()
        self.assertEqual(msgSuccess, "Usuario cadastrado com sucesso!")

    def cadastrarUsuarioProfessor(self):
        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-cadastrar').click()
        time.sleep(1)

        self.driver.find_element(By.ID, 'nome').send_keys("Professor1")
        self.driver.find_element(By.ID, 'login').send_keys("Professor1")
        self.driver.find_element(By.ID, 'senha').send_keys("123123")
        select = Select(self.driver.find_element(By.ID, 'urole'))

        # select by value 
        select.select_by_value('professor')

        self.driver.find_element(By.ID, 'submit').click()
        time.sleep(1)
        e = self.driver.find_element(By.CLASS_NAME, 'message')
        msgSuccess = e.get_attribute('innerHTML')
        time.sleep(1)

        return msgSuccess

    def testCadastrarUsuarioProfessor(self):
        msgSuccess = self.cadastrarUsuarioProfessor()
        self.driver.close()
        self.assertEqual(msgSuccess, "Usuario cadastrado com sucesso!")

    def loginAluno(self):
        time.sleep(1)
        self.driver.find_element(By.ID, 'login').send_keys("Aluno1")
        self.driver.find_element(By.ID, 'senha').send_keys("123123")
        self.driver.find_element(By.ID, 'btn-login').click()
        time.sleep(1)

    def loginProfessor(self):
        time.sleep(1)
        self.driver.find_element(By.ID, 'login').send_keys("Professor1")
        self.driver.find_element(By.ID, 'senha').send_keys("123123")
        self.driver.find_element(By.ID, 'btn-login').click()
        time.sleep(1)

    def cadastrarTurma(self):
        self.cadastrarUsuarioProfessor()
        self.loginProfessor()

        self.driver.find_element(By.ID, 'nav-turmas').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-add-turma').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'nome').send_keys("Turma 1")
        self.driver.find_element(By.ID, 'descricao').send_keys("Essa turma tem aula")
        self.driver.find_element(By.ID, 'btn-add-turma').click()

        time.sleep(1)

    def cadastrarProva(self):
        self.cadastrarTurma()

        self.driver.find_element(By.ID, 'nav-provas').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-add-prova').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'prova').send_keys("Prova 1")

        select = Select(self.driver.find_element(By.ID, 'turma'))
        select.select_by_visible_text('Turma 1 - Essa turma tem aula')

        self.driver.find_element(By.ID, 'data').send_keys("2022-10-10")

        select = Select(self.driver.find_element(By.ID, 'temporizada'))
        select.select_by_value('0')

        self.driver.find_element(By.ID, 'tempo').send_keys("2022-10-10")

        self.driver.find_element(By.NAME, 'pergunta0').send_keys("A resposta é B")
        self.driver.find_element(By.NAME, 'valor0').send_keys("10")

        self.driver.find_element(By.NAME, 'opcao01').send_keys("Errada")
        self.driver.find_element(By.NAME, 'opcao02').send_keys("Certa")
        self.driver.find_element(By.NAME, 'opcao03').send_keys("Errada!")
        self.driver.find_element(By.NAME, 'opcao04').send_keys("Errada!!")
        self.driver.find_element(By.ID, 'radio2').click()

        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-add-prova-2').click()
        time.sleep(1)

        e = self.driver.find_element(By.CLASS_NAME, 'message')
        msgSuccess = e.get_attribute('innerHTML')

        return msgSuccess

    def testCadastrarProva(self):
        msgSuccess = self.cadastrarProva()
        self.driver.close()
        self.assertEqual(msgSuccess, "Prova cadastrada com sucesso")

    def adicionarAlunoNaTurma(self):
        self.cadastrarUsuarioAluno()
        self.cadastrarProva()
        self.driver.find_element(By.ID, 'nav-turmas').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'turma1').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'btn-gerenciar-alunos').click()
        time.sleep(3)
        self.driver.find_element(By.ID, 'check-aluno1').click()
        self.driver.find_element(By.ID, 'btn-add-aluno-turma').click()
        time.sleep(1)
        e = self.driver.find_element(By.CLASS_NAME, 'message')
        msgSuccess = e.get_attribute('innerHTML')

        return msgSuccess

    def testAdicionarAlunoNaTurma(self):
        msgSuccess = self.adicionarAlunoNaTurma()
        self.driver.close()
        self.assertAlmostEqual(msgSuccess, "Turma editada com sucesso")


    def testFazerProva(self):
        msg1 = self.adicionarAlunoNaTurma()
        self.driver.find_element(By.ID, 'nav-logout').click()
        self.loginAluno()
        self.driver.find_element(By.ID, 'nav-provas').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'responder-prova1').click()
        time.sleep(3)
        self.driver.find_element(By.ID, 'resposta1-2').click()
        self.driver.find_element(By.ID, 'btn-submit-resposta').click()
        e = self.driver.find_element(By.CLASS_NAME, 'message')
        msgSuccess = e.get_attribute('innerHTML')
        self.assertEqual(msgSuccess, "Prova respondida com sucesso!")
        self.driver.close()