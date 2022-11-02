import unittest
from provasonline.prova.controller import nome

class Testing(unittest.TestCase):
    def test_nome(self):
        teste = nome()
        self.assertEqual("leandro122212", teste)

    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)