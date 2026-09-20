"""[07] Crescimento das operações: o que acontece quando n dobra (bubble x selection)
Tema: Ordenação / Big O | Complexidade: O(n²) | Memória: O(1)
Palavras-chave: n dobra, quadruplica, fator 4, n(n-1)/2, comparações, trocas, crescimento, tabela, random.seed, atividade 02, quadrático

O que faz:
- Roda bubble sort e selection sort para n = 25, 50, 100, 200, 400 nos três cenários (ordenada, aleatória, invertida).
- Imprime a tabela de comparações e trocas e a razão entre n e 2n, mostrando o fator ~4 do crescimento quadrático.
- Usa random.seed(42) para o cenário aleatório ser reprodutível.

Perguntas prováveis:
P: Quando n dobra, quantas vezes crescem as comparações de um algoritmo O(n²)?
R: Cerca de 4 vezes: (2n)² = 4n². Na tabela, 1.225 -> 4.950 -> 19.900 (fator ~4 a cada dobra).
P: Por que o melhor caso do bubble sort cresce só 2x quando n dobra?
R: Porque em lista ordenada ele faz n-1 comparações: crescimento linear, O(n).
P: Por que o selection sort faz o mesmo número de comparações nos três cenários?
R: Ele sempre varre o trecho restante inteiro para achar o menor, sem olhar se a lista já está ordenada.
P: Para que serve random.seed(42) aqui?
R: Para o cenário aleatório sortear sempre a mesma lista; sem isso cada execução mediria um teste diferente.
"""
import random


def bubble_sort(lista):
    lista = list(lista); n = len(lista); comp = troc = 0
    for passagem in range(n - 1):
        houve_troca = False
        for i in range(n - 1 - passagem):
            comp += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                troc += 1; houve_troca = True
        if not houve_troca:
            break
    return comp, troc


def selection_sort(lista):
    lista = list(lista); n = len(lista); comp = troc = 0
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            comp += 1
            if lista[j] < lista[menor]:
                menor = j
        if menor != i:
            lista[i], lista[menor] = lista[menor], lista[i]; troc += 1
    return comp, troc


if __name__ == "__main__":
    random.seed(42)
    tamanhos = (25, 50, 100, 200, 400)
    print(f"{'n':>5} {'cenario':<10} {'bubble comp':>12} {'bubble troc':>12} {'select comp':>12} {'select troc':>12}")
    print("-" * 68)
    pior_bubble = {}
    for n in tamanhos:
        listas = {
            "melhor": list(range(n)),
            "medio": random.sample(range(n), n),
            "pior": list(range(n, 0, -1)),
        }
        for cenario, lst in listas.items():
            bc, bt = bubble_sort(lst)
            sc, st = selection_sort(lst)
            print(f"{n:>5} {cenario:<10} {bc:>12} {bt:>12} {sc:>12} {st:>12}")
            if cenario == "pior":
                pior_bubble[n] = bc
        print()

    print("Razao entre n e 2n (pior caso, comparacoes do bubble sort):")
    for n in tamanhos[:-1]:
        print(f"  {n:>4} -> {2 * n:<4}: {pior_bubble[2 * n] / pior_bubble[n]:.2f}x   (n(n-1)/2: {n*(n-1)//2} -> {2*n*(2*n-1)//2})")
    print("Fator ~4 a cada dobra = crescimento quadratico, O(n^2).")
