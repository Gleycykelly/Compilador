

dadosParaArquivo = []
x = 0
variaveisTemporarias = []
possuiErroSemantico = False


def invocar_semantico(pilha_semantica, numeroDaRegra, Tabela_Simbolos, atributos, linhas, colunas):
    global x
    global variaveisTemporarias

    if(numeroDaRegra == 4):
        dadosParaArquivo.append('\n\n\n')      

    elif(numeroDaRegra == 7):
        jaExisteDeclaracao = True
        ehVirgula = False
        
        for tipo in pilha_semantica:
            if(tipo["lexema"] == "TIPO"):
                for chave in Tabela_Simbolos.keys():
                    if(Tabela_Simbolos[chave]["classe"] == "id" and Tabela_Simbolos[chave]["tipo"] is None):
                        jaExisteDeclaracao = False
                        encontrouNaPilha = False
                        Tabela_Simbolos[chave]["tipo"] = tipo["tipo"]
                        
                        for simbolo in pilha_semantica: 
                            if(simbolo["classe"] == "vir"):
                                ehVirgula = True
                            if(simbolo["lexema"] == Tabela_Simbolos[chave]["lexema"] and Tabela_Simbolos[chave]["classe"] == "id"):
                                encontrouNaPilha = True
                        if(ehVirgula and encontrouNaPilha):
                            dadosParaArquivo.append("{},".format(Tabela_Simbolos[chave]["lexema"]))
                            ehVirgula = False
                        else:
                            dadosParaArquivo.append("{};\n".format(Tabela_Simbolos[chave]["lexema"]))

                for item in pilha_semantica:
                    if(item["classe"] == "L"):
                        item["tipo"] = tipo["tipo"]

        if(jaExisteDeclaracao):
            possuiErroSemantico = True
            print("Erro: Variável já está declarada. Linha {}, coluna {}".format(linhas, colunas))


    elif(numeroDaRegra == 8):
        for chave in Tabela_Simbolos.keys():
            if("inteiro" in chave):
                pilha_semantica[-1]["tipo"] = Tabela_Simbolos[chave]["tipo"]
                dadosParaArquivo.append("int")
    
    elif(numeroDaRegra == 9):
        for chave in Tabela_Simbolos.keys():
            if("real" in chave):
                pilha_semantica[-1]["tipo"] = Tabela_Simbolos[chave]["tipo"]
                dadosParaArquivo.append("double")
    
    elif(numeroDaRegra == 10):
        for chave in Tabela_Simbolos.keys():
            if("literal" in chave):
                pilha_semantica[-1]["tipo"] = Tabela_Simbolos[chave]["tipo"]
                dadosParaArquivo.append("literal")
                break
    
    elif(numeroDaRegra == 12):
        temDeclaracao = False
        for simbolo in Tabela_Simbolos.values():
            if(simbolo["lexema"] == atributos[0]["lexema"]):
                temDeclaracao = True
                if(simbolo["tipo"] == "literal"):
                    dadosParaArquivo.append("scanf('%s', {});\n".format(simbolo["lexema"]))
                elif(simbolo["tipo"] == "inteiro"):
                    dadosParaArquivo.append("scanf('%d', &{});\n".format(simbolo["lexema"]))
                elif(simbolo["tipo"] == "real"):
                    dadosParaArquivo.append("scanf('%lf', &{});\n".format(simbolo["lexema"]))
        if(not temDeclaracao):
            possuiErroSemantico = True
            print("Erro: Variável não declarada. Linha {}, coluna {}".format(linhas, colunas))
            


    elif(numeroDaRegra == 13):
        dadosParaArquivo.append("printf({});\n".format(atributos[0]["lexema"]))
    
    elif(numeroDaRegra == 16):
        temDeclaracao = False

        for item in atributos:
            for simbolo in Tabela_Simbolos.values():
                if(simbolo["classe"] == "id" and simbolo["lexema"] == item["lexema"]):
                    temDeclaracao = True
            if(not temDeclaracao):
                possuiErroSemantico = True
                print("Erro: Variável não declarada. Linha {}, coluna {}".format(linhas, colunas))
            temDeclaracao = False
    
    elif(numeroDaRegra == 18):
        temDeclaracao = False
        for simbolo in Tabela_Simbolos.values():
            if(simbolo["lexema"] == atributos[0]["lexema"]):
                temDeclaracao = True
                if(atributos[0]["tipo"] == atributos[2]["tipo"]):
                    primeiro = next(aux for aux in atributos if aux["classe"] == "id")["lexema"]
                    segundo = next(aux for aux in atributos if aux["classe"] != "rcb" and aux["lexema"] != primeiro)["lexema"]

                    dadosParaArquivo.append("{} = {};\n".format(primeiro, segundo))

                else:
                    possuiErroSemantico = True
                    print("Erro: Tipos diferentes para atribuição. Linha {}, coluna {}".format(linhas, colunas))

        if(not temDeclaracao):
            possuiErroSemantico = True
            print("Erro: Variável não declarada. Linha {}, coluna {}".format(linhas, colunas))

    elif(numeroDaRegra == 19):
        temporaria = {}
        if(all(atributo["tipo"] != "literal" and (atributos[0]["tipo"] == atributo["tipo"] or atributo["classe"] == "opm") for atributo in atributos)):
            nomeVariavel = "T{}".format(x)
            x = x + 1
            temporaria[nomeVariavel] = next(x for x in atributos if x["classe"] == "id")["lexema"] + next(x for x in atributos if x["classe"] == "opm")["lexema"] + next(x for x in atributos if x["classe"] == "num")["lexema"]
            pilha_semantica[-1]["lexema"] = nomeVariavel
            pilha_semantica[-1]["tipo"] = atributos[3]["tipo"]
            dadosParaArquivo.append("{} = {};\n".format(nomeVariavel, temporaria[nomeVariavel]))
            variaveisTemporarias.append(temporaria)
        else:
            possuiErroSemantico = True
            print("Erro: Operadores com tipos incompatíveis. Linha {}, coluna {}".format(linhas, colunas))

    elif(numeroDaRegra == 21):
        temDeclaracao = False
        pilha_semantica[-1]["atributos"] = []

        for item in atributos:
            for simbolo in Tabela_Simbolos.values():
                if(simbolo["classe"] == "id" and simbolo["lexema"] == item["lexema"]):
                    temDeclaracao = True
                    pilha_semantica[-1]["atributos"].append(item)
            if(not temDeclaracao):
                possuiErroSemantico = True
                print("Erro: Variável não declarada. Linha {}, coluna {}".format(linhas, colunas))
            temDeclaracao = False

    elif(numeroDaRegra == 22):
        pilha_semantica[-1]["atributos"] = []
        for item in atributos:
            pilha_semantica[-1]["atributos"].append(item)

    elif(numeroDaRegra == 24):
        dadosParaArquivo.append("}\n")

    elif(numeroDaRegra == 25):
        dadosParaArquivo.append("if({}) {{\n".format(atributos[0]["lexema"]))

    elif(numeroDaRegra == 26):
        temporaria = {}
        if(atributos[0]["atributos"][0]["tipo"] == atributos[2]["atributos"][0]["tipo"]):
            nomeVariavel = "T{}".format(x)
            x = x + 1
            temporaria[nomeVariavel] = atributos[0]["atributos"][0]["lexema"] + atributos[1]["lexema"] + atributos[2]["atributos"][0]["lexema"]
            pilha_semantica[-1]["lexema"] = nomeVariavel
            dadosParaArquivo.append("{} = {}; \n".format(nomeVariavel, temporaria[nomeVariavel]))
            variaveisTemporarias.append(temporaria)
            
        else:
            possuiErroSemantico = True
            print("Erro: Operandos com tipos incompatíveis. Linha {}, coluna {}".format(linhas, colunas))

def gerarArquivo(possuiErroLexico, possuiErroSintatico):

    if(not possuiErroSemantico and not possuiErroLexico and not possuiErroSintatico):
        with open("PROGRAMA.C", 'w') as arquivo:
            arquivo.write("#include<stdio.h>\n")
            arquivo.write("typedef char literal[256];\n")
            arquivo.write("void main(void)\n")
            arquivo.write("{\n")
            identacao = "\t"
            for item in variaveisTemporarias:
                chave = list(item.keys())[0]
                arquivo.write("{}int {};".format(identacao, chave))
                arquivo.write("\n")

            for item in dadosParaArquivo:
                if("}" in item):
                    identacao = identacao.replace("\t\t", "\t")
                arquivo.write("{}{}".format(identacao, item))
                if("{" in item):
                    identacao = "{}\t".format(identacao)
                
    else:
        print("Foram identificados erros na análise do código, impedindo a geração do arquivo.")
    