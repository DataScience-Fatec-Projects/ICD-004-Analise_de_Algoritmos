"""[09] Quicksort: pivô primeiro x meio x aleatório (melhor, médio e pior caso) — experimento da aula 06
Tema: Dividir para conquistar / Ordenação / Medição | Complexidade: O(n log n) médio, O(n²) pior | Memória: pilha O(log n) a O(n)
Palavras-chave: quicksort, escolha do pivô, pivô aleatório, pivô do meio, random.choice, pior caso, lista ordenada, caso médio, tempo, comparações, altura da pilha, setrecursionlimit

O que faz:
- Ordena uma lista de 1.000 elementos já ordenada e uma embaralhada com três estratégias de pivô: primeiro, meio e aleatório.
- Para cada combinação mede comparações, altura da pilha e tempo, mostrando o pior caso O(n²) do pivô fixo em lista ordenada.

Perguntas prováveis:
P: Como evitar o pior caso do quicksort?
R: Não usar pivô fixo no primeiro/último elemento: escolher o do meio, um aleatório (random.choice) ou a mediana de três. Assim a partição tende a ser equilibrada e a altura fica ~log n.
P: Por que a aula usou sys.setrecursionlimit?
R: Porque no pior caso a pilha tem altura n (1.000 níveis para n = 1.000), acima do limite padrão do Python (~1.000), o que causaria RecursionError.
P: Com pivô aleatório, qual é o Big O esperado?
R: O(n log n) no caso médio; o pior caso O(n²) continua possível, mas com probabilidade desprezível.
P: Merge sort é sempre melhor por garantir O(n log n)?
R: Não necessariamente: o quicksort tem constante menor e costuma ser mais rápido na prática; o merge sort vale quando é preciso garantir o pior caso.
"""
import random
import sys
import time

sys.setrecursionlimit(5000)

comparacoes = 0
altura_max = 0


def quicksort(arr, escolher_pivo, profundidade=0):
    global comparacoes, altura_max
    altura_max = max(altura_max, profundidade + 1)
    if len(arr) <= 1:
        return arr
    i = escolher_pivo(arr)
    pivo = arr[i]
    resto = arr[:i] + arr[i + 1:]
    comparacoes += len(resto)                          # cada elemento e comparado com o pivo
    menores = [x for x in resto if x <= pivo]
    maiores = [x for x in resto if x > pivo]
    return quicksort(menores, escolher_pivo, profundidade + 1) + [pivo] + quicksort(maiores, escolher_pivo, profundidade + 1)


ESTRATEGIAS = {
    "primeiro": lambda arr: 0,
    "meio": lambda arr: len(arr) // 2,
    "aleatorio": lambda arr: random.randrange(len(arr)),
}


def medir(arr, nome):
    global comparacoes, altura_max
    comparacoes = altura_max = 0
    inicio = time.perf_counter()
    r = quicksort(arr, ESTRATEGIAS[nome])
    tempo = (time.perf_counter() - inicio) * 1000
    assert r == sorted(arr)                            # validar antes de comparar
    return comparacoes, altura_max, tempo


if __name__ == "__main__":
    random.seed(42)
    n = 1000
    ordenada = list(range(n))
    embaralhada = random.sample(range(n), n)
    print(f"n = {n} | n(n-1)/2 = {n*(n-1)//2} | n*log2(n) ~ {n * 10}")
    print(f"{'lista':<12} {'pivo':<10} {'comparacoes':>12} {'altura pilha':>13} {'tempo (ms)':>11}")
    print("-" * 62)
    for nome_lista, lst in (("ordenada", ordenada), ("embaralhada", embaralhada)):
        for pivo in ESTRATEGIAS:
            c, a, t = medir(lst, pivo)
            print(f"{nome_lista:<12} {pivo:<10} {c:>12} {a:>13} {t:>11.3f}")
        print()
    print("Pivo fixo + lista ordenada: altura = n e comparacoes = n(n-1)/2 -> O(n^2).")
    print("Pivo do meio ou aleatorio: altura ~ log2 n e comparacoes ~ n log n -> O(n log n).")
