import streamlit as st
from programacao_linear import pLinear, verify_viability

# Define o título da aba e o layout da página
st.set_page_config(page_title="Otimizador Simplex", layout="wide")
st.title("Otimizador Simplex com Análise de Sensibilidade")
st.markdown("Este aplicativo resolve problemas usando o método Simplex com até 4 variáveis. Forneça os dados no menu lateral e execute os cálculos.")

# Cria um estado persistente para armazenar os preços sombra anteriores
if "previous_psombras" not in st.session_state:
    st.session_state.previous_psombras = []

# Função auxiliar para arredondar os valores de entrada com até 4 casas decimais
def validate_decimal(value, key):
    return round(value, 4) if value is not None else value

# Menu lateral
with st.sidebar:
    st.header("Configurações")

    # Define o número de variáveis (1 a 4) e o número de restrições (1 a 10)
    num_variaveis = st.number_input("Número de variáveis", min_value=1, max_value=4, step=1, key="num_variaveis")
    num_restricoes = st.number_input("Número de restrições", min_value=1, max_value=10, step=1, key="num_restricoes")
    st.markdown("---")
    st.subheader("Coeficientes da Função Objetivo")

    # O usuário insere os coeficientes de cada variável para a função objetivo
    coeficientes_fo = []
    for i in range(num_variaveis):
        coef = validate_decimal(
            st.number_input(f"Coef. X{i+1}", key=f"coef_fo_{i}"),
            key=f"coef_fo_{i}",
        )
        coeficientes_fo.append(coef)
    st.markdown("---")
    st.subheader("Restrições")

    # Contrução do menu das restirções
    restricoes = []
    for i in range(num_restricoes):
        st.markdown(f"**Restrição {i+1}**")
        restricao = []
        
        # Coeficientes das variáveis (input distribuído em colunas)
        cols = st.columns(num_variaveis)
        for j in range(num_variaveis):
            coef = validate_decimal(
                cols[j].number_input(f"X{j+1} (R{i+1})", key=f"coef_{i}_{j}"),
                key=f"coef_{i}_{j}",
            )
            restricao.append(coef)
        
        # Limite da inequação
        limite = st.number_input(f"Limite (R{i+1})", key=f"limite_{i}")

        # Sinal da inequação
        sinal = st.selectbox(f"Sinal (R{i+1})", ("<=", ">="), key=f"sinal_{i}")
        
        # Constroi a matriz restricoes
        restricao += [sinal, limite]
        restricoes.append(restricao)

# Definição dos titulos das abas
tabs = st.tabs(["Visualização do Problema", "Solução", "Alterações"])

# Definindo a primeira aba
with tabs[0]:
    # Mostra a função objetivo e restrições formatadas
    st.subheader("Função Objetivo")
    fo_str = " + ".join([f"{coeficientes_fo[i]}·X{i+1}" for i in range(num_variaveis)])
    st.code(f"Max Z = {fo_str}", language="markdown")

    st.subheader("Restrições")
    for i, restricao in enumerate(restricoes):
        coef = restricao[:-2]
        limite = restricao[-1]
        sinal = restricao[-2]
        if any(c != 0 for c in coef):
            restr_str = " + ".join([f"{coef[j]}·X{j+1}" for j in range(len(coef)) if coef[j] != 0])
            st.code(f"{restr_str} {sinal} {limite}", language="markdown")

    st.code("X1, X2, ..., Xn ≥ 0", language="markdown")

# Definição da segunda aba
with tabs[1]:
    if st.button("Calcular Solução"):
        try:
            # Chama a função pLinear passando os dados
            result = pLinear(num_variaveis, coeficientes_fo, restricoes)
            st.success("Solução Ótima Encontrada")
            # Mostra os valores otimos encontrados
            for i, val in enumerate(result[0]):
                st.write(f"**X{i+1} = {val}**")
            
            # Mostra o lucro maximo
            st.markdown(f"### Lucro Máximo (Z): `{result[1]}`")

            st.subheader("Preços Sombra")
            # Salva os preços sombra
            st.session_state.previous_psombras.clear()
            for i, preco in enumerate(result[2]):
                st.write(f"Restrição {i+1}: **{preco}** reais")
                st.session_state.previous_psombras.append(preco)
        except Exception as e:
            st.error(f"Erro ao calcular solução: {e}")

# Definição da terceira aba
with tabs[2]:
    st.subheader("Alterações nas Restrições")
    alteracoes = []

    # Altera dinamicamente os limites das restrições
    for i, restricao in enumerate(restricoes):
        st.write(f"Alterar limite da restrição {i+1}")
        alteracao = st.number_input(f"Δ Limite (R{i+1})", key=f"alt_{i}")
        restricoes[i][-1] += alteracao
        alteracoes.append(alteracao)

    if st.button("Verificar Viabilidade"):
        # Chama verify_viability para checar se as alterações ainda formam um problema viável
        viavel, restricoes_inviaveis = verify_viability(restricoes)
        if viavel:
            # Resolve de novo com pLinear
            result = pLinear(num_variaveis, coeficientes_fo, restricoes)
            new_psombras = result[2]
            novo_lucro = result[1]

            # Compara os novos preços sombra com os antigos
            if st.session_state.previous_psombras:
                alteracao_viavel = new_psombras == st.session_state.previous_psombras
                
                # Se iguais: indica que as alterações são sensíveis e não afetam o modelo
                if alteracao_viavel:
                    st.success("Alterações viáveis. Preços sombra mantidos.")
                    st.markdown(f"**Novo Lucro Ótimo (Z):** `{novo_lucro}`")
                    st.markdown("### Limites de validade do preço-sombra (sensibilidade)")

                    for i, preco in enumerate(new_psombras):
                        if i < len(alteracoes):
                            delta = alteracoes[i]
                            if delta > 0:
                                sentido = "aumentar"
                            elif delta < 0:
                                sentido = "reduzir"
                            else:
                                sentido = "manter"
                            st.write(f"- Restrição {i+1}: foi possível **{sentido}** o limite em `{abs(delta)}` sem alterar os preços sombra.")
                
                # Se diferentes: alterações invalidam a análise de sensibilidade            
                else:
                    st.warning("Alterações afetam os preços sombra. Resultado não é considerado viável no contexto de sensibilidade.")
                    st.markdown(f"**Novo Lucro Ótimo (Z):** `{novo_lucro}`")
            else:
                st.info("Preços sombra originais ainda não foram calculados na solução inicial.")
        else:
            st.error("Restrições inviáveis: " + ", ".join(map(str, restricoes_inviaveis)))
