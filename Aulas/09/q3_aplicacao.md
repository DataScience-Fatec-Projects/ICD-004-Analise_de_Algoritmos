# Questão 3 — Aplicação prática: detecção de fraude em uma rede de contas bancárias

## O problema

Um banco digital tem milhões de contas e precisa descobrir quais delas fazem parte de um **anel de
fraude**: grupos de contas laranja que recebem o dinheiro de um golpe e o repassam rapidamente
entre si até sacar. Olhar cada conta sozinha (valor, horário, idade da conta) não basta, porque cada
transferência, isolada, parece normal. O que entrega o golpe é a **ligação** entre as contas. Por isso
a análise tem de ser feita sobre um grafo.

## Como modelar com grafo

| Elemento do grafo | No cenário |
|---|---|
| **Vértice** | uma conta (ou cliente) |
| **Aresta** | uma relação entre duas contas: transferência PIX entre elas, mesmo celular/dispositivo usado para logar, mesmo endereço ou mesmo CPF de responsável |
| **Grafo não direcionado** | para descobrir quem está *ligado* a quem, a direção do dinheiro não importa (para seguir o fluxo do dinheiro, daria para usar a versão direcionada) |

A representação é a mesma do grafo do metrô da questão 1, um dicionário de listas de adjacência:

```python
rede = {
    'conta_A': ['conta_B', 'conta_C'],   # A fez PIX para B e usa o mesmo celular que C
    'conta_B': ['conta_A', 'conta_D'],
    ...
}
```

Em Ciência de Dados esse dicionário é montado a partir das tabelas do banco: cada linha da tabela de
transações (`origem`, `destino`) vira uma aresta, e o mesmo vale para a tabela de logins (`conta`,
`id_dispositivo`), ligando as contas que aparecem com o mesmo dispositivo. A lista de adjacência é a
escolha certa porque a rede é **esparsa**: cada conta se relaciona com poucas outras, e uma matriz
de adjacência de milhões × milhões seria quase toda de zeros.

## O que a BFS responde

1. **"Qual o caminho entre esta conta e um fraudador já confirmado?"** É exatamente a função
   `bfs_caminho_mais_curto` da questão 2. O caminho devolvido (ex.: `conta_X → conta_K → fraudador`)
   é a **explicação** do alerta, e o analista de prevenção a fraudes consegue conferir trecho por trecho.
2. **Distância até a fraude como variável (feature) do modelo.** Rodando a BFS a partir de *todas* as
   contas fraudulentas conhecidas ao mesmo tempo (BFS com várias origens), cada conta recebe a sua
   distância até a fraude mais próxima: 1 = transacionou direto com um fraudador, 2 = amigo de amigo,
   e assim por diante. Essa coluna entra no modelo de machine learning (regressão logística, árvore,
   XGBoost) ao lado das variáveis tradicionais, e costuma ser uma das mais fortes.
3. **Bloqueio preventivo por camadas.** Como a BFS anda em "ondas" (primeiro distância 1, depois 2...),
   ela entrega as contas por nível de risco: bloquear a camada 1, colocar a camada 2 em revisão manual.
4. **Encontrar o anel inteiro.** Uma BFS que começa em uma conta suspeita e roda até a fila esvaziar
   visita o **componente conectado** inteiro, ou seja, o grupo todo de contas ligadas. É o mesmo
   fenômeno do teste "sem caminho" da questão 2: o Aeroporto-Guarulhos está em outro componente,
   e a BFS nunca chega lá.

## Por que BFS e não outra busca

- A BFS garante o **menor número de saltos**, e na fraude a proximidade é o que importa: quanto menos
  intermediários, mais forte a suspeita. Uma busca em profundidade (DFS) acharia *um* caminho, não
  necessariamente o mais curto.
- Ela é eficiente: **O(V + E)**, porque cada conta entra na fila uma vez e cada relação é olhada uma vez.
  Isso viabiliza rodar sobre a rede inteira todas as noites.
- Na prática dá para limitar a profundidade (parar no nível 3, por exemplo), o que deixa a busca
  ainda mais barata.

## Outros cenários com a mesma ideia

- **Redes sociais:** "pessoas que você talvez conheça" são os vértices a distância 2 na BFS.
- **Epidemiologia:** rastreamento de contatos, com contatos diretos e de segundo grau de um caso.
- **Transporte (o próprio metrô):** menor número de estações ou de baldeações entre dois pontos.
