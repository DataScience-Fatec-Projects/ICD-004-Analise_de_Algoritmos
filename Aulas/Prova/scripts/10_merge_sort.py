"""[10] Merge sort com rastreamento das divisões e intercalações
Tema: Dividir para conquistar / Ordenação | Complexidade: melhor, médio e pior O(n log n) | Memória: O(n)
Palavras-chave: merge sort, intercalação, merge, dividir ao meio, combinar, O(n log n) garantido, estável, memória extra, altura log n

O que faz:
- Divide a lista ao meio recursivamente até listas de 1 elemento e depois intercala (merge) as metades ordenadas.
- Mostra cada merge com recuo pela profundidade e conta comparações e altura da pilha.

Perguntas prováveis:
P: Quais são as etapas dividir, conquistar e combinar no merge sort?
R: Dividir: cortar a lista ao meio. Conquistar: ordenar cada metade recursivamente (caso base: 1 elemento). Combinar: intercalar as duas metades ordenadas em O(n).
P: Por que o merge sort é O(n log n) em todos os casos?
R: Sempre divide ao meio (altura log n) e cada nível intercala n elementos (O(n) por nível), independentemente da ordem inicial.
P: Qual é a desvantagem do merge sort em relação ao quicksort?
R: Usa O(n) de memória extra para as listas intercaladas e tem constante maior; na prática costuma ser um pouco mais lento.
P: Quando preferir merge sort?
R: Quando é preciso garantir O(n log n) no pior caso ou manter a ordem relativa de elementos iguais (estabilidade).
"""

comparacoes = 0
altura_max = 0


def merge_sort(array, profundidade=0, mostrar=False):
    global comparacoes, altura_max
    altura_max = max(altura_max, profundidade + 1)
    if len(array) < 2:                          # caso base
        return array
    meio = len(array) // 2
    esquerda = merge_sort(array[:meio], profundidade + 1, mostrar)     # dividir + conquistar
    direita = merge_sort(array[meio:], profundidade + 1, mostrar)
    saida, i, j = [], 0, 0
    while i < len(esquerda) and j < len(direita):                        # combinar (merge)
        comparacoes += 1
        if esquerda[i] <= direita[j]:
            saida.append(esquerda[i]); i += 1
        else:
            saida.append(direita[j]); j += 1
    saida += esquerda[i:] + direita[j:]
    if mostrar:
        print(f"{'  ' * profundidade}merge {esquerda} + {direita} -> {saida}")
    return saida


if __name__ == "__main__":
    lista = [38, 27, 43, 3, 9, 82, 10]
    print("Lista:", lista)
    r = merge_sort(lista, mostrar=True)
    print(f"resultado={r} comparacoes={comparacoes} altura da pilha={altura_max}")

    print("\nComparacoes <= n*log2(n) e altura = log2(n)+1 em QUALQUER cenario:")
    import math
    import random
    random.seed(42)
    for n in (8, 64, 1024):
        for nome, lst in (("ordenada", list(range(n))), ("aleatoria", random.sample(range(n), n)), ("invertida", list(range(n, 0, -1)))):
            comparacoes = altura_max = 0
            merge_sort(lst)
            print(f"  n={n:<5} {nome:<10} comparacoes={comparacoes:<6} altura={altura_max:<3} n*log2(n)={int(n * math.log2(n))}")
