import pulp as pl

def pLinear(nvar,f_obj,rest):
    #Criar o modelo do problema
    model = pl.LpProblem("Maximize", pl.LpMaximize)

    #Definir as variáveis
    vars = []
    for i in range(nvar):
        vars.append(pl.LpVariable(chr(97+i), lowBound=0)) #add vars em ordem alfabética
    print(vars)
    
    #Adicionar função objetivo:
    print(sum(f_obj[i] * vars[i] for i in range(nvar)))
    model += sum(f_obj[i] * vars[i] for i in range(nvar))

    #Adicionar restrições
    for i in range(len(rest)):
        if(rest[i][-2] == "<="):
            model += sum(rest[i][j] * vars[j] for j in range(nvar)) <= rest[i][-1]
        else:
            model += sum(rest[i][j] * vars[j] for j in range(nvar)) >= rest[i][-1]

    #Resolver
    model.solve()
    
    #Salvar ponto ótimo
    p_otimo = []
    for i in range(nvar): 
        p_otimo.append(vars[i].varValue)
    lucro_otimo = pl.value(model.objective)

    precos_sombra = [model.constraints[list(model.constraints.keys())[i]].pi for i in range(len(rest))]

    return [p_otimo, lucro_otimo, precos_sombra]

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