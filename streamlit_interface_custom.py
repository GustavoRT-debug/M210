import streamlit as st
from programacao_linear import pLinear, verify_viability

st.set_page_config(page_title="Otimizador Simplex", layout="wide")
st.title("Otimizador Simplex com Análise de Sensibilidade")

st.markdown("Este aplicativo resolve problemas usando o método Simplex com até 4 variáveis. Forneça os dados no menu lateral e execute os cálculos.")

if "previous_psombras" not in st.session_state:
    st.session_state.previous_psombras = []

def validate_decimal(value, key):
    return round(value, 4) if value is not None else value

with st.sidebar:
    st.header("Configurações")
    num_variaveis = st.number_input("Número de variáveis", min_value=1, max_value=4, step=1, key="num_variaveis")
    num_restricoes = st.number_input("Número de restrições", min_value=1, max_value=10, step=1, key="num_restricoes")

    st.markdown("---")
    st.subheader("Coeficientes da Função Objetivo")
    coeficientes_fo = []
    for i in range(num_variaveis):
        coef = validate_decimal(
            st.number_input(f"Coef. X{i+1}", key=f"coef_fo_{i}"),
            key=f"coef_fo_{i}",
        )
        coeficientes_fo.append(coef)

    st.markdown("---")
    st.subheader("Restrições")
    restricoes = []
    for i in range(num_restricoes):
        st.markdown(f"**Restrição {i+1}**")
        restricao = []
        cols = st.columns(num_variaveis)
        for j in range(num_variaveis):
            coef = validate_decimal(
                cols[j].number_input(f"X{j+1} (R{i+1})", key=f"coef_{i}_{j}"),
                key=f"coef_{i}_{j}",
            )
            restricao.append(coef)
        limite = st.number_input(f"Limite (R{i+1})", key=f"limite_{i}")
        sinal = st.selectbox(f"Sinal (R{i+1})", ("<=", ">="), key=f"sinal_{i}")
        restricao += [sinal, limite]
        restricoes.append(restricao)

tabs = st.tabs(["Visualização do Problema", "Solução", "Alterações"])

with tabs[0]:
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

with tabs[1]:
    if st.button("Calcular Solução"):
        try:
            result = pLinear(num_variaveis, coeficientes_fo, restricoes)
            st.success("Solução Ótima Encontrada")
            for i, val in enumerate(result[0]):
                st.write(f"**X{i+1} = {val}**")
            st.markdown(f"### Lucro Máximo (Z): `{result[1]}`")

            st.subheader("Preços Sombra")
            st.session_state.previous_psombras.clear()
            for i, preco in enumerate(result[2]):
                st.write(f"Restrição {i+1}: **{preco}** reais")
                st.session_state.previous_psombras.append(preco)
        except Exception as e:
            st.error(f"Erro ao calcular solução: {e}")

with tabs[2]:
    st.subheader("Alterações nas Restrições")
    alteracoes = []
    for i, restricao in enumerate(restricoes):
        st.write(f"Alterar limite da restrição {i+1}")
        alteracao = st.number_input(f"Δ Limite (R{i+1})", key=f"alt_{i}")
        restricoes[i][-1] += alteracao
        alteracoes.append(alteracao)

    if st.button("Verificar Viabilidade"):
        viavel, restricoes_inviaveis = verify_viability(restricoes)
        if viavel:
            result = pLinear(num_variaveis, coeficientes_fo, restricoes)
            new_psombras = result[2]
            novo_lucro = result[1]

            if st.session_state.previous_psombras:
                alteracao_viavel = new_psombras == st.session_state.previous_psombras

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
                else:
                    st.warning("Alterações afetam os preços sombra. Resultado não é considerado viável no contexto de sensibilidade.")
                    st.markdown(f"**Novo Lucro Ótimo (Z):** `{novo_lucro}`")
            else:
                st.info("Preços sombra originais ainda não foram calculados na solução inicial.")
        else:
            st.error("Restrições inviáveis: " + ", ".join(map(str, restricoes_inviaveis)))
