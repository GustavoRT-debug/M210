import pulp as pl

    #o nvar: Número de variáveis de decisão                                                           
    #o f_obj: Lista com os coeficientes da função objetivo (os pesos de cada variável).
    #o rest: Lista de restrições, onde cada restrição é representada por uma lista 
    #contendo os coeficientes das variáveis, o tipo de restrição (<= ou >=), e o valor 
    #limite da restrição (lado direito)

def pLinear(nvar,f_obj,rest):

    #O PuLP gerencia internamente as equações e restrições do problema
    #Criar o modelo do problema
    model = pl.LpProblem("Maximize", pl.LpMaximize)

    # nvar = 2 → cria: a = x, b = y
    #lowBound=0 → não pode ser negativo
    #Definir as variáveis
    vars = []
    for i in range(nvar):
        vars.append(pl.LpVariable(chr(97+i), lowBound=0)) #add vars em ordem alfabética
    print(vars)
    
    #Adicionar função objetivo:
    print(sum(f_obj[i] * vars[i] for i in range(nvar)))
    model += sum(f_obj[i] * vars[i] for i in range(nvar))


    #A função objetivo é uma combinação linear das variáveis, onde cada variável vars[i] é 
    #multiplicada pelo coeficiente correspondente em f_obj[i]. 
    #A linha model += ... adiciona a função objetivo ao modelo, configurando-a para ser maximizada.
    #Adicionar restrições
    for i in range(len(rest)):
        if(rest[i][-2] == "<="):
            model += sum(rest[i][j] * vars[j] for j in range(nvar)) <= rest[i][-1]
        else:
            model += sum(rest[i][j] * vars[j] for j in range(nvar)) >= rest[i][-1]

    #Agora o solver faz os cálculos matemáticos automaticamente, usando o método Simplex, e encontra os melhores valores para x e y que:
    #Maximizam o lucro
    #Resolver
    model.solve()
    
    #Salvar ponto ótimo
    p_otimo = []
    for i in range(nvar): 
        p_otimo.append(vars[i].varValue)
    lucro_otimo = pl.value(model.objective)

    #O preço sombra (pi) indica o impacto no valor da função objetivo por unidade de variação no 
    #lado direito da restrição.
    #Usa model.constraints para acessar as restrições e .pi para obter o preço sombra
    precos_sombra = [model.constraints[list(model.constraints.keys())[i]].pi for i in range(len(rest))]

    return [p_otimo, lucro_otimo, precos_sombra]

    #Passa sobre cada restrição em rest
    #Extrai os coeficientes (restricao[:-2]) e o limite (restricao[-1])
    #Calcula a soma dos coeficientes (soma_coeficientes) 
    #Verifica se a soma dos coeficientes é maior que o limite. Se for, a restrição é considerada 
    #inviável, e seu índice ( i + 1) é adicionado à lista infeasible_constraints

def verify_viability(rest):
    infeasible_constraints = []    
    for i, restricao in enumerate(rest):
        coeficientes = restricao[:-2]
        limite = restricao[-1]
        
        #Regra de viabilidade: soma dos coeficientes deve ser <= limite
        soma_coeficientes = sum(coeficientes)
        if soma_coeficientes > limite:
            infeasible_constraints.append(i + 1)

    #Retorna True se nenhuma restrição for inviável
    return len(infeasible_constraints) == 0, infeasible_constraints