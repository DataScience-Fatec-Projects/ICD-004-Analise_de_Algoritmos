"""[08] Quicksort (versão do livro/aula) com rastreamento de pivô, partição e pilha
Tema: Dividir para conquistar / Ordenação | Complexidade: melhor e médio O(n log n), pior O(n²) | Memória: pilha O(log n) a O(n) + listas novas O(n)
Palavras-chave: quicksort, pivô, particionamento, menores, maiores, caso base, recursão, altura da pilha, chamadas, dividir para conquistar, aula 06

O que faz:
- Implementa o quicksort do livro (pivô = primeiro elemento, listas novas de menores e maiores).
- Mostra cada chamada com recuo pela profundidade: pivô, menores, maiores e o resultado combinado.
- Conta o total de chamadas e a altura máxima da pilha para uma lista aleatória e para uma já ordenada (pior caso).

Perguntas prováveis:
P: Qual é o caso base do quicksort?
R: Lista com 0 ou 1 elemento: já está ordenada, basta devolvê-la.
P: Quais são as três etapas do quicksort?
R: 1) escolher o pivô; 2) particionar em menores e maiores que o pivô; 3) chamar o quicksort recursivamente nos dois subarrays e combinar: menores + [pivô] + maiores.
P: Por que a lista ordenada é o pior caso com pivô no primeiro elemento?
R: Um dos subarrays fica sempre vazio: a lista só diminui de 1 por nível, a pilha tem altura n e cada nível ainda custa O(n), total O(n²).
P: O que muda entre melhor e pior caso: o custo de cada nível ou a quantidade de níveis?
R: A quantidade de níveis (altura da pilha): log n no melhor, n no pior. Cada nível custa O(n) de qualquer jeito.
P: Quantas chamadas de quicksort ocorrem?
R: Sempre O(n): cada chamada com 2 ou mais elementos gera duas novas. Para [33, 15, 10, 42, 7] são 7 chamadas; para [1, 2, 3, 4, 5] (pior caso) são 9.
"""
import sys

sys.setrecursionlimit(5000)

chamadas = 0
altura_max = 0


def quicksort(array, profundidade=0, mostrar=False):
    global chamadas, altura_max
    chamadas += 1
    altura_max = max(altura_max, profundidade + 1)
    recuo = "  " * profundidade
    if len(array) < 2:                          # caso base
        if mostrar:
            print(f"{recuo}quicksort({array}) -> {array}  (caso base)")
        return array
    pivo = array[0]
    menores = [x for x in array[1:] if x <= pivo]
    maiores = [x for x in array[1:] if x > pivo]
    if mostrar:
        print(f"{recuo}quicksort({array}): pivo={pivo} menores={menores} maiores={maiores}")
    resultado = quicksort(menores, profundidade + 1, mostrar) + [pivo] + quicksort(maiores, profundidade + 1, mostrar)
    if mostrar:
        print(f"{recuo}-> {resultado}")
    return resultado


def medir(array, mostrar=False):
    global chamadas, altura_max
    chamadas = altura_max = 0
    resultado = quicksort(array, mostrar=mostrar)
    return resultado, chamadas, altura_max


if __name__ == "__main__":
    for nome, lst in (("exemplo da aula", [33, 15, 10, 42, 7]), ("pior caso: ja ordenada", [1, 2, 3, 4, 5])):
        print(f"\n{nome}: {lst}")
        r, c, a = medir(lst, mostrar=True)
        print(f"resultado={r} chamadas={c} altura da pilha={a}")

    print("\nAltura da pilha para n = 1000:")
    import random
    random.seed(42)
    aleatoria = random.sample(range(1000), 1000)
    _, c1, a1 = medir(aleatoria)
    _, c2, a2 = medir(list(range(1000)))
    print(f"  lista aleatoria : chamadas={c1:<5} altura={a1:<5} (~log2 n = 10 no ideal)")
    print(f"  lista ordenada  : chamadas={c2:<5} altura={a2:<5} (= n: pior caso, O(n^2))")
