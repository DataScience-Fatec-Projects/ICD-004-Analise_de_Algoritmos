"""[05] Selection sort com rastreamento de cada passagem
Tema: Ordenação | Complexidade: melhor, médio e pior O(n²) | Memória: O(1)
Palavras-chave: selection sort, ordenação por seleção, menor elemento, n(n-1)/2, comparações, trocas, sempre quadrático, livro cap. 2

O que faz:
- Ordena mostrando, a cada passagem, qual foi o menor encontrado e a lista resultante.
- Conta comparações e trocas nos três cenários (ordenada, aleatória, invertida) com n = 5.
- Mostra que as comparações são SEMPRE n(n-1)/2, independentemente da ordem inicial.

Perguntas prováveis:
P: Como funciona o selection sort?
R: A cada passagem percorre o trecho ainda não ordenado, encontra o MENOR elemento e o coloca na primeira posição livre. Repete n-1 vezes.
P: Por que ele é O(n²) mesmo no melhor caso?
R: Porque não aproveita a ordem existente: sempre varre todo o trecho restante para achar o menor. Faz (n-1) + (n-2) + ... + 1 = n(n-1)/2 comparações em qualquer entrada.
P: Quantas trocas ele faz no máximo?
R: n-1 (uma por passagem, e só quando o menor não está no lugar). Por isso é bom quando a troca é cara.
P: Por que O(n²) e não O(n²/2)? (Livro, cap. 2)
R: Big O ignora constantes multiplicativas como o 1/2; o que importa é o crescimento quadrático.
"""


def selection_sort(lista, mostrar=False):
    lista = list(lista)                        # copia, nao altera a original
    n = len(lista)
    comparacoes = trocas = 0
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):              # procura o menor no trecho restante
            comparacoes += 1
            if lista[j] < lista[menor]:
                menor = j
        if menor != i:
            lista[i], lista[menor] = lista[menor], lista[i]
            trocas += 1
        if mostrar:
            print(f"  passagem {i + 1}: menor={lista[i]} (veio do indice {menor}) -> {lista}")
    return lista, comparacoes, trocas


if __name__ == "__main__":
    cenarios = [
        ("melhor caso (ja ordenada)", [1, 2, 3, 4, 5]),
        ("caso medio (aleatoria)", [3, 5, 1, 4, 2]),
        ("pior caso (invertida)", [5, 4, 3, 2, 1]),
        ("exemplo da revisao", [5, 2, 9, 1, 7]),
    ]
    for nome, lst in cenarios:
        print(f"\n{nome}: {lst}")
        ordenada, comp, troc = selection_sort(lst, mostrar=True)
        print(f"  => {ordenada} | comparacoes={comp} trocas={troc}")

    print("\nComparacoes sao SEMPRE n(n-1)/2:")
    for n in (5, 10, 100, 500):
        _, comp, _ = selection_sort(list(range(n, 0, -1)))
        print(f"  n={n:<4} comparacoes={comp:<7} n(n-1)/2={n * (n - 1) // 2}")
