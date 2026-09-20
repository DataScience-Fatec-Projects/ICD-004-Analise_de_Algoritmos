"""[06] Bubble sort com parada antecipada e rastreamento de cada passagem
Tema: Ordenação | Complexidade: melhor O(n), médio e pior O(n²) | Memória: O(1)
Palavras-chave: bubble sort, ordenação por bolha, vizinhos, troca, passagem, houve_troca, parada antecipada, melhor caso O(n), n(n-1)/2, atividade 02

O que faz:
- Ordena comparando pares VIZINHOS e trocando quando estão fora de ordem; mostra a lista após cada passagem.
- Para quando uma passagem inteira não troca nada (lista já ordenada).
- Conta comparações, trocas e passagens nos três cenários da Atividade 02 (n = 5).

Perguntas prováveis:
P: Como funciona o bubble sort?
R: Compara cada par de vizinhos e troca se estiverem fora de ordem; a cada passagem o maior elemento restante "sobe" para o fim. Repete até uma passagem sem trocas.
P: Por que o melhor caso é O(n)?
R: Em lista já ordenada, a 1ª passagem faz n-1 comparações e nenhuma troca; o algoritmo percebe e para. Ex.: n = 5 -> 4 comparações, 0 trocas, 1 passagem.
P: Quantas comparações e trocas no pior caso (lista invertida)?
R: n(n-1)/2 comparações e n(n-1)/2 trocas, porque TODO par comparado está fora de ordem. Para n = 5: 10 e 10.
P: Por que o laço interno vai até n - 1 - passagem?
R: Porque depois de cada passagem o maior elemento já está no fim; a cauda está ordenada e não precisa ser comparada de novo.
P: Bubble sort ou selection sort para uma lista quase ordenada?
R: Bubble sort: ele detecta a ordem e para cedo. O selection sort faria n(n-1)/2 comparações de qualquer jeito.
"""


def bubble_sort(lista, mostrar=False):
    lista = list(lista)                        # copia, nao altera a original
    n = len(lista)
    comparacoes = trocas = passagens = 0
    for passagem in range(n - 1):              # no maximo n-1 passagens
        houve_troca = False
        passagens += 1
        for i in range(n - 1 - passagem):      # a cauda ja esta ordenada
            comparacoes += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                trocas += 1
                houve_troca = True
        if mostrar:
            print(f"  passagem {passagem + 1}: {lista}  (trocou: {'sim' if houve_troca else 'nao'})")
        if not houve_troca:                    # passagem sem troca -> ja ordenada
            break
    return lista, comparacoes, trocas, passagens


if __name__ == "__main__":
    cenarios = [
        ("melhor caso (ja ordenada)", [1, 2, 3, 4, 5]),
        ("caso medio (aleatoria)", [3, 5, 1, 4, 2]),
        ("pior caso (invertida)", [5, 4, 3, 2, 1]),
        ("exemplo da revisao", [5, 2, 9, 1, 7]),
    ]
    for nome, lst in cenarios:
        print(f"\n{nome}: {lst}")
        ordenada, comp, troc, pas = bubble_sort(lst, mostrar=True)
        print(f"  => {ordenada} | comparacoes={comp} trocas={troc} passagens={pas}")

    print("\nPior caso (invertida): comparacoes = trocas = n(n-1)/2")
    for n in (5, 10, 100, 500):
        _, comp, troc, _ = bubble_sort(list(range(n, 0, -1)))
        print(f"  n={n:<4} comparacoes={comp:<7} trocas={troc:<7} n(n-1)/2={n * (n - 1) // 2}")
