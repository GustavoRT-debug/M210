# 📊 SolveX – Solucionador de Programação Linear com Método Simplex

SolveX é uma aplicação web interativa desenvolvida com **Streamlit** para resolver problemas de **Programação Linear (PPL)** utilizando o **método Simplex Tableau**. A ferramenta suporta até **4 variáveis** e **5 restrições**, oferecendo uma interface intuitiva para entrada de dados, resolução do problema e análise de sensibilidade com **preço sombra** e **folgas** das restrições.

Opção 2: Desenvolver o código, em Python, para resolver um PPL com 2,3 ou 4 variáveis, usando 
o método Simplex Tableau. O mesmo deverá possuir uma entrada de dados amigável assim 
como uma saída. É permitido o uso de bibliotecas específicas de programação linear. 
A entrada de dados é composta pelos coeficientes da função objetivo e das restrições. Além 
disto das variações desejadas em cada restrição. 
A saída de dados deve conter o ponto ótimo de operação, o preço-sombra de cada restrição  
e se as alterações desejadas são viáveis. Caso as alterações sejam viáveis, apresentar o novo 
lucro ótimo e o limite de validade do preço-sombra. 
A diferença da primeira opção, neste caso, é a de que deve ser desenvolvida uma interface 
gráfica (frontend) utilizando bibliotecas para este fim. Exemplo: streamlit, panel, gradio, etc. 

---

## 🚀 Funcionalidades

- **Entrada de dados personalizada**: Defina a função objetivo e as restrições de forma simples e intuitiva.
- **Maximização e Minimização**: Suporte para ambos os tipos de otimização.
- **Visualização interativa**: Exibição do tableau Simplex em formato de tabela editável.
- **Resultados detalhados**:
  - Valor ótimo da função objetivo (Z).
  - Valores ótimos das variáveis de decisão.
  - Preços sombra das restrições.
  - Folgas das restrições.
- **Análise de sensibilidade**: Reanalise o problema alterando a disponibilidade dos recursos.
- **Avaliação de viabilidade**: Verifique a viabilidade e o novo lucro após alterações nos recursos.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- Algoritmo Simplex implementado manualmente ou via biblioteca externa (ex.: `PuLP`, `scipy.optimize`)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/GustavoRT-debug/M210.git
cd M210
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Certifique-se de que as bibliotecas `streamlit` e `pandas` estão instaladas.

### 3. Execute a aplicação

```bash
streamlit run main.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

---

## 📂 Estrutura do Projeto

```
M210/
├── main.py                   # Arquivo principal com a interface Streamlit
├── functions.py              # Funções auxiliares (Simplex, criação da tabela etc.)
├── requirements.txt          # Lista de dependências
└── README.md                 # Documentação do projeto
```

---

## ✍️ Exemplo de Uso

1. **Defina o problema**:
   - Escolha o número de variáveis (até 4) e restrições (até 5).
   - Selecione entre **Maximizar** ou **Minimizar** a função objetivo.
2. **Crie o tableau**:
   - Clique em "Criar Tabela Simplex" para gerar a tabela editável.
3. **Preencha os dados**:
   - Insira os coeficientes da função objetivo e das restrições na tabela.
4. **Resolva o problema**:
   - Clique em "Resolver Tableau" para obter:
     - Valor ótimo (Z).
     - Valores das variáveis de decisão.
     - Preços sombra.
     - Folgas.
5. **Análise de sensibilidade** (opcional):
   - Altere a disponibilidade dos recursos e clique em "Recalcular com novas disponibilidades" para avaliar a viabilidade e o novo lucro.

---

## 🧠 Conceitos Envolvidos

- **Programação Linear (PPL)**: Modelagem de problemas de otimização com restrições lineares.
- **Método Simplex Tableau**: Algoritmo iterativo para encontrar a solução ótima de problemas de PPL.
- **Análise de Sensibilidade**: Avaliação do impacto de mudanças nos recursos disponíveis.
- **Preço Sombra**: Indica o quanto o valor ótimo da função objetivo mudaria ao alterar a disponibilidade de um recurso.
- **Folgas**: Representam os recursos não utilizados após a alocação ótima.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias no código, novas funcionalidades ou correções de bugs.

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie para o repositório remoto (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Desenvolvido com 💻 
```
