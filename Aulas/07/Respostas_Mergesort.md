---
title: "Atividade – Mergesort"
subtitle: "Respostas"
---

<style>body{font-size:10pt} pre{font-size:9pt;line-height:1.25;margin:4px 0} h2{margin-top:12px} p,li{margin:3px 0}</style>

**Aluno:** Wellington Torres

## Questão 1

Vetor inicial: `[38, 27, 43, 3, 9, 82, 10]`

**Fase 1 – Divisão** (o vetor é dividido ao meio até restar 1 elemento por parte):

```
                    [38, 27, 43, 3, 9, 82, 10]
                   /                          \
          [38, 27, 43, 3]                  [9, 82, 10]
           /          \                     /        \
      [38, 27]      [43, 3]             [9, 82]      [10]
      /     \       /    \              /    \         |
   [38]    [27]  [43]    [3]          [9]   [82]     [10]
```

**Fase 2 – Intercalação (merge)**, de baixo para cima:

```
   [38]  [27]   [43]  [3]       [9]  [82]     [10]
      \  /         \  /            \  /         |
    [27, 38]      [3, 43]         [9, 82]      [10]
          \        /                   \       /
       [3, 27, 38, 43]                [9, 10, 82]
                  \                    /
             [3, 9, 10, 27, 38, 43, 82]
```

Vetor ordenado: **`[3, 9, 10, 27, 38, 43, 82]`**

## Questão 2

| Caso   | Complexidade   |
|--------|----------------|
| Melhor | **O(n log n)** |
| Médio  | **O(n log n)** |
| Pior   | **O(n log n)** |

**Por que é sempre igual:** o Mergesort divide o vetor **sempre no meio, pela posição**, sem olhar os valores. Por isso, a árvore de divisão tem sempre **log n níveis**. Em cada nível, o merge percorre os **n elementos** para intercalá-los. Isso dá **n × log n**, esteja o vetor ordenado ou embaralhado (recorrência T(n) = 2T(n/2) + n).

No Quicksort, a divisão depende do pivô. Um pivô ruim, como num vetor já ordenado, gera partições desequilibradas e leva o algoritmo a O(n²).

## Questão 3

O Mergesort usa **O(n) de memória auxiliar**, porque precisa de um vetor temporário para intercalar as metades durante o merge. Por isso consome mais memória que o Quicksort, que ordena **in-place** (troca os elementos no próprio vetor) e só usa a pilha de recursão, O(log n).

Ele é a melhor escolha quando:

- **É preciso estabilidade:** elementos iguais mantêm a ordem original.
- **Os dados não cabem na RAM:** ordenação externa, em arquivos grandes.
- **A estrutura é uma lista encadeada.**
- **É preciso tempo garantido O(n log n)**, sem risco do pior caso O(n²).
