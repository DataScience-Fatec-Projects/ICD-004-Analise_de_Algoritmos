"""[14] Fibonacci com memorização (cache): dicionário manual e @lru_cache
Tema: Recursividade / Fibonacci / Cache | Complexidade: tempo O(n) | Memória: cache O(n) + pilha O(n)
Palavras-chave: memorização, memoization, cache, dicionário, lru_cache, cache_info, hits, misses, 2n-1, top-down, cache quente, RecursionError, atividade 03

O que faz:
- Implementa fib_memo com um dict e fib_lru com functools.lru_cache, contando as chamadas (2n − 1).
- Compara com o recursivo puro para n = 5..30 (quantas vezes menos chamadas).
- Mostra cache_info() (acertos e falhas) e o custo de uma consulta com o cache já quente.
- Mostra o RecursionError da versão top-down para n grande e como evitá-lo.

Perguntas prováveis:
P: O que é memorização e por que ela ajuda?
R: Guardar o resultado de cada subproblema na primeira vez que é calculado e reaproveitá-lo depois (consulta O(1) no dicionário). Cada fib(k) é calculado uma única vez: o total cai de exponencial para linear.
P: Quantas chamadas faz a versão memoizada?
R: 2n − 1: cada uma das n−1 chaves novas dispara duas chamadas, e as demais caem no cache. Para n = 10: 19; n = 20: 39; n = 30: 59.
P: Qual é o custo em memória da memorização?
R: O(n) para o cache (uma entrada por valor calculado) mais O(n) de pilha na versão recursiva. É a troca clássica: memória por tempo.
P: Por que fib_memo(5000) pode dar RecursionError e a iterativa não?
R: A memoizada ainda é recursiva e desce n níveis antes de preencher o cache; a iterativa usa um laço e duas variáveis (pilha constante).
P: O que é um cache quente?
R: Cache já preenchido por chamadas anteriores; a próxima consulta custa O(1). Em benchmarks o cache deve ser zerado, senão mede-se uma consulta e não o algoritmo.
"""
import sys
import time
from functools import lru_cache

chamadas = 0


def fib_memo(n, cache=None):
    """Top-down com dicionario. Cache novo a cada chamada externa."""
    global chamadas
    chamadas += 1
    if cache is None:
        cache = {0: 0, 1: 1}
    if n in cache:                             # ja calculado -> consulta O(1)
        return cache[n]
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]


@lru_cache(maxsize=None)
def fib_lru(n):
    if n < 2:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


def fib_recursivo_chamadas(n):
    """So para comparar: numero de chamadas do recursivo puro = 2F(n+1)-1."""
    a, b = 0, 1
    for _ in range(n + 1):
        a, b = b, a + b
    return 2 * a - 1


if __name__ == "__main__":
    print(f"{'n':>3} {'recursivo puro':>15} {'memoizado':>10} {'2n-1':>6} {'vezes menos':>12}")
    for n in (5, 10, 15, 20, 25, 30):
        chamadas = 0
        fib_memo(n)
        puro = fib_recursivo_chamadas(n)
        print(f"{n:>3} {puro:>15} {chamadas:>10} {2 * n - 1:>6} {puro / chamadas:>11.0f}x")

    print("\n@lru_cache: fib_lru(30) =", fib_lru(30))
    print("  cache_info:", fib_lru.cache_info(), " <- misses = valores calculados; hits = reaproveitados")

    inicio = time.perf_counter()
    fib_lru(300)                                # aquece o cache
    t_frio = time.perf_counter() - inicio
    inicio = time.perf_counter()
    fib_lru(300)                                # cache quente
    t_quente = time.perf_counter() - inicio
    print(f"\nfib_lru(300): 1a chamada {t_frio * 1e6:.1f} us | 2a chamada (cache quente) {t_quente * 1e6:.2f} us")

    print("\nTop-down e recursivo: para n grande estoura a pilha (limite =", sys.getrecursionlimit(), ")")
    try:
        fib_memo(5000)
    except RecursionError:
        print("  fib_memo(5000) -> RecursionError")
    print("  solucao: preencher o cache de baixo para cima (bottom-up) ou usar a versao iterativa.")
