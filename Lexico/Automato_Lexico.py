from Tabela_Simbolos import *

letra_alfabeto   =   tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
digito_alfabeto  =   tuple("0123456789")
operadores_alfabeto = tuple("+-*/")
espacos          =    tuple("\t\n\r\f\v ")
underline =  tuple("_")
identificador = (letra_alfabeto + digito_alfabeto + underline)
alfabeto_geral = (letra_alfabeto + digito_alfabeto + operadores_alfabeto + espacos)

automato_finito_deterministico = {
    0: {espacos: 0,
        digito_alfabeto: 1,
        "\"": 7,
        letra_alfabeto: 9,
        "{": 10,
        "eof": 12,
        ";": 13,
        operadores_alfabeto: 14,
        ",": 15,
        "(": 16,
        ")": 17,
        "=": 20,
        ">": 21,
        "<": 23
    },
    1: {
        "\.": 2,
        "Ee": 4,
        digito_alfabeto: 1
    },
    2: {
        digito_alfabeto: 3,
    },
    3: {
        digito_alfabeto: 3,
        "Ee": 4
    },
    4: {
        "+-": 6,
        digito_alfabeto: 5
    },
    5: {
        digito_alfabeto: 5
    },
    6: {
        digito_alfabeto: 5
    },
    7: {
        alfabeto_geral: 7,
        "\"": 8
    },
    8: {

    },
    9: {
        identificador: 9
    },
    10: {
        alfabeto_geral: 10,
        "}": 11
    },
    11: {

    },
    12: {

    },
    13: {

    },
    14: {

    },
    15: {

    },
    16: {

    },
    17: {

    },
    18: {

    },
    20: {

    },
    21: {
        "=": 22
    },
    23: {
        ">": 25,
        "=": 24,
        "-": 18,
    },
    24: {

    },
    25: {

    },
}

Estados_Finais = {
    1: "num",
    3: "num",
    5: "num",
    8: "lit",
    9: "id",
    11: "comentario",
    12: "eof",
    14: "opm",
    13: "pt_v",
    15: "vir",
    16: "ab_p",
    17: "fc_p",
    18: "rcb",
    20: "opr",
    21: "opr",
    22: "opr",
    23: "opr",
    24: "opr", 
    25: "opr"
}

def buscaEstado (caractere, estadoAnterior):
    estado = 0

    for chave in automato_finito_deterministico[estadoAnterior].keys():

        if(caractere in chave):
            estado = automato_finito_deterministico[estadoAnterior][chave]
            return estado

    return ""
    

    