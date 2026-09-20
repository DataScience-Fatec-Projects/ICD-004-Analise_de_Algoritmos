"""[15] Fibonacci: recursivo x memoizado x iterativo — tempo, chamadas e profundidade da pilha
Tema: Recursividade / Fibonacci / Medição | Complexidade: O(2^n) x O(n) x O(n) | Memória: O(n) x O(n) x O(1)
Palavras-chave: fibonacci iterativo, bottom-up, comparação, benchmark, timeit, mínimo, tempo, memória, profundidade da pilha, getsizeof, memória auxiliar, atividade 03

O que faz:
- Valida que as três implementações dão os mesmos valores (teste de corretude antes do benchmark).
- Mede o tempo das três para n = 20..30 com timeit (menor de várias rodadas), zerando o cache a cada execução.
- Mede a profundidade máxima da pilha e a memória auxiliar (tamanho do cache) de cada versão.

Perguntas prováveis:
P: Qual versão é a mais eficiente e por quê?
R: A iterativa (bottom-up): O(n) de tempo e O(1) de memória, sem risco de estourar a pilha. A memoizada também é O(n) de tempo, mas gasta O(n) de memória; a recursiva pura é O(2^n).
P: Por que validar a corretude antes do benchmark?
R: Comparar a velocidade de algoritmos que dão respostas diferentes não significa nada; um algoritmo rápido e errado não serve.
P: Por que usar o menor tempo (ou a mediana) e não a média?
R: O mínimo e a mediana são estáveis; a média é distorcida por picos do sistema operacional.
P: Por que o cache é zerado a cada execução do benchmark?
R: Para medir a construção da tabela inteira, e não um acerto de cache já pronto.
"""
import sys
import timeit

profundidade_atual = profundidade_maxima = 0


def fib_recursivo(n):
    global profundidade_atual, profundidade_maxima
    profundidade_atual += 1
    profundidade_maxima = max(profundidade_maxima, profundidade_atual)
    try:
        if n < 2:
            return n
        return fib_recursivo(n - 1) + fib_recursivo(n - 2)
    finally:
        profundidade_atual -= 1


def fib_memo(n, cache=None):
    global profundidade_atual, profundidade_maxima
    if cache is None:
        cache = {0: 0, 1: 1}
    profundidade_atual += 1
    profundidade_maxima = max(profundidade_maxima, profundidade_atual)
    try:
        if n in cache:
            return cache[n]
        cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
        return cache[n]
    finally:
        profundidade_atual -= 1


def fib_iterativo(n):
    anterior, atual = 0, 1
    for _ in range(n):
        anterior, atual = atual, anterior + atual
    return anterior


def menor_tempo(funcao, n, rodadas=3, repeticoes=1):
    return min(timeit.repeat(lambda: funcao(n), repeat=rodadas, number=repeticoes)) / repeticoes


if __name__ == "__main__":
    # 1) corretude
    esperado = [fib_iterativo(i) for i in range(21)]
    assert [fib_recursivo(i) for i in range(21)] == esperado
    assert [fib_memo(i) for i in range(21)] == esperado
    print("Corretude OK: as tres versoes coincidem para n = 0..20:", esperado[:12], "...")

    # 2) tempo
    print(f"\n{'n':>3} {'recursivo (s)':>14} {'memoizado (s)':>14} {'iterativo (s)':>14} {'ganho memo':>11}")
    for n in (20, 22, 24, 26, 28):
        tr = menor_tempo(fib_recursivo, n)
        tm = menor_tempo(fib_memo, n, rodadas=5, repeticoes=200)
        ti = menor_tempo(fib_iterativo, n, rodadas=5, repeticoes=200)
        print(f"{n:>3} {tr:>14.6f} {tm:>14.8f} {ti:>14.8f} {tr / tm:>10.0f}x")

    # 3) memoria: profundidade da pilha e memoria auxiliar
    n = 25
    profundidade_atual = profundidade_maxima = 0
    fib_recursivo(n)
    prof_rec = profundidade_maxima
    profundidade_atual = profundidade_maxima = 0
    cache = {0: 0, 1: 1}
    fib_memo(n, cache)
    prof_memo = profundidade_maxima
    print(f"\nMemoria (n = {n}):")
    print(f"  recursivo  pilha maxima={prof_rec:<3} quadros | memoria auxiliar: nenhuma (so a pilha)")
    print(f"  memoizado  pilha maxima={prof_memo:<3} quadros | cache com {len(cache)} entradas (~{sys.getsizeof(cache)} bytes so o dict)")
    print(f"  iterativo  pilha maxima=1   quadro  | 2 variaveis inteiras: O(1)")
    print("Recursivo puro: tempo exponencial, mas pilha O(n). Memoizado: troca memoria O(n) por tempo O(n).")
