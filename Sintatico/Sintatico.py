import pandas as pd

import sys
sys.path.append('Lexico')
sys.path.append('Semantico')

from Lexico import scanner, linhasEColunas, Tabela_Simbolos, possuiErroLexico
from Producao import producoes
from Semantico import invocar_semantico, gerarArquivo
import copy

linhas = 1
colunas = 1
possuiErroSintatico = False

action = pd.read_csv('Sintatico\Actions.csv')
goto = pd.read_csv('Sintatico\GoTo.csv')
arquivo = open('Teste_mgol\Teste_mgol', 'r').read()

possuiErros = False

def parser():
    tokenAnterior = None
    pilha = [0]
    pilha_semantica = []
    atributos = []
    s = pilha[-1]
    global possuiErroSintatico

    a = copy.deepcopy(scanner(arquivo))

    if(a is not None):
        
        while(True):
            
            s = pilha[-1]
            acaoAtual = action.at[s, a['classe']]

            if('s' == acaoAtual[0]):
                linhasSemantico, colunasSemantico = linhasEColunas()
                pilha.append(int(acaoAtual[1: len(acaoAtual)]))
                pilha_semantica.append(a)

                if(tokenAnterior is not None):
                    a = copy.deepcopy(tokenAnterior)
                    tokenAnterior = None
                    
                else:
                    a = copy.deepcopy(scanner(arquivo))
                    while (a is None) :
                        a = copy.deepcopy(scanner(arquivo))

            elif('r' == acaoAtual[0]):
                numeroDaRegra = int(acaoAtual[1: len(acaoAtual)])
                regra = producoes[numeroDaRegra].split('-> ')
                qtdaParaDesempilhar = len(regra[1].split(' '))

                if(regra[0] == "ARG"):

                    for item in pilha_semantica:
                        if(item["classe"] in ("lit", "id", "num")):
                            atributos.append(item)
                
                if(regra[0] == "OPRD"):

                    for item in pilha_semantica:
                        if(item["classe"] in ("id", "num")):
                            atributos.append(item)
                
                if(regra[0] == "ES"):
                    for item in pilha_semantica:
                        if(item["classe"] == "leia"):
                            for itemAtributo in pilha_semantica:
                                if(itemAtributo["classe"] == "id"):
                                    atributos.append(itemAtributo)

                if(regra[0] == "EXP_R"):
                    for aux in range(3):
                        indice = len(pilha_semantica) - 3 + aux
                        atributos.append(pilha_semantica[indice])

                if(regra[0] == "CAB"):
                    for item in pilha_semantica:
                        if(item["classe"] == "EXP_R"):
                                    atributos.append(item)
                
                if(regra[0] == "CABR"):
                    for item in pilha_semantica:
                        if(item["classe"] == "EXP_R"):
                                    atributos.append(item)
                
                if(regra[0] == "LD"):
                    for item in pilha_semantica:
                        if(item["classe"] == "OPRD"):
                            for itemAtributos in item["atributos"]:
                                atributos.append(itemAtributos)
                        elif(item["classe"] == "opm"):
                            atributos.append(item)

                if(regra[0] == "CMD"):
                    for item in pilha_semantica:
                        if(item["classe"] == "id"):
                            atributos.append(item)
                        elif(item["classe"] == "rcb"):
                            atributos.append(item)
                        elif(item["classe"] == "LD"):
                            atributos.append(item)

                for _ in range(qtdaParaDesempilhar):
                    pilha.pop()
                    pilha_semantica.pop()

                t = pilha[-1]
                gotoAtual = int(goto.at[t, regra[0]])
                pilha.append(gotoAtual)
                pilha_semantica.append({"classe": regra[0], "lexema": regra[0], "tipo": None})
                
                print(producoes[numeroDaRegra])
                invocar_semantico(pilha_semantica, numeroDaRegra, Tabela_Simbolos, atributos, linhasSemantico, colunasSemantico)

                if(numeroDaRegra in (12, 13, 18, 19, 21, 22, 25, 33, 26)):
                    atributos = []

            elif ('acc' in acaoAtual):
                gerarArquivo(possuiErroLexico, possuiErroSintatico)
                break

            else:
                tokenAnterior =  copy.deepcopy(a)
                linhas, colunas = linhasEColunas()
                possuiErroSintatico = True
                if('erroPT_V' == acaoAtual):
                    print("ERRO sintático – ; esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'pt_v'
                
                elif('erroPT_VouFC_P' == acaoAtual):
                    print("ERRO sintático – ; ou ) esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'fc_p'
                elif('erroInicio' == acaoAtual):
                    print("ERRO sintático – inicio esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'inicio'
                elif('erroVarinicio' == acaoAtual):
                    print("ERRO sintático – varinicio esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'varinicio'
                elif('erroVarfim' == acaoAtual):
                    print("ERRO sintático – varfim esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'varfim'
                
                elif('erroEscreva' == acaoAtual):
                    print("ERRO sintático – escreva esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'lit'
                elif('erroId' == acaoAtual):
                    print("ERRO sintático – id esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'id'
                elif('erroSe' == acaoAtual):
                    print("ERRO sintático – se esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'se'
                elif('erroAB_P' == acaoAtual):
                    print("ERRO sintático – ( esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'ab_p'
                elif('erroFc_p' == acaoAtual):
                    print("ERRO sintático – ) esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'fc_p'
                elif('erroOPR' == acaoAtual):
                    print("ERRO sintático – operador relacional ou matemático esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'opr'
                elif('erroNUMID' == acaoAtual):
                    print("ERRO sintático – id ou constante numérica esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'num'
                elif('erroExpressao' == acaoAtual):
                    print("ERRO sintático – id ou expressão condicional esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'id'
                elif('erroEntao' == acaoAtual):
                    print("ERRO sintático – então esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'então'
                elif('erroFimse' == acaoAtual):
                    print("ERRO sintático – fimse esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'fimse'
                elif('erroSimboloAtribuicao' == acaoAtual):
                    print("ERRO sintático – - esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'rcb'
                elif('erroAtribuicao' == acaoAtual):
                    print("ERRO sintático – id ou número esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'id'
                elif('erroFimrepita' == acaoAtual):
                    print("ERRO sintático – fimrepita esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'fimrepita'
                elif('erroIdString' == acaoAtual):
                    print("ERRO sintático – id ou string esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'id'
                elif('erroFim' == acaoAtual):
                    print("ERRO sintático – fim esperado antes de EOF. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'fim'
                elif('erroVir' == acaoAtual):
                    print("ERRO sintático – , esperado antes de %s. Linha %s, coluna %d" % (a['lexema'], linhas, colunas - len(a['lexema'])))
                    a['classe'] = 'vir'
                else:
                    print("ERRO sintático – token %s inesperado. Linha %s, coluna %d" % (a['lexema'], linhas, (colunas - len(a['lexema']))))
                    
                    while('erro' == acaoAtual):
                        a = scanner(arquivo)
                        while (a is None) :
                            a = scanner(arquivo)
                        acaoAtual = action.at[s, a['classe']]
    else:
            a = copy.deepcopy(scanner(arquivo))
            while (a is None) :
                a = copy.deepcopy(scanner(arquivo))

parser()
