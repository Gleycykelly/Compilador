

dadosParaArquivo = []
x = 0
variaveisTemporarias = []


def invocar_semantico(token, pilha_semantica, numeroDaRegra, Tabela_Simbolos, atributos):
    print(dadosParaArquivo)
    global x
    global variaveisTemporarias
    if(numeroDaRegra == 4):
        dadosParaArquivo.append('\n\n\n')      

    elif(numeroDaRegra == 7):
        for tipo in pilha_semantica:
            if(tipo["lexema"] == "TIPO"):
                for chave in Tabela_Simbolos.keys():
                    if(Tabela_Simbolos[chave]["classe"] == "id" and Tabela_Simbolos[chave]["tipo"] is None):
                        Tabela_Simbolos[chave]["tipo"] = tipo["tipo"]
                        dadosParaArquivo.append(Tabela_Simbolos[chave]["lexema"])
                for item in pilha_semantica:
                    if(item["classe"] == "L"):
                        item["tipo"] = tipo["tipo"]

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
        for chave in Tabela_Simbolos.keys():
            if(Tabela_Simbolos[chave]["lexema"] == atributos[0]["lexema"]):
                if(Tabela_Simbolos[chave]["tipo"] == "literal"):
                    dadosParaArquivo.append("scanf('%s', {});".format(Tabela_Simbolos[chave]["lexema"]))
                elif(Tabela_Simbolos[chave]["tipo"] == "inteiro"):
                    dadosParaArquivo.append("scanf('%d', &{});".format(Tabela_Simbolos[chave]["lexema"]))
                elif(Tabela_Simbolos[chave]["tipo"] == "real"):
                    dadosParaArquivo.append("scanf('%lf', &{});".format(Tabela_Simbolos[chave]["lexema"]))
                else:
                    print("Erro: Variável não declarada. Linha XX e Coluna XX")
            


    elif(numeroDaRegra == 13):
        dadosParaArquivo.append("printf({})".format(atributos[0]["lexema"]))
    
    elif(numeroDaRegra == 16):
        temDeclaracao = False

        for item in atributos:
            for chave in Tabela_Simbolos.keys():
                if(Tabela_Simbolos[chave]["classe"] == "id" and Tabela_Simbolos[chave]["lexema"] == item["lexema"]):
                    temDeclaracao = True
            if(not temDeclaracao):
                print("Erro: Varável não declarada. Linha XX, Coluna XX")
            temDeclaracao = False
    
    elif(numeroDaRegra == 18):
        
        for chave in Tabela_Simbolos.keys():
            if(Tabela_Simbolos[chave]["lexema"] == atributos[0]["lexema"]):
                if(atributos[0]["tipo"] == atributos[2]["tipo"]):
                    primeiro = next(aux for aux in atributos if aux["classe"] == "id")["lexema"]
                    segundo = next(aux for aux in atributos if aux["classe"] != "rcb" and aux["lexema"] != primeiro)["lexema"]

                    dadosParaArquivo.append("{} = {}".format(primeiro, segundo))

                else:
                    print("Erro: Tipos diferentes para atribuição. Linha XX e Coluna XX")

            else:
                print("Erro: Variável não declarada. Linha XX e Coluna XX")

    elif(numeroDaRegra == 19):
        temporaria = {}
        if(all(atributo["tipo"] != "literal" and (atributos[0]["tipo"] == atributo["tipo"] or atributo["classe"] == "opm") for atributo in atributos)):
            nomeVariavel = "T{}".format(x)
            x = x + 1
            temporaria[nomeVariavel] = next(x for x in atributos if x["classe"] == "id")["lexema"] + next(x for x in atributos if x["classe"] == "opm")["lexema"] + next(x for x in atributos if x["classe"] == "num")["lexema"]
            pilha_semantica[-1]["lexema"] = nomeVariavel
            pilha_semantica[-1]["tipo"] = atributos[3]["tipo"]
            dadosParaArquivo.append("{} = {}".format(nomeVariavel, temporaria[nomeVariavel]))
            variaveisTemporarias.append(temporaria)
        else:
            print("Erro: Operadores com tipos incompatíveis. Linha XX, Coluna XX")

    elif(numeroDaRegra == 21):
        temDeclaracao = False
        pilha_semantica[-1]["atributos"] = []

        for item in atributos:
            for chave in Tabela_Simbolos.keys():
                if(Tabela_Simbolos[chave]["classe"] == "id" and Tabela_Simbolos[chave]["lexema"] == item["lexema"]):
                    temDeclaracao = True
                    pilha_semantica[-1]["atributos"].append(item)
            if(not temDeclaracao):
                print("Erro: Variável não declarada. Linha XX, Coluna XX")
            temDeclaracao = False

    elif(numeroDaRegra == 22):
        pilha_semantica[-1]["atributos"] = []
        for item in atributos:
            pilha_semantica[-1]["atributos"].append(item)

    elif(numeroDaRegra == 24):
        dadosParaArquivo.append("}")

    elif(numeroDaRegra == 25):
        dadosParaArquivo.append("if({}) {{".format(atributos[0]["lexema"]))

    elif(numeroDaRegra == 26):
        temporaria = {}
        if(atributos[0]["atributos"][0]["tipo"] == atributos[2]["atributos"][0]["tipo"]):
            nomeVariavel = "T{}".format(x)
            x = x + 1
            temporaria[nomeVariavel] = atributos[0]["atributos"][0]["lexema"] + atributos[1]["lexema"] + atributos[2]["atributos"][0]["lexema"]
            pilha_semantica[-1]["lexema"] = nomeVariavel
            dadosParaArquivo.append("{} = {}".format(nomeVariavel, temporaria[nomeVariavel]))
            variaveisTemporarias.append(temporaria)
            
        else:
            print("Erro: Operandos com tipos incompatíveis. Linha XX e Coluna XX")
