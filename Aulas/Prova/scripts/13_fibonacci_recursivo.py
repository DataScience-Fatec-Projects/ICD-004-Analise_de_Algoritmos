"""[13] Fibonacci recursivo puro: árvore de chamadas, contagem e crescimento exponencial
Tema: Recursividade / Fibonacci | Complexidade: tempo O(2^n) (exatamente Θ(1,618^n)) | Memória: pilha O(n)
Palavras-chave: fibonacci, recursivo puro, árvore de chamadas, subproblemas sobrepostos, recálculo, exponencial, razão áurea, phi 1.618, 2F(n+1)-1, chamadas, atividade 03

O que faz:
- Desenha a árvore de chamadas de fib(5) e conta quantas vezes cada subproblema é recalculado.
- Conta as chamadas para n = 5..30 e confere a fórmula fechada T(n) = 2·F(n+1) − 1.
- Mostra que a razão T(n)/T(n−1) converge para a razão áurea (~1,618): cada +1 em n multiplica o trabalho por 1,618.

Perguntas prováveis:
P: Por que o Fibonacci recursivo puro é ineficiente?
R: Porque recalcula os mesmos subproblemas muitas vezes (fib(2) aparece 3 vezes em fib(5); fib(1), 5 vezes). A árvore de chamadas cresce exponencialmente.
P: Qual é a complexidade e como se chega a ela?
R: T(n) = T(n-1) + T(n-2) + 1, a própria recorrência de Fibonacci; solução T(n) = 2·F(n+1) − 1 = Θ(1,618^n), que está em O(2^n). Confirmado: 15, 177, 21.891 e 2.692.537 chamadas para n = 5, 10, 20, 30.
P: Se fib(30) leva 0,13 s, quanto leva fib(40)?
R: Cerca de 0,13 × 1,618^10 ≈ 0,13 × 123 ≈ 16 s. Cada +1 em n multiplica o tempo por ~1,618.
P: O tempo é exponencial; a memória também?
R: Não. A pilha tem no máximo n quadros ao mesmo tempo (a árvore é percorrida em profundidade): memória O(n).
"""
from collections import Counter

chamadas = 0


def fib_recursivo(n):
    global chamadas
    chamadas += 1
    if n < 2:                                  # casos base: F(0) = 0, F(1) = 1
        return n
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)


def contar_chamadas(n):
    global chamadas
    chamadas = 0
    valor = fib_recursivo(n)
    return valor, chamadas


def fib_iterativo(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def desenhar_arvore(n, prefixo="", ultimo=True, raiz=True, contador=None):
    contador = Counter() if contador is None else contador
    contador[n] += 1
    conector = "" if raiz else ("`- " if ultimo else "|- ")
    print(f"{prefixo}{conector}fib({n}){'   <- caso base' if n < 2 else ''}")
    if n >= 2:
        novo = prefixo if raiz else prefixo + ("   " if ultimo else "|  ")
        desenhar_arvore(n - 1, novo, False, False, contador)
        desenhar_arvore(n - 2, novo, True, False, contador)
    return contador


if __name__ == "__main__":
    print("ARVORE DE CHAMADAS DE fib(5)")
    contador = desenhar_arvore(5)
    print("\nQuantas vezes cada subproblema foi calculado:")
    for k in sorted(contador):
        print(f"  fib({k}) -> {contador[k]}x")
    print(f"  total = {sum(contador.values())} chamadas")

    print(f"\n{'n':>3} {'chamadas':>10} {'2F(n+1)-1':>10} {'T(n)/T(n-1)':>12}")
    for n in (5, 10, 15, 20, 21, 22, 23, 24, 25):
        _, c = contar_chamadas(n)
        formula = 2 * fib_iterativo(n + 1) - 1
        anterior = 2 * fib_iterativo(n) - 1        # T(n-1) pela formula fechada
        print(f"{n:>3} {c:>10} {formula:>10} {c / anterior:>12.4f}")
    print("Razao converge para phi = 1,618 (razao aurea): crescimento exponencial.")
