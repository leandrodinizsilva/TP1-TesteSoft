import re

def checkEmailRegex(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    result = False
    if(re.search(regex,email)):
        result = True
    else:
        result = False

    return result

def string_contem_somente_numeros(texto):
    listaTextos = texto.split()
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
    if (numero.lower() in ['true', '1', 't', 'y', 'yes']):
        return 1
    elif (numero.lower() in ['false', '0', 'f', 'n', 'no']):
        return 0

    return 1