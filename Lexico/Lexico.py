from Automato_Lexico import *
from Tabela_Simbolos import *

posicaoArquivo = 0
tamanhoDoArquivo = 0
linhas = 1
colunas = 1
mensagemErro = None
linhaErro = 0
colunaErro = 0
possuiErroLexico = False

def buscaToken(lexema):
    for chave in Tabela_Simbolos.keys():
        if(lexema == chave):
            return Tabela_Simbolos[chave]

    return None
        
def criarToken(estado, lexema):
    novoToken = {
        'classe': Estados_Finais[estado],
        'lexema': lexema,
        'tipo'  : None,
    }

    if(estado == 8):
        novoToken['tipo'] = 'literal'
    if(estado == 1):
        novoToken['tipo'] = 'inteiro'
    if(estado == 3):
        novoToken['tipo'] = 'real'
    
    if(novoToken['classe'] == 'id'):
        Tabela_Simbolos[lexema] = (novoToken)

    if(novoToken['classe'] == 'comentario'):
        return None
    return novoToken

def criarTokenERRO(lexema):
    novoToken = {
        'classe': "ERRO",
        'lexema': lexema,
        'tipo'  : None,
    }
    possuiErroLexico = True
    Tabela_Simbolos[lexema] = (novoToken)
    return novoToken
        
def scanner(arquivo):
    global posicaoArquivo
    global colunas
    global linhas
    global mensagemErro
    global linhaErro
    global colunaErro
    global possuiErroLexico
    lexema = ""
    estado = 0
    estadoAnterior = 0
    
    if(posicaoArquivo == len(arquivo)):
        arquivo == "eof"
        estado = buscaEstado("eof", estado)
        lexema = "eof"

        if(estado in Estados_Finais.keys()):
            token = buscaToken(lexema)
                    
            if (token is None):
                token = criarToken(estado, lexema)
            return token

    while(posicaoArquivo <= len(arquivo)):

        if(posicaoArquivo != len(arquivo)):

            caractere = arquivo[posicaoArquivo] 

            estadoAnterior = estado

            estado = buscaEstado(caractere, estado)

            if(estadoAnterior == 0 and estado == ""):
                mensagemErro = "ERRO léxico – Caractere inválido na linguagem. Linha %s, coluna %d" % (linhas, colunas)
                token = criarTokenERRO(caractere)
                lexema = ""
                posicaoArquivo = posicaoArquivo + 1
                colunas = colunas + 1
                if(token['classe'] == "ERRO"):
                    print(mensagemErro)
                    mensagemErro = None
                    linhaErro = 0
                    colunaErro = 0
                return None

            if((estadoAnterior == 10 and estado != 11) or (estadoAnterior == 7 and estado != 8)):
                if(linhaErro == 0): linhaErro = linhas
                if(colunaErro == 0): colunaErro = colunas
                estado = estadoAnterior
                lexema = lexema + caractere
                posicaoArquivo = posicaoArquivo + 1
                colunas = colunas + 1
                if(caractere == "\n"):
                    linhas = linhas + 1
                    colunas = -1
                continue

        else:
            
            if(estadoAnterior == 10 and "{" in lexema):

                mensagemErro = "ERRO léxico – A { não foi fechada. Linha %s, coluna %d" % (linhaErro, colunaErro)
                token = criarTokenERRO(lexema)
                if(token['classe'] == "ERRO"):
                    print(mensagemErro)
                    mensagemErro = None
                    linhaErro = 0
                    colunaErro = 0
                return None
            
            if(estadoAnterior == 7 and "\"" in lexema):
                mensagemErro = "ERRO léxico – A \" não foi fechada. Linha %s, coluna %d" % (linhaErro, colunaErro)
                token = criarTokenERRO(lexema)
                if(token['classe'] == "ERRO"):
                    print(mensagemErro)
                    mensagemErro = None
                    linhaErro = 0
                    colunaErro = -1
                return None
            
            estadoAnterior = estado
            estado = ""

        if(estado == "" and estadoAnterior in Estados_Finais.keys()):
            estado = estadoAnterior
                
            if(estado  in Estados_Finais.keys()):
                token = buscaToken(lexema)
                    
                if (token is None):
                    token = criarToken(estado, lexema)
                return token 
                    
        if(caractere in espacos and estado == 0):
                if(caractere == "\n"):
                    linhas = linhas + 1
                    colunas = -1
                colunas = colunas + 1
                posicaoArquivo = posicaoArquivo + 1
                return None
            
        lexema = lexema + caractere
        colunas = colunas + 1
        posicaoArquivo = posicaoArquivo + 1

def linhasEColunas():
    return linhas, colunas
