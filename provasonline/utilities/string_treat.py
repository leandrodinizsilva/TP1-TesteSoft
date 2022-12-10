import re


class NonStringArgument(Exception):
    def __init__(self, value):
        self.parameter = value
    
    def __str__(self):
        return repr(self.parameter)


def checkEmailRegex(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    result = False
    try:
        if(re.search(regex,email)):
            result = True
        else:
            result = False
    except TypeError:
        raise TypeError

    return result

def string_contem_somente_numeros(texto):
    listaTextos = []
    try:
        listaTextos = texto.split()
    
    except AttributeError:
        raise AttributeError

    result = False
    qtdStrings = len(listaTextos)
    
    somenteNumeros = 0
    for texto in (listaTextos):
        if texto.isnumeric():
            somenteNumeros = somenteNumeros + 1

    if qtdStrings == somenteNumeros:
        result = True

    return result

def transforma_um_e_zero_em_bool(numero):
    if not isinstance(numero, str): raise NonStringArgument("Parâmetro não é uma string")

    if (numero.lower() in ['true', '1', 't', 'y', 'yes']):
        return 1
    elif (numero.lower() in ['false', '0', 'f', 'n', 'no']):
        return 0

    return 1