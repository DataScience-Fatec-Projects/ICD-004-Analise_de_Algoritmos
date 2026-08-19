# Objeto de estudo — versão avançada da Atividade 01

Esta pasta **não é a entrega**. A entrega é o PDF simples em `Aulas/03/`.

Aqui está uma versão mais rigorosa do mesmo experimento, para estudar depois com calma.
Tudo roda igual: `python atividade01.py` e depois `python gerar_pdf.py`.

## Arquivos

| Arquivo | O que é |
|---|---|
| `atividade01.py` | Experimento completo: 4 cenários × 4 tamanhos de lista, medição por mediana, validação automática e geração dos gráficos |
| `gerar_pdf.py` | Monta um relatório de 9 páginas a partir do `saida/resultados.json` |
| `saida/resultados.json` | Todos os números medidos (é a fonte do PDF — o relatório não tem número digitado à mão) |
| `saida/grafico_*.png` | Passos, tempo e ganho de velocidade |
| `saida/Atividade01_Busca_Linear_vs_Binaria.pdf` | O relatório avançado |

## Roteiro de estudo (na ordem)

**1. Melhor caso, caso médio e pior caso.**
A versão simples testa só o pior caso (alvo no fim da lista). Aqui há quatro cenários, e um
resultado que parece contraditório: **no melhor caso a busca linear ganha** — ela acha na
primeira comparação, enquanto a binária ainda precisa afunilar até a posição 0. Entender por
que isso não invalida o O(log n) é entender o que a notação Big O realmente afirma: ela fala
de *crescimento*, não de vantagem em todo caso particular.

**2. Por que medir passos E tempo.**
Contagem de passos é propriedade do algoritmo (igual em qualquer máquina); tempo é
propriedade da execução (muda com CPU, cache, linguagem). Quando as duas evidências
apontam junto, a conclusão não é artefato do computador de teste. Veja `medir_cenario()`.

**3. Como se mede tempo sem se enganar.**
Uma única medição de uma busca binária (~0,002 ms) está dentro do ruído do relógio. Em
`cronometrar()` a chamada é repetida até esgotar um orçamento de tempo e se usa a **mediana**,
não a média — a mediana ignora picos causados pelo sistema operacional.

**4. Verificar antes de comparar.**
`validar_algoritmos()` roda 500 buscas com alvos aleatórios comparando o resultado dos dois
algoritmos, e confere que a binária nunca passa de `floor(log2(n)) + 1` passos. Um algoritmo
rápido e errado não serve como base de comparação — por isso a validação vem antes do
benchmark.

**5. O preço do pré-requisito (a parte mais útil na prática).**
A binária exige lista ordenada, e ordenar custa O(n log n) — mais caro que uma única busca
linear O(n). O script mede isso e calcula o **ponto de equilíbrio**: abaixo de ~12 consultas
numa lista desordenada, a busca linear é a escolha certa; acima disso, vale ordenar uma vez e
usar a binária sempre. É a resposta para "qual é melhor?": depende de quantas vezes você vai
buscar.

**6. Reprodutibilidade.**
`random.seed(42)` faz o experimento sortear sempre os mesmos alvos. Sem isso, cada execução
mede um teste diferente e as comparações entre execuções não valem nada.

## Conceitos de Python que aparecem aqui e não na versão simples

`dataclass`, type hints (`list[int]`), `statistics.median`, `pathlib`, `json`, f-strings com
formatação (`f"{x:,.2f}"`), `inspect.getsource` (o PDF extrai o código do próprio script, então
relatório e implementação nunca divergem) e `assert` como ferramenta de validação.

## Dependências

`matplotlib` (gráficos) e `reportlab` (PDF) — os dois já instalados nesta máquina.
